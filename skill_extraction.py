from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_skills(user_text):

    prompt = f"""
    Extract only the technical skills from the following text.

    Text:
    {user_text}

    Return the skills as a comma-separated list.
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output_text
def skill_extraction_agent(user_text):
    skills = extract_skills(user_text)
    skills = validate_skills(skills)

    return {
        "agent": "Skill Extraction Agent",
        "input": user_text,
        "skills": skills
    }

def skill_extraction_agent(user_text):
    skills = extract_skills(user_text)
    skills= validate_skills(skilla)

    return {
        "agent": "Skill Extraction Agent",
        "input": user_text,
        "skills": skills
    }

if __name__ == "__main__":
    user_input = input("Enter your skills or experience: ")

    result = skill_extraction_agent(user_input)

    print(result)