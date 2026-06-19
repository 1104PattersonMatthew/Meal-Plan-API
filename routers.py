from fastapi import APIRouter, Depends, HTTPException, status
from uuid import uuid4
from datetime import datetime

from models import MealCreate, MealResponse
from storage import read_data, write_data
from auth import verify_api_key


router = APIRouter(
    tags=["Meals"],
    dependencies=[Depends(verify_api_key)]
)

DATA_FILE = "data/meals.json"

#creates a meal
@router.post(
    "/meals",
    response_model=MealResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a meal",
    description="Creates a new meal plan entry and saves it to the JSON file.",
    responses={
        403: {"description": "Invalid or missing API key"},
        422: {"description": "Validation error"}
    }
)
def create_meal(meal: MealCreate):
    meals = read_data(DATA_FILE)

    new_meal = meal.model_dump()
    new_meal["id"] = str(uuid4())
    new_meal["created_at"] = datetime.now().isoformat()

    meals.append(new_meal)
    write_data(DATA_FILE, meals)

    return new_meal

#returns all meals in json
@router.get(
    "/meals",
    response_model=list[MealResponse],
    summary="Get all meals",
    description="Returns all saved meal plan entries.",
    responses={
        403: {"description": "Invalid or missing API key"}
    }
)
def get_all_meals():
    return read_data(DATA_FILE)


@router.get(
    "/meals/summary",
    summary="Get meal summary",
    description="Returns a simple summary showing how many meals exist for each meal type.",
    responses={
        403: {"description": "Invalid or missing API key"}
    }
)
def get_meal_summary():
    meals = read_data(DATA_FILE)

    summary = {
        "total_meals": len(meals),
        "breakfast": 0,
        "lunch": 0,
        "dinner": 0,
        "snack": 0,
        "other": 0
    }

    for meal in meals:
        meal_type = meal["meal_type"].lower()

        if meal_type == "breakfast":
            summary["breakfast"] += 1
        elif meal_type == "lunch":
            summary["lunch"] += 1
        elif meal_type == "dinner":
            summary["dinner"] += 1
        elif meal_type == "snack":
            summary["snack"] += 1
        else:
            summary["other"] += 1

    return summary


@router.get(
    "/shopping-list",
    summary="Generate shopping list",
    description="Creates a simple shopping list by combining all ingredients from all meals.",
    responses={
        403: {"description": "Invalid or missing API key"}
    }
)
def get_shopping_list():
    meals = read_data(DATA_FILE)
    shopping_list = []

    for meal in meals:
        for ingredient in meal["ingredients"]:
            if ingredient not in shopping_list:
                shopping_list.append(ingredient)

    return {
        "shopping_list": shopping_list
    }


@router.get(
    "/meals/{meal_id}",
    response_model=MealResponse,
    summary="Get one meal",
    description="Returns one meal plan entry by its unique ID.",
    responses={
        403: {"description": "Invalid or missing API key"},
        404: {"description": "Meal not found"}
    }
)
def get_meal_by_id(meal_id: str):
    meals = read_data(DATA_FILE)

    for meal in meals:
        if meal["id"] == meal_id:
            return meal

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Meal not found"
    )


@router.put(
    "/meals/{meal_id}",
    response_model=MealResponse,
    summary="Update a meal",
    description="Updates an existing meal plan entry by its unique ID.",
    responses={
        403: {"description": "Invalid or missing API key"},
        404: {"description": "Meal not found"},
        422: {"description": "Validation error"}
    }
)
def update_meal(meal_id: str, updated_meal: MealCreate):
    meals = read_data(DATA_FILE)

    for index, meal in enumerate(meals):
        if meal["id"] == meal_id:
            meal_data = updated_meal.model_dump()
            meal_data["id"] = meal["id"]
            meal_data["created_at"] = meal["created_at"]

            meals[index] = meal_data
            write_data(DATA_FILE, meals)

            return meal_data

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Meal not found"
    )


@router.delete(
    "/meals/{meal_id}",
    summary="Delete a meal",
    description="Deletes an existing meal plan entry by its unique ID.",
    responses={
        403: {"description": "Invalid or missing API key"},
        404: {"description": "Meal not found"}
    }
)
def delete_meal(meal_id: str):
    meals = read_data(DATA_FILE)

    for meal in meals:
        if meal["id"] == meal_id:
            meals.remove(meal)
            write_data(DATA_FILE, meals)

            return {
                "message": "Meal deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Meal not found"
    )