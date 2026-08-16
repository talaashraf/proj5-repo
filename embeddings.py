from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(texts):
    """
    Convert a list of texts into embeddings.
    """
    embeddings = model.encode(texts)
    return embeddings


def build_user_vector(skills):
    """
    Convert user skills into embeddings
    and combine them into one user profile vector.
    """

    skill_embeddings = generate_embeddings(skills)

    user_vector = np.mean(
        skill_embeddings,
        axis=0
    )

    return user_vector


def generate_course_embeddings(course_descriptions):
    """
    Convert course descriptions into embeddings.
    """

    course_embeddings = generate_embeddings(
        course_descriptions
    )

    return course_embeddings


def compute_similarity(
    user_vector,
    course_embeddings
):
    """
    Compare the user vector with all course embeddings
    using cosine similarity.
    """

    similarities = cosine_similarity(
        [user_vector],
        course_embeddings
    )[0]

    return similarities
