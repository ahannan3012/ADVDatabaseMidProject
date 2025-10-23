from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Why Pydantic models? FastAPI uses them to validate data automatically

class Movie(BaseModel):
    """Movie data structure"""
    title: str
    release_year: int
    genres: List[str]  # List because movie can have multiple genres
    cast: List[str]    # List of actor names
    director: str
    rating: float      # Average rating like 4.5 out of 5

class User(BaseModel):
    """User data structure"""
    name: str
    email: str
    subscription_type: str  # e.g., "Basic", "Premium", "Free"

class WatchHistory(BaseModel):
    """Track what users watched"""
    user_id: str
    movie_id: str
    timestamp: datetime
    watch_duration: int  # in minutes

class Review(BaseModel):
    """User reviews for movies"""
    user_id: str
    movie_id: str
    rating: float       # User's rating 1-5
    review_text: str
    timestamp: datetime