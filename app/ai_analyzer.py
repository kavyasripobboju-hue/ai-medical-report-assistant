import os
from google import genai


def analyze_medical_report(report_text):

    key = os.getenv("GEMINI_API_KEY")

    print("Key exists:", key is not None)
    print("Key length:", len(key) if key else 0)

    client = genai.Client(api_key=key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
You are an AI Medical Report Assistant.

Analyze the following medical report.

Explain it in simple English.
Mention abnormal values if present.
Give a short summary.
Always remind the user to consult a doctor because this is not a medical diagnosis.

Medical Report:

{report_text}
"""
    )

    return response.text