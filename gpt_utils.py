import openai

def rewrite_symptoms(user_input, api_key):
    client = openai.OpenAI(api_key=api_key)

    prompt = f"""
You are a helpful assistant who helps patients prepare to talk to their doctor by organizing their thoughts into a clear summary.

The patient wrote:
\"\"\"{user_input}\"\"\"

Rewrite this so it sounds like a well-prepared patient describing their concerns calmly and clearly to a doctor. Use plain, natural language — but feel free to include appropriate medical phrasing if it helps the doctor understand. Prioritize clarity and structure over formality.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You help patients prepare for doctor visits by organizing their concerns into a calm, clear, slightly medical summary from the patient's perspective."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=250
    )

    return response.choices[0].message.content.strip()


def suggest_follow_up_questions(user_input, api_key):
    client = openai.OpenAI(api_key=api_key)

    prompt = f"""
A patient has described the following symptoms to you:

\"\"\"{user_input}\"\"\"

Based on these symptoms, suggest 3–5 helpful follow-up questions the patient could ask their doctor. Phrase them clearly, like a curious patient—not too technical.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant helping patients prepare for medical visits."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=200
    )

    return response.choices[0].message.content.strip()
