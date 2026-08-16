from skill_extraction import skill_extraction_agent
from recommendation import course_recommendation_agent


def run_workflow(user_text, user_id):

    # Step 1: Skill Extraction
    skill_result = skill_extraction_agent(user_text)

    if not skill_result["skills"]:
        return {
            "status": "failed",
            "message": "No skills were extracted."
        }
    skills=skill_result["skills"]

    # Step 2 + 3 + 4:
    # Embeddings + Course Retrieval + Ranking
    recommendation_result = course_recommendation_agent(user_id)

    if recommendation_result["status"] != "Success":
        return {
                "status": "fallback",
                "skills": skills,
                "recommendations": [
                    "Python for Data Science",
                    "SQL and Databases"
                ],
                "message": "No strong matches were found, so default recommendations were returned."
            }
    # Step 5: Explanation
    explanation = (
        "Courses were recommended based on the similarity "
        "between the user's skills and course descriptions."
    )

    return {
        "status": "success",
        "skills": skill_result["skills"],
        "recommendations": recommendation_result["recommendations"],
        "explanation": explanation
    }


if __name__ == "__main__":

    user_text = input("Enter your skills or experience: ")

    user_id = int(input("Enter user ID: "))

    result = run_workflow(user_text, user_id)

    print(result)