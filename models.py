from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

#uses pyndatic model named MealCreate
#optional means it can be left blank
class MealCreate(BaseModel):
    day: str = Field(..., description="Day of the week for the meal")
    meal_type: str = Field(..., description="Type of meal, such as Breakfast, Lunch, Dinner, or Snack")
    meal_name: str = Field(..., description="Name of the planned meal")
    ingredients: list[str] = Field(..., description="List of ingredients needed for the meal")
    notes: Optional[str] = Field(None, description="Optional notes about the meal")


class MealResponse(MealCreate):
    id: str = Field(..., description="Unique ID for the meal")
    created_at: datetime = Field(..., description="Timestamp when the meal was created")