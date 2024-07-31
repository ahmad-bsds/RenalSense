from domain.user_functions import add_new_user_in_app, add_user_data, produce_prompt_inference
from domain.prompt_embed import prompt_encode
from infrastructure.vector_db import search
data = """
Patient Name: John Doe
Date of Birth: 01/01/1980
Date of Report: 01/01/2024

Clinical Indication: Routine check-up

Ultrasound Findings:

Right kidney measures [normal/increased/decreased] in length, width, and thickness.
Left kidney measures [normal/increased/decreased] in length, width, and thickness.
Renal cortex appears [normal/thinned/thickened].
Renal medulla appears [normal/echogenic/hypoechoic].
No evidence of hydronephrosis, calculi, or masses.
Normal blood flow to both kidneys.
Laboratory Results:

Blood Urea Nitrogen (BUN): [normal/elevated/decreased]
Creatinine: [normal/elevated/decreased]
Estimated Glomerular Filtration Rate (eGFR): [normal/reduced]
Urine analysis: [normal/abnormal findings, e.g., proteinuria, hematuria]
Impression:
[Overall assessment of kidney function based on ultrasound and lab results, e.g., normal kidney size and function, mild renal insufficiency, etc.]

Recommendations:
[Follow-up recommendations based on findings, e.g., repeat ultrasound in 6 months, refer to nephrologist for further evaluation, monitor blood pressure, etc.]
"""
prompt = "What is the patient's estimated glomerular filtration rate (eGFR) and what does this indicate about kidney function?"
USER_ID = "013"

# print("Adding new user...................")
# add_new_user_in_app(user_id=USER_ID, data=data)
# print("New user added....................")

embed_prompt = prompt_encode(prompt)

# print("Quring data..................")
# query = produce_prompt_inference(user_id=USER_ID,
#                                  prompt="")
# print(query)

print(search(vect=embed_prompt, c_name=USER_ID))

#TODO: add payload while new user.