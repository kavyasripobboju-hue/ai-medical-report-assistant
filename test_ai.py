from app.ai_analyzer import analyze_medical_report

report = """
Hemoglobin: 10.5 g/dL
WBC Count: 8000
Platelets: 250000
"""

result = analyze_medical_report(report)

print(result)