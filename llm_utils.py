import os
import requests

API_URL = "https://router.huggingface.co/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
}


def build_message(user_query, context):

    system_prompt = f"""
You are a helpful, factual, and reliable assistant.

Your job is to answer the user's question using ONLY the provided context.

---------------------
RULES:
1. Do NOT use outside knowledge.
2. If the answer is fully present → answer clearly.
3. If the answer is partially present → 
   - Answer what is available
   - Clearly say what is missing
4. If the answer is NOT present → say:
   "Not found in document."
5. Do NOT guess, assume, or hallucinate.
6. Keep answers concise, structured, and easy to read.
7. Prefer bullet points when listing information.
8. If relevant, quote key phrases from context.

---------------------
CONTEXT:
{context}
---------------------
"""

    user_prompt = f"""
Question: {user_query}

Answer:
"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def get_llm_response(user_query, context):
    response = query({
        "messages": build_message(user_query, context),
        "model": "meta-llama/Llama-3.1-8B-Instruct:novita"
    })

    return response["choices"][0]["message"]