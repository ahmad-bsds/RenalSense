from user_functions import produce_prompt_inference

data = """
Patient Information:

Name: John Doe
Date of Birth: 01/01/1980
Medical Record Number: 123456789
Date of Report: 07/31/2024
Reason for Visit:
Routine annual physical examination.

Subjective Complaints:
Patient reports no specific complaints or symptoms.

Objective Findings:

Vital signs: Blood pressure 120/80 mmHg, pulse 72 beats/min, respiratory rate 16 breaths/min, temperature 98.6°F.
Height: 5'10" (178 cm), Weight: 180 lbs (81.6 kg), BMI: 25.5 (overweight).
Head, eyes, ears, nose, and throat (HEENT): Normal.
Neck: Supple without lymphadenopathy.
Chest: Clear to auscultation bilaterally.
Heart: Regular rate and rhythm, no murmurs or gallops.
Abdomen: Soft, non-tender, with normal bowel sounds.
Extremities: No edema or clubbing.
Neurological: Normal strength, sensation, and reflexes.
Diagnostic Tests:

Complete blood count (CBC): Within normal limits.
Basic metabolic panel (BMP): Within normal limits.
Lipid profile: Total cholesterol 220 mg/dL, LDL cholesterol 140 mg/dL, HDL cholesterol 50 mg/dL, triglycerides 150 mg/dL.
Electrocardiogram (ECG): Normal sinus rhythm.
Assessment:
Overall, patient appears in good health for his age. He is overweight and requires lifestyle modifications to improve cardiovascular health. Lipid profile is abnormal and requires further evaluation and management.

Plan:
Recommend diet and exercise to achieve and maintain a healthy weight.
Refer to a cardiologist for further evaluation of lipid profile and to discuss treatment options.
Schedule follow-up appointment in 3 months to monitor progress.
Blood: normal
suger: normal
sleep:normal
"""
prompt = "what will you suggest based on my data?"
USER_ID = "0011"

print(
    produce_prompt_inference(user_id=USER_ID, prompt=prompt)
)
