# Movie Streaming Backend - FA23-BCS-013-A

## Project Overview
This is a movie streaming platform backend built with FastAPI and MongoDB. It provides APIs for searching movies, viewing watch history, and reading reviews.

## Technologies Used
- **Python 3.x**: Programming language
- **FastAPI**: Web framework for building APIs
- **MongoDB**: NoSQL database (local installation)
- **PyMongo**: Python driver for MongoDB

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start MongoDB
Make sure MongoDB is running on your local machine (default: localhost:27017)

### 3. Populate Database
Run this command to create sample data:
```bash
python sample_data.py
```

### 4. Run the Application
```bash
uvicorn app:app --reload
```

The API will be available at: `http://localhost:8000`

## API Endpoints

### 1. User Watch History
- **URL**: `/users/{user_id}/history`
- **Method**: GET
- **Description**: Get all movies watched by a user

### 2. Movie Reviews
- **URL**: `/movies/{movie_id}/reviews`
- **Method**: GET
- **Description**: Get all reviews for a specific movie

### 3. Movie Search (Hybrid)
- **URL**: `/movies/search?query=...`
- **Method**: GET
- **Description**: Search movies with hybrid ranking (text match + rating + popularity)

### 4. Top Watched Movies
- **URL**: `/movies/top-watched`
- **Method**: GET
- **Description**: Get top 5 most-watched movies in the last 30 days

## Testing the APIs

### Using Browser
1. Open `http://localhost:8000/docs` for interactive API documentation
2. Try each endpoint directly from the browser

### Using Command Line (curl)
```bash
# Search movies
curl "http://localhost:8000/movies/search?query=godfather"

# Top watched
curl "http://localhost:8000/movies/top-watched"
```

## Database Schema

### Movies Collection
```json
{
  "title": "string",
  "release_year": "number",
  "genres": ["array of strings"],
  "cast": ["array of strings"],
  "director": "string",
  "rating": "number (0-5)"
}
```

### Users Collection
```json
{
  "name": "string",
  "email": "string",
  "subscription_type": "string (Free/Basic/Premium)"
}
```

### Watch History Collection
```json
{
  "user_id": "string",
  "movie_id": "string",
  "timestamp": "datetime",
  "watch_duration": "number (minutes)"
}
```

### Reviews Collection
```json
{
  "user_id": "string",
  "movie_id": "string",
  "rating": "number (1-5)",
  "review_text": "string",
  "timestamp": "datetime"
}
```

## Hybrid Search Formula
- **50% Text Similarity**: How well query matches title/director/cast
- **30% Rating**: Movie's average rating
- **20% Popularity**: Number of times watched

## Student Information
- **Name**: Abdul Hannan
- **Roll No**: FA23-BCS-013-A
- **Course**: Advanced Database Systems
- **Semester**: 5th BSCSs