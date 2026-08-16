from sqlalchemy import select
from database import engine
from models import users, skills, courses, user_skills


with engine.begin() as conn:

  

    sample_users = ["Tala", "Ahmad", "Sara"]

    existing_users = conn.execute(
        select(users.c.name)
    ).scalars().all()

    for name in sample_users:
        if name not in existing_users:
            conn.execute(
                users.insert().values(name=name)
            )



    sample_skills = [
        "Python",
        "SQL",
        "Machine Learning",
        "Data Analysis",
    ]

    existing_skills = conn.execute(
        select(skills.c.skill_name)
    ).scalars().all()

    for skill_name in sample_skills:
        if skill_name not in existing_skills:
            conn.execute(
                skills.insert().values(
                    skill_name=skill_name
                )
            )


   

    sample_courses = [
        {
            "course_name": "Python for Data Science",
            "description": "Learn Python for data analysis and data science",
        },
        {
            "course_name": "SQL and Databases",
            "description": "Learn SQL and database management",
        },
        {
            "course_name": "Machine Learning Foundations",
            "description": "Learn machine learning algorithms and AI",
        },
        {
            "course_name": "Backend Development",
            "description": "Learn backend development and API development",
        },
    ]

    existing_courses = conn.execute(
        select(courses.c.course_name)
    ).scalars().all()

    for course in sample_courses:
        if course["course_name"] not in existing_courses:
            conn.execute(
                courses.insert().values(
                    course_name=course["course_name"],
                    description=course["description"],
                )
            )


   

    user_rows = conn.execute(
        select(users)
    ).fetchall()

    skill_rows = conn.execute(
        select(skills)
    ).fetchall()

    user_map = {
        row.name: row.id
        for row in user_rows
    }

    skill_map = {
        row.skill_name: row.id
        for row in skill_rows
    }


    

    tala_skills = [
        "Python",
        "SQL",
        "Machine Learning",
    ]

    for skill_name in tala_skills:

        user_id = user_map["Tala"]
        skill_id = skill_map[skill_name]

        existing_relation = conn.execute(
            select(user_skills).where(
                user_skills.c.user_id == user_id,
                user_skills.c.skill_id == skill_id,
            )
        ).first()

        if existing_relation is None:
            conn.execute(
                user_skills.insert().values(
                    user_id=user_id,
                    skill_id=skill_id,
                )
            )


print("Sample data inserted successfully!")