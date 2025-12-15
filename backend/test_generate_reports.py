import requests
import json

print("Testing /generate-reports endpoint")
print("=" * 60)

response = requests.post("http://127.0.0.1:8000/generate-reports")
print(f"Status Code: {response.status_code}")
print(f"\nResponse:\n{json.dumps(response.json(), indent=2)}")
