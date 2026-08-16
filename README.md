# proj5-repo
# Setup Instructions
1. Create and activate a virtual environment.
2. Install the required Python packages.
3. Configure the database connection.
4. Run the application using: uvicorn app:app --reload
5. Open the FastAPI documentation at:http://127.0.0.1:8000/docs
## Example Input and Output

### Input

```json
{
  "user_id": 10
}
```

# Output

The API returns the user's extracted skills and recommended courses ranked by similarity.

```json
{
  "user_id": 10,
  "extracted_skills": [
    "Python",
    "SQL",
    "Machine Learning"
  ],
  "recommended_courses": [
    "Machine Learning Foundations",
    "SQL and Databases",
    "Python for Data Science"
  ]
}
```
# Explanation of Approach
The system recommends courses based on the user's existing skills.
1. The user's skills are retrieved from the PostgreSQL database.
2. SentenceTransformer is used to convert the skills into embeddings.
3. The skill embeddings are combined to create a user profile vector.
4. Course descriptions are also converted into embeddings.
5. Cosine similarity is used to compare the user profile with the courses.
6. The courses are ranked based on similarity scores.
7. The top 3 courses are returned through the FastAPI endpoint.