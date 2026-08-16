from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from recommendation import recommend_courses, get_user_skills


app = FastAPI()


class RecommendRequest(BaseModel):
    user_id: int


@app.get("/")
def home():
    return {
        "message": "Project 5 API is running!"
    }


@app.post("/api/recommend")
def recommend(data: RecommendRequest):

    user_id = data.user_id

    skills = get_user_skills(user_id)

    if not skills:
        raise HTTPException(
            status_code=404,
            detail="User not found or has no skills"
        )

    recommendations = recommend_courses(
        user_id,
        top_n=3
    )

    return {
        "user_id": user_id,
        "extracted_skills": skills,
        "recommended_courses": recommendations,
        "explanation": (
            "Courses are recommended based on similarity "
            "between the user's skills and course descriptions."
        )
    }