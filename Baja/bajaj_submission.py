import requests


name = "Adarsh Yadav"  
reg_no = "0827CS221016"       
email = "adarshyadav220475@acropolis.in" 


print(" Generating webhook...")

generate_url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
payload = {
    "name": name,
    "regNo": reg_no,
    "email": email
}

try:
    response = requests.post(generate_url, json=payload)
    response.raise_for_status()
    data = response.json()
    access_token = data['accessToken']
    print("Webhook generated successfully!")
    print("Access Token:", access_token)
except Exception as e:
    print("Error generating webhook:", e)
    exit()

final_sql_query = """
SELECT 
    e1.EMP_ID,
    e1.FIRST_NAME,
    e1.LAST_NAME,
    d.DEPARTMENT_NAME,
    COUNT(e2.EMP_ID) AS YOUNGER_EMPLOYEES_COUNT
FROM EMPLOYEE e1
JOIN DEPARTMENT d ON e1.DEPARTMENT = d.DEPARTMENT_ID
LEFT JOIN EMPLOYEE e2 
    ON e1.DEPARTMENT = e2.DEPARTMENT
    AND e2.DOB > e1.DOB
GROUP BY 
    e1.EMP_ID, e1.FIRST_NAME, e1.LAST_NAME, d.DEPARTMENT_NAME
ORDER BY 
    e1.EMP_ID DESC;
"""


print("Submitting SQL query to testWebhook...")

submit_url = "https://bfhldevapigw.healthrx.co.in/hiring/testWebhook/PYTHON"

headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}

submission_payload = {
    "finalQuery": final_sql_query.strip()
}

try:
    submit_response = requests.post(submit_url, headers=headers, json=submission_payload)
    submit_response.raise_for_status()
    print(" Query submitted successfully!")
    print("Server Response:", submit_response.json())
except Exception as e:
    print("Error submitting SQL query:", e)
