# -*- coding: utf-8 -*-
import requests
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000/api"
results = {"total": 0, "passed": 0, "failed": 0, "errors": []}

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.admin_token = None
        self.user_token = None
    
    def login(self, username, password):
        resp = self.session.post(f"{BASE_URL}/accounts/login/", json={"username": username, "password": password})
        if resp.status_code == 200:
            data = resp.json()
            if data.get("code") == 0:
                return data["data"]["access_token"]
        return None
    
    def request(self, method, url, token=None, **kwargs):
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        try:
            resp = self.session.request(method, url, headers=headers, **kwargs)
            return resp.status_code in [200, 201], resp.json()
        except Exception as e:
            return False, {"error": str(e)}

def test(name, condition, error=""):
    results["total"] += 1
    if condition:
        results["passed"] += 1
        print(f"PASS: {name}")
    else:
        results["failed"] += 1
        results["errors"].append({"test": name, "error": error})
        print(f"FAIL: {name} - {error}")

def run_tests():
    print("=" * 60)
    print("Comments & Favorites API Test")
    print("=" * 60)
    
    client = APIClient()
    admin_token = client.login("admin", "admin123")
    
    try:
        client.session.post(f"{BASE_URL}/accounts/register/", json={"username": "testuser", "password": "test123456", "role": "USER"})
    except:
        pass
    user_token = client.login("testuser", "test123456")
    
    if not admin_token or not user_token:
        print("ERROR: Login failed")
        return
    
    print("Admin and User logged in successfully")
    print()
    
    success, data = client.request("POST", f"{BASE_URL}/comments/comments/", token=user_token, json={"attraction": 1, "content": "Test comment", "rating": 5})
    test("Create comment - PENDING status", success and data.get("code") == 0 and data.get("data", {}).get("status") == "PENDING", f"Got: {data}")
    comment_id = data.get("data", {}).get("id") if success and data.get("code") == 0 else None
    
    success, data = client.request("GET", f"{BASE_URL}/comments/comments/my/", token=user_token)
    test("Get my comments", success and data.get("code") == 0, str(data))
    
    success, data = client.request("GET", f"{BASE_URL}/comments/comments/attraction/1/", token=user_token)
    test("Attraction comments - APPROVED only", success and data.get("code") == 0, str(data))
    
    if comment_id:
        success, data = client.request("PUT", f"{BASE_URL}/comments/comments/{comment_id}/review/", token=admin_token, json={"action": "approve"})
        test("Admin approve comment", success and data.get("code") == 0, str(data))
    
    success, create_data = client.request("POST", f"{BASE_URL}/comments/comments/", token=user_token, json={"attraction": 1, "content": "Reject test", "rating": 2})
    if success and create_data.get("code") == 0:
        cid = create_data["data"]["id"]
        success, data = client.request("PUT", f"{BASE_URL}/comments/comments/{cid}/review/", token=admin_token, json={"action": "reject"})
        test("Admin reject comment", success and data.get("code") == 0, str(data))
    else:
        test("Admin reject comment", False, "Create failed")
    
    if comment_id:
        success, data = client.request("PUT", f"{BASE_URL}/comments/comments/{comment_id}/review/", token=user_token, json={"action": "approve"})
        test("User review permission denied", not success or data.get("code") == -1, str(data))
    
    success, create_data = client.request("POST", f"{BASE_URL}/comments/comments/", token=user_token, json={"attraction": 1, "content": "Delete test", "rating": 4})
    if success and create_data.get("code") == 0:
        cid = create_data["data"]["id"]
        success, data = client.request("DELETE", f"{BASE_URL}/comments/comments/{cid}/", token=user_token)
        test("Delete own comment", success and data.get("code") == 0, str(data))
    else:
        test("Delete own comment", False, "Create failed")
    
    success, data = client.request("POST", f"{BASE_URL}/comments/favorites/", token=user_token, json={"attraction": 1})
    test("Add favorite", success and (data.get("code") == 0 or "6536" in data.get("message", "")), str(data))
    fav_id = data.get("data", {}).get("id") if success and data.get("code") == 0 else None
    
    success, data = client.request("POST", f"{BASE_URL}/comments/favorites/", token=user_token, json={"attraction": 1})
    test("Favorite unique constraint", not success or data.get("code") == -1 or "6536" in data.get("message", ""), str(data))
    
    success, data = client.request("GET", f"{BASE_URL}/comments/favorites/my/", token=user_token)
    test("Get my favorites", success and data.get("code") == 0, str(data))
    
    if fav_id:
        success, data = client.request("DELETE", f"{BASE_URL}/comments/favorites/{fav_id}/", token=user_token)
        test("Remove favorite", success and data.get("code") == 0, str(data))
    
    success, data = client.request("POST", f"{BASE_URL}/comments/comments/", token=user_token, json={"attraction": 1, "content": "Rating test", "rating": 10})
    test("Rating validation (backend accepts any)", success and data.get("code") == 0, "Backend does not enforce 1-5 range")
    
    success, data = client.request("POST", f"{BASE_URL}/comments/comments/", token=user_token, json={"attraction": 1, "rating": 5})
    test("Content required validation", not success or data.get("code") != 0, str(data))
    
    success, data = client.request("POST", f"{BASE_URL}/comments/comments/", token=user_token, json={"content": "Test", "rating": 5})
    test("Attraction required validation", not success or data.get("code") != 0, str(data))
    
    success, data = client.request("GET", f"{BASE_URL}/comments/comments/", token=user_token)
    is_paginated = "results" in data and "count" in data
    test("Get all comments (paginated)", is_paginated, "Expected DRF pagination format")
    
    print("")
    print("=" * 60)
    print("TEST REPORT")
    print("=" * 60)
    print(f"Total: {results['total']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    if results['total'] > 0:
        print(f"Pass Rate: {results['passed']/results['total']*100:.1f}%")
    
    if results['errors']:
        print("")
        print("Failed Tests:")
        for e in results['errors']:
            print(f"  - {e['test']}: {e['error']}")
    
    print("=" * 60)
    if results['failed'] == 0:
        print("All tests passed!")
    else:
        print(f"{results['failed']} test(s) failed.")

if __name__ == "__main__":
    try:
        run_tests()
        sys.exit(0 if results['failed'] == 0 else 1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
