import ollama
from fastapi import HTTPException


def generate_answer(context: str, question: str) -> str:

    prompt = f"""
You are an AI assistant.

Use the context below to answer the user's question.

Context:
{context}

Question:
{question}

Instructions:
- Answer only from the context.
- Give a short and clear answer.
- If the context does not contain the answer, say:
"I couldn't find the answer in the provided content."

Answer:
"""

    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": "You answer questions using only the given context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0
            }
        )

        return response["message"]["content"].strip()

    except ollama.ResponseError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Ollama error: {str(e)}"
        )

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to generate an answer. Please make sure Ollama is running."
        )


def generate_title(content: str) -> str:

    prompt = f"""
Generate a short title (maximum 8 words) for the following content.

Return ONLY the title.

Content:
{content[:3000]}
"""

    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0
            }
        )

        return response["message"]["content"].strip()

    except Exception:
        return "Untitled"


def generate_summary(content: str) -> str:

    prompt = f"""
Summarize the following content.

Rules:
- Maximum 2 sentences.
- Easy to understand.
- Do not add extra information.
- Return only the summary.

Content:
{content[:5000]}
"""

    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0
            }
        )

        return response["message"]["content"].strip()

    except Exception:
        return content[:200]