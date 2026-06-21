import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("Gemini_api_key"))

model = genai.GenerativeModel("gemini-2.5-flash")

role = input("Enter target job role: ")

history = []

print("\nAI Interviewer Started")
print("Type 'finish' anytime to end the interview.\n")

prompt = f"""
You are a professional interviewer.

Conduct an interview for the role: {role}

Ask only ONE interview question.

Do not give explanations.
Do not number questions.
"""

response = model.generate_content(prompt)

question = response.text.strip()

while True:

    print("\nInterviewer:", question)

    answer = input("You: ")

    if answer.lower() == "finish":
        break

    history.append({
        "question": question,
        "answer": answer
    })

    
    with open("interview_data.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

    prompt = f"""
You are a professional interviewer.

Role:
{role}

Interview history:
{history}

Based on the candidate's previous answers:

1. Analyze responses internally.
2. Ask ONE relevant follow-up interview question.
3. Adapt to the candidate's skills.
4. Do NOT provide feedback.
5. Do NOT ask multiple questions.

Return only the next question.
"""

    response = model.generate_content(prompt)

    question = response.text.strip()


print("\nGenerating report...\n")

report_prompt = f"""
You are a senior HR interviewer.

Role:
{role}

Interview transcript:
{history}

Generate a professional report containing:

1. Candidate Summary
2. Technical Knowledge
3. Communication Skills
4. Confidence Level
5. Strengths
6. Weaknesses
7. Areas for Improvement
8. Recommended Roles
9. Overall Score out of 10
10. Hiring Recommendation

Format it professionally.
"""

report = model.generate_content(report_prompt)

print(report.text)


with open("report.txt", "w", encoding="utf-8") as f:
    f.write(report.text)

print("\nReport saved to report.txt")