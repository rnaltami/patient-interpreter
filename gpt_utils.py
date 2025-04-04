import openai

def rewrite_symptoms(user_input, api_key):
    client = openai.OpenAI(api_key=api_key)

    prompt = f"""
Rephrase the following notes using clear, structured medical language in the first person.
Patient note:
\"\"\"{user_input}\"\"\"

Rewritten version (first-person, clinical tone):
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You rewrite patient symptom notes using clinical terminology and structured first-person summaries for doctor visits."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()


def suggest_follow_up_questions(user_input, api_key):
    client = openai.OpenAI(api_key=api_key)

    prompt = f"""
A patient has written the following description of their symptoms:

\"\"\"{user_input}\"\"\"

Based on this, generate 3 to 5 thoughtful follow-up questions they could ask their doctor during an appointment.

The questions should be written in the patient’s voice — first-person, curious, and respectful — but reflect a clear understanding of their symptoms. Use medically relevant language when appropriate, and focus on helping the patient advocate for further investigation, clarification, or next steps.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You help patients prepare intelligent, medically relevant follow-up questions for their doctors."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.65,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()
