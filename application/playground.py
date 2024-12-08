# TODO: Add memory.
# TODO: Chat always include query response, its not suitable as answer to hi means no match.

data = {'kidney_health': {'risk': 'No', 'recommendations': ['Maintain a healthy diet, including limiting sodium intake.', 'Stay hydrated by drinking plenty of fluids.', 'Exercise regularly to maintain a healthy weight.', 'Avoid smoking and limit alcohol consumption.', 'Monitor blood pressure and seek medical attention if it is consistently high.', 'Follow up with a healthcare provider for regular check-ups and monitoring of kidney health.']}}

data = data['kidney_health']

if 'stage'  not in data:
    data['stage'] = "N/A (Refresh/Data required)"

if 'risk' not in data:
    data['risk'] = "N/A (Refresh/Data required)"

if 'recommendations' not in data:
    data['recommendations'] = ["Hey, Sorry for inconvenience. Data is not available right now. Please try again."]


print(data)



