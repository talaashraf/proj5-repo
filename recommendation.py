from sqlalchemy import select
from database import engine
from models import users, skills, user_skills, courses, recommendation_logs
from embeddings import (
    build_user_vector,
    generate_course_embeddings,
    compute_similarity
)


def get_user_skills(user_id):
    with engine.connect() as conn:

        query = (
            select(skills.c.skill_name)
            .select_from(
                user_skills.join(
                    skills,
                    user_skills.c.skill_id == skills.c.id
                )
            )
            .where(user_skills.c.user_id == user_id)
        )

        result = conn.execute(query).scalars().all()

        return result


def get_courses():
    with engine.connect() as conn:

        query = select(
            courses.c.id,
            courses.c.course_name,
            courses.c.description
        )

        result = conn.execute(query).fetchall()

        return result


def recommend_courses(user_id, top_n=3):

    
    user_skill_list = get_user_skills(user_id)

    if not user_skill_list:
        return []

    user_vector = build_user_vector(user_skill_list)

    
    course_rows = get_courses()

    if not course_rows:
        return []

    course_descriptions = [
        course.description
        for course in course_rows
    ]

    
    course_embeddings = generate_course_embeddings(
        course_descriptions
    )

    
    similarities = compute_similarity(
        user_vector,
        course_embeddings
    )

    
    recommendations = []

    for course, score in zip(course_rows, similarities):
        recommendations.append({
            "course_id": course.id,
            "course_name": course.course_name,
            "description": course.description,
            "score": float(score)
        })

    
    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations[:top_n]

def course_recommendation_agent(user_id):

    # Get top 3 course recommendations
    recommendations = recommend_courses(user_id, top_n=3)

    # Guardrail: no recommendations found
    if not recommendations:
        return {
            "agent": "Course Recommendation Agent",
            "status": "No recommendations found",
            "recommendations": []
        }

    # Logging:
    # Save recommendation results in the database
    with engine.begin() as conn:
        for course in recommendations:
            conn.execute(
                recommendation_logs.insert().values(
                    user_id=user_id,
                    course_id=course["course_id"],
                    score=str(course["score"])
                )
            )

    # Return final result
    return {
        "agent": "Course Recommendation Agent",
        "status": "Success",
        "recommendations": recommendations
    }


# Test
if __name__ == "__main__":

    user_id = 10

    results = recommend_courses(user_id)

    print("\nTop Recommendations:")

    for course in results:
        print(
            course["course_name"],
            "->",
            course["score"]
        )