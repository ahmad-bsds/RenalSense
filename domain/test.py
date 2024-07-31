from domain.user_functions import add_data_or_usr, produce_prompt_inference
from domain.prompt_embed import prompt_encode
from infrastructure.vector_db import qdrant_client
from infrastructure.vector_db import query_collection

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
Note: This is a hypothetical medical report and does not constitute actual medical advice. Please consult with a healthcare professional for any medical concerns.

Would you like to add any specific conditions or symptoms to the report?
"""
prompt = "technology"
USER_ID = "040"

# print("....................Start")
# add_data_or_usr(user_id=USER_ID, data=data)
print("................................Done 1/2")
srh_r = query_collection(user_id=USER_ID, prompt=prompt)

print(srh_r[0].metadata['document'])
