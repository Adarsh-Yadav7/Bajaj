import requests

url_generate_webhook = 'https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON'
data = {
    "name": "Adarsh Yadav",
    "regNo": "0827CS221016",
    "email": "adarshyadav220475@acropolis.in"
}

response = requests.post(url_generate_webhook, json=data)
response.raise_for_status()  # This will raise an error if the response status is not 2xx
response_data = response.json()

webhook_url = response_data.get("webhook")
access_token = response_data.get("accessToken")

if not webhook_url or not access_token:
    print("Error: Webhook URL or Access Token missing.")
    exit(1)

print("Webhook URL:", webhook_url)
print("Access Token:", access_token)

reg_no_last_digit = int(data["regNo"][-1])
question_url = "https://drive.google.com/file/d/1q8F8g0EpyNzd5BWk-voe5CKbsxoskJWY/view?usp=sharing" if reg_no_last_digit % 2 == 1 else "https://drive.google.com/file/d/1PO1ZvmDqAZJv77XRYsVben11Wp2HVb/view?usp=sharing"

print("SQL Question URL:", question_url)


sql_query = """SELECT 
    p.AMOUNT AS SALARY,
    CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
    FLOOR(DATEDIFF(CURDATE(), e.DOB) / 365) AS AGE,
    d.DEPARTMENT_NAME
FROM 
    PAYMENTS p
JOIN 
    EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN 
    DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE 
    DAY(p.PAYMENT_TIME) != 1
ORDER BY 
    p.AMOUNT DESC
LIMIT 1;"""  

url_submit_query = 'https://bfhldevapigw.healthrx.co.in/hiring/testWebhook/PYTHON'
headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}

submission_data = {
    "finalQuery": sql_query
}

response_submit = requests.post(url_submit_query, headers=headers, json=submission_data)
response_submit.raise_for_status()  
print("Submission Response:", response_submit.text)
