from database import movies_collection, users_collection, watch_history_collection, reviews_collection
from datetime import datetime, timedelta
import random

# Sample movies data
movies_data = [
    {
        "title": "The Godfather",
        "release_year": 1972,
        "genres": ["Crime", "Drama"],
        "cast": ["Marlon Brando", "Al Pacino", "James Caan"],
        "director": "Francis Ford Coppola",
        "rating": 4.8
    },
    {
        "title": "The Dark Knight",
        "release_year": 2008,
        "genres": ["Action", "Crime", "Drama"],
        "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
        "director": "Christopher Nolan",
        "rating": 4.7
    },
    {
        "title": "Inception",
        "release_year": 2010,
        "genres": ["Action", "Sci-Fi", "Thriller"],
        "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page"],
        "director": "Christopher Nolan",
        "rating": 4.6
    },
    {
        "title": "Pulp Fiction",
        "release_year": 1994,
        "genres": ["Crime", "Drama"],
        "cast": ["John Travolta", "Uma Thurman", "Samuel L. Jackson"],
        "director": "Quentin Tarantino",
        "rating": 4.5
    },
    {
        "title": "The Shawshank Redemption",
        "release_year": 1994,
        "genres": ["Drama"],
        "cast": ["Tim Robbins", "Morgan Freeman"],
        "director": "Frank Darabont",
        "rating": 4.9
    },
    {
        "title": "Forrest Gump",
        "release_year": 1994,
        "genres": ["Drama", "Romance"],
        "cast": ["Tom Hanks", "Robin Wright", "Gary Sinise"],
        "director": "Robert Zemeckis",
        "rating": 4.4
    },
    {
        "title": "The Matrix",
        "release_year": 1999,
        "genres": ["Action", "Sci-Fi"],
        "cast": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"],
        "director": "Lana Wachowski",
        "rating": 4.5
    },
    {
        "title": "Interstellar",
        "release_year": 2014,
        "genres": ["Adventure", "Drama", "Sci-Fi"],
        "cast": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"],
        "director": "Christopher Nolan",
        "rating": 4.6
    },
    {
        "title": "Gladiator",
        "release_year": 2000,
        "genres": ["Action", "Adventure", "Drama"],
        "cast": ["Russell Crowe", "Joaquin Phoenix"],
        "director": "Ridley Scott",
        "rating": 4.4
    },
    {
        "title": "The Lion King",
        "release_year": 1994,
        "genres": ["Animation", "Adventure", "Drama"],
        "cast": ["Matthew Broderick", "Jeremy Irons", "James Earl Jones"],
        "director": "Roger Allers",
        "rating": 4.3
    },
    {
        "title": "Avatar",
        "release_year": 2009,
        "genres": ["Action", "Adventure", "Fantasy"],
        "cast": ["Sam Worthington", "Zoe Saldana", "Sigourney Weaver"],
        "director": "James Cameron",
        "rating": 4.2
    },
    {
        "title": "Titanic",
        "release_year": 1997,
        "genres": ["Drama", "Romance"],
        "cast": ["Leonardo DiCaprio", "Kate Winslet"],
        "director": "James Cameron",
        "rating": 4.3
    },
    {
        "title": "The Avengers",
        "release_year": 2012,
        "genres": ["Action", "Adventure", "Sci-Fi"],
        "cast": ["Robert Downey Jr.", "Chris Evans", "Scarlett Johansson"],
        "director": "Joss Whedon",
        "rating": 4.1
    },
    {
        "title": "Jurassic Park",
        "release_year": 1993,
        "genres": ["Adventure", "Sci-Fi", "Thriller"],
        "cast": ["Sam Neill", "Laura Dern", "Jeff Goldblum"],
        "director": "Steven Spielberg",
        "rating": 4.4
    },
    {
        "title": "Star Wars",
        "release_year": 1977,
        "genres": ["Action", "Adventure", "Fantasy"],
        "cast": ["Mark Hamill", "Harrison Ford", "Carrie Fisher"],
        "director": "George Lucas",
        "rating": 4.5
    },
    {
        "title": "The Silence of the Lambs",
        "release_year": 1991,
        "genres": ["Crime", "Drama", "Thriller"],
        "cast": ["Jodie Foster", "Anthony Hopkins"],
        "director": "Jonathan Demme",
        "rating": 4.6
    },
    {
        "title": "Saving Private Ryan",
        "release_year": 1998,
        "genres": ["Drama", "War"],
        "cast": ["Tom Hanks", "Matt Damon", "Tom Sizemore"],
        "director": "Steven Spielberg",
        "rating": 4.5
    },
    {
        "title": "The Green Mile",
        "release_year": 1999,
        "genres": ["Crime", "Drama", "Fantasy"],
        "cast": ["Tom Hanks", "Michael Clarke Duncan", "David Morse"],
        "director": "Frank Darabont",
        "rating": 4.4
    },
    {
        "title": "Goodfellas",
        "release_year": 1990,
        "genres": ["Biography", "Crime", "Drama"],
        "cast": ["Robert De Niro", "Ray Liotta", "Joe Pesci"],
        "director": "Martin Scorsese",
        "rating": 4.6
    },
    {
        "title": "Fight Club",
        "release_year": 1999,
        "genres": ["Drama"],
        "cast": ["Brad Pitt", "Edward Norton", "Helena Bonham Carter"],
        "director": "David Fincher",
        "rating": 4.5
    }
]

# Sample users data
users_data = [
    {"name": "Ahmed Ali", "email": "ahmed@example.com", "subscription_type": "Premium"},
    {"name": "Fatima Khan", "email": "fatima@example.com", "subscription_type": "Basic"},
    {"name": "Hassan Raza", "email": "hassan@example.com", "subscription_type": "Premium"},
    {"name": "Ayesha Malik", "email": "ayesha@example.com", "subscription_type": "Free"},
    {"name": "Bilal Ahmed", "email": "bilal@example.com", "subscription_type": "Basic"},
    {"name": "Zainab Shah", "email": "zainab@example.com", "subscription_type": "Premium"},
    {"name": "Usman Tariq", "email": "usman@example.com", "subscription_type": "Basic"},
    {"name": "Mariam Noor", "email": "mariam@example.com", "subscription_type": "Free"},
    {"name": "Ali Hassan", "email": "alihassan@example.com", "subscription_type": "Premium"},
    {"name": "Sana Iqbal", "email": "sana@example.com", "subscription_type": "Basic"}
]


def populate_database():
    """Fill database with sample data"""
    
    # Clear existing data
    # Why clear? Start fresh each time we run this
    movies_collection.delete_many({})
    users_collection.delete_many({})
    watch_history_collection.delete_many({})
    reviews_collection.delete_many({})
    
    print("Inserting movies...")
    movies_result = movies_collection.insert_many(movies_data)
    movie_ids = movies_result.inserted_ids
    
    print("Inserting users...")
    users_result = users_collection.insert_many(users_data)
    user_ids = users_result.inserted_ids
    
    print("Creating watch history...")
    # Create 100 watch history records
    # Why 100? Enough data to show patterns but not overwhelming
    watch_history_data = []
    for _ in range(100):
        random_user = random.choice(user_ids)
        random_movie = random.choice(movie_ids)
        # Random date in last 60 days
        random_days_ago = random.randint(0, 60)
        timestamp = datetime.now() - timedelta(days=random_days_ago)
        watch_duration = random.randint(30, 180)  # 30-180 minutes
        
        watch_history_data.append({
            "user_id": str(random_user),
            "movie_id": str(random_movie),
            "timestamp": timestamp,
            "watch_duration": watch_duration
        })
    
    watch_history_collection.insert_many(watch_history_data)
    
    print("Creating reviews...")
    # Create 50 reviews
    reviews_data = []
    for _ in range(50):
        random_user = random.choice(user_ids)
        random_movie = random.choice(movie_ids)
        rating = round(random.uniform(3.0, 5.0), 1)  # Random rating 3.0-5.0
        
        # Simple review texts
        review_texts = [
            "Great movie! Highly recommend.",
            "Amazing performances and direction.",
            "A must-watch film.",
            "Good story and excellent cast.",
            "Loved every minute of it.",
            "One of the best movies I have seen.",
            "Decent movie, worth watching.",
            "Brilliant cinematography.",
            "Engaging plot and great acting."
        ]
        
        reviews_data.append({
            "user_id": str(random_user),
            "movie_id": str(random_movie),
            "rating": rating,
            "review_text": random.choice(review_texts),
            "timestamp": datetime.now() - timedelta(days=random.randint(0, 60))
        })
    
    reviews_collection.insert_many(reviews_data)
    
    print("Database populated successfully!")
    print(f"Movies: {len(movie_ids)}")
    print(f"Users: {len(user_ids)}")
    print(f"Watch history: 100 records")
    print(f"Reviews: 50 records")


if __name__ == "__main__":
    populate_database()