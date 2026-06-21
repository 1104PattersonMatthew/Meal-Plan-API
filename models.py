from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MealCreate(BaseModel):
    day: str = Field(..., description="Day of the week for the meal")
    meal_type: str = Field(..., description="Type of meal, such as Breakfast, Lunch, Dinner, or Snack")
    meal_name: str = Field(..., description="Name of the planned meal")
    ingredients: list[str] = Field(..., description="List of ingredients needed for the meal")
    notes: Optional[str] = Field(None, description="Optional notes about the meal")


class MealResponse(MealCreate):
    id: str = Field(..., description="Unique ID for the meal")
    created_at: datetime = Field(..., description="Timestamp when the meal was created")


class MealSummaryResponse(BaseModel):
    total_meals: int = Field(..., description="Total number of saved meals")
    breakfast: int = Field(..., description="Number of breakfast meals")
    lunch: int = Field(..., description="Number of lunch meals")
    dinner: int = Field(..., description="Number of dinner meals")
    snack: int = Field(..., description="Number of snack meals")
    other: int = Field(..., description="Number of meals that do not match the main meal types")


class ShoppingListResponse(BaseModel):
    shopping_list: list[str] = Field(..., description="Combined list of unique ingredients from all meals")


class MessageResponse(BaseModel):
    message: str = Field(..., description="Response message")