import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print(f"Testing Enterprise Features at {BASE_URL}...")
    
    # 1. Login (Check Org Aware)
    print("\n[TEST] /login (Org Aware)")
    try:
        resp = requests.post(f"{BASE_URL}/login", json={"username": "admin", "password": "admin"})
        if resp.status_code == 200:
            token = resp.json().get("token")
            # In a real test we'd decode JWT, but here we just check if we got one.
            print(f"[OK] Admin Login success. Token: {token[:10]}...")
        else:
            print(f"[FAIL] Admin Login failed: {resp.status_code} {resp.text}")
            sys.exit(1)
    except Exception as e:
        print(f"[FAIL] Connection failed: {e}")
        sys.exit(1)

    # 2. Email Report
    print("\n[TEST] /email-report")
    try:
        resp = requests.post(f"{BASE_URL}/email-report", json={"email": "test@test.com", "content": "Test Insight content"})
        if resp.status_code == 200:
            print(f"[OK] Email sent status: {resp.json()}")
        else:
            print(f"[FAIL] Email failed: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"[FAIL] Email error: {e}")

if __name__ == "__main__":
    run_tests()
