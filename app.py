from fastapi import FastAPI, HTTPException, Query
from database import get_db, create_indexes
from bson import ObjectId
from datetime import datetime, timedelta
from typing import Optional

app = FastAPI(title="Movie Streaming Backend")

# Get database connection
db = get_db()

# Create indexes when app starts
# Why here? Run once when server starts
@app.on_event("startup")
async def startup_event():
    create_indexes()


# Helper function to convert MongoDB ObjectId to string
# Why? ObjectId is not JSON serializable, need to convert to string
def convert_objectid(data):
    """Convert MongoDB ObjectId to string for JSON response"""
    if isinstance(data, list):
        for item in data:
            if '_id' in item:
                item['_id'] = str(item['_id'])
    elif isinstance(data, dict):
        if '_id' in data:
            data['_id'] = str(data['_id'])
    return data


# API 1: Get user's watch history
@app.get("/users/{user_id}/history")
async def get_user_watch_history(user_id: str):
    """
    Get all movies watched by a specific user
    Why this API? Users want to see their viewing history
    """
    
    # Check if user exists
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get watch history for this user
    # Why aggregate? Need to join watch_history with movies collection
    pipeline = [
        # Step 1: Filter watch history for this user
        {"$match": {"user_id": user_id}},
        
        # Step 2: Sort by timestamp (newest first)
        {"$sort": {"timestamp": -1}},
        
        # Step 3: Join with movies collection to get movie details
        # Why lookup? Like SQL JOIN - get movie info for each watch record
        {"$lookup": {
            "from": "movies",
            "localField": "movie_id",
            "foreignField": "_id",
            "as": "movie_details"
        }},
        
        # Step 4: Unwind movie_details array (convert array to object)
        {"$unwind": "$movie_details"},
        
        # Step 5: Format output - select which fields to show
        {"$project": {
            "movie_title": "$movie_details.title",
            "movie_id": "$movie_id",
            "watched_on": "$timestamp",
            "watch_duration": "$watch_duration",
            "genres": "$movie_details.genres",
            "rating": "$movie_details.rating"
        }}
    ]
    
    history = list(db.watch_history.aggregate(pipeline))
    history = convert_objectid(history)
    
    return {
        "user_id": user_id,
        "user_name": user['name'],
        "total_movies_watched": len(history),
        "watch_history": history
    }


# API 2: Get movie reviews
@app.get("/movies/{movie_id}/reviews")
async def get_movie_reviews(movie_id: str):
    """
    Get all reviews for a specific movie
    Why this API? Users want to read reviews before watching
    """
    
    # Check if movie exists
    movie = db.movies.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Get all reviews for this movie
    pipeline = [
        # Step 1: Filter reviews for this movie
        {"$match": {"movie_id": movie_id}},
        
        # Step 2: Sort by timestamp (newest first)
        {"$sort": {"timestamp": -1}},
        
        # Step 3: Join with users collection to get reviewer name
        {"$lookup": {
            "from": "users",
            "localField": "user_id",
            "foreignField": "_id",
            "as": "user_details"
        }},
        
        # Step 4: Unwind user_details
        {"$unwind": "$user_details"},
        
        # Step 5: Format output
        {"$project": {
            "user_name": "$user_details.name",
            "rating": "$rating",
            "review_text": "$review_text",
            "posted_on": "$timestamp"
        }}
    ]
    
    reviews = list(db.reviews.aggregate(pipeline))
    reviews = convert_objectid(reviews)
    
    # Calculate average rating
    # Why? Give users quick overview of movie quality
    avg_rating = sum(r['rating'] for r in reviews) / len(reviews) if reviews else 0
    
    return {
        "movie_id": movie_id,
        "movie_title": movie['title'],
        "average_rating": round(avg_rating, 2),
        "total_reviews": len(reviews),
        "reviews": reviews
    }


# API 3: Hybrid search for movies
@app.get("/movies/search")
async def search_movies(query: str = Query(..., description="Search query")):
    """
    Search movies with hybrid ranking
    Why hybrid? Combines text search + rating + popularity for best results
    """
    
    # Step 1: Text search using MongoDB text index
    # Why $text? Uses the text index we created for fast search
    search_results = list(db.movies.find(
        {"$text": {"$search": query}},
        {"score": {"$meta": "textScore"}}  # Get relevance score
    ).sort([("score", {"$meta": "textScore"})]))
    
    if not search_results:
        return {
            "query": query,
            "total_results": 0,
            "results": []
        }
    
    # Step 2: Calculate popularity (watch count) for each movie
    # Why? Popular movies should rank higher
    movie_ids = [str(movie['_id']) for movie in search_results]
    
    # Count how many times each movie was watched
    watch_counts = {}
    for movie_id in movie_ids:
        count = db.watch_history.count_documents({"movie_id": movie_id})
        watch_counts[movie_id] = count
    
    # Find max watch count for normalization
    # Why normalize? Convert all scores to 0-1 range for fair comparison
    max_watch_count = max(watch_counts.values()) if watch_counts else 1
    
    # Step 3: Calculate hybrid score for each movie
    # Formula: 50% similarity + 30% rating + 20% popularity
    for movie in search_results:
        movie_id = str(movie['_id'])
        
        # Normalize text similarity score (0-1)
        # Why divide by 10? MongoDB text scores are usually 0-10
        similarity_score = min(movie.get('score', 0) / 10, 1.0)
        
        # Normalize rating (0-1)
        # Why divide by 5? Ratings are out of 5
        rating_score = movie.get('rating', 0) / 5.0
        
        # Normalize popularity (0-1)
        popularity_score = watch_counts.get(movie_id, 0) / max_watch_count
        
        # Calculate final hybrid score
        hybrid_score = (
            0.5 * similarity_score +  # 50% weight to text match
            0.3 * rating_score +      # 30% weight to rating
            0.2 * popularity_score    # 20% weight to popularity
        )
        
        movie['hybrid_score'] = round(hybrid_score, 3)
        movie['similarity_score'] = round(similarity_score, 3)
        movie['rating_score'] = round(rating_score, 3)
        movie['popularity_score'] = round(popularity_score, 3)
        movie['watch_count'] = watch_counts.get(movie_id, 0)
    
    # Step 4: Sort by hybrid score (highest first)
    search_results.sort(key=lambda x: x['hybrid_score'], reverse=True)
    
    # Convert ObjectId to string for JSON response
    search_results = convert_objectid(search_results)
    
    return {
        "query": query,
        "total_results": len(search_results),
        "results": search_results
    }


# Aggregation Query: Top 5 most-watched movies in last month
@app.get("/movies/top-watched")
async def get_top_watched_movies():
    """
    Get top 5 most-watched movies in the last 30 days
    Why this query? Show trending/popular movies to users
    """
    
    # Calculate date 30 days ago
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    # Aggregation pipeline
    pipeline = [
        # Step 1: Filter watch history from last 30 days
        {"$match": {
            "timestamp": {"$gte": thirty_days_ago}
        }},
        
        # Step 2: Group by movie_id and count watches
        # Why group? Count how many times each movie was watched
        {"$group": {
            "_id": "$movie_id",
            "watch_count": {"$sum": 1}
        }},
        
        # Step 3: Sort by watch count (descending)
        {"$sort": {"watch_count": -1}},
        
        # Step 4: Limit to top 5
        {"$limit": 5},
        
        # Step 5: Join with movies collection to get movie details
        {"$lookup": {
            "from": "movies",
            "localField": "_id",
            "foreignField": "_id",
            "as": "movie_details"
        }},
        
        # Step 6: Unwind movie_details
        {"$unwind": "$movie_details"},
        
        # Step 7: Format output
        {"$project": {
            "movie_id": "$_id",
            "title": "$movie_details.title",
            "director": "$movie_details.director",
            "rating": "$movie_details.rating",
            "genres": "$movie_details.genres",
            "watch_count": "$watch_count"
        }}
    ]
    
    top_movies = list(db.watch_history.aggregate(pipeline))
    top_movies = convert_objectid(top_movies)
    
    return {
        "period": "Last 30 days",
        "total_movies": len(top_movies),
        "top_movies": top_movies
    }


# Root endpoint
@app.get("/")
async def root():
    """Welcome message"""
    return {
        "message": "Movie Streaming Backend API",
        "endpoints": [
            "/users/{user_id}/history - Get user watch history",
            "/movies/{movie_id}/reviews - Get movie reviews",
            "/movies/search?query=... - Search movies",
            "/movies/top-watched - Top 5 watched movies (last month)"
        ]
    }