import requests

try:
    response = requests.post("http://127.0.0.1:8000/generate-reports")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    if response.status_code == 200:
        print(f"JSON: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
