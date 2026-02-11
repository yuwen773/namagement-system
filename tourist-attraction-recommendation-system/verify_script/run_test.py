import requests
import time

BASE = "http://localhost:8000/api"
tokens = {}
results = []
user1_id = None
notif_id = None
announce_id = None

def req(m, e, token=None, data=None):
    h = {"Content-Type": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    u = f"{BASE}{e}"
    try:
        if m == "GET":
            r = requests.get(u, headers=h, timeout=10)
        elif m == "POST":
            r = requests.post(u, headers=h, json=data, timeout=10)
        elif m == "PUT":
            r = requests.put(u, headers=h, json=data, timeout=10)
        elif m == "DELETE":
            r = requests.delete(u, headers=h, timeout=10)
        return r.status_code < 400, r.json() if r.text else {}
    except Exception as ex:
        return False, {"error": str(ex)}

def test(name, ok, msg=""):
    s = "PASS" if ok else "FAIL"
    print(f"{s}: {name} {msg}")
    results.append((name, ok))

def sec(name):
    print("\n" + "="*60)
    print(name)
    print("="*60)

sec("Notifications API Test Suite")

sec("Step 1: Create Test Users")
req("POST", "/accounts/register/", data={"username": "test_admin", "password": "admin123", "real_name": "Test Admin"})
req("POST", "/accounts/register/", data={"username": "test_user1", "password": "user123", "real_name": "Test User 1"})
req("POST", "/accounts/register/", data={"username": "test_user2", "password": "user123", "real_name": "Test User 2"})

sec("Step 2: User Login")
s, r = req("POST", "/accounts/login/", data={"username": "test_admin", "password": "admin123"})
if s and r.get("code") == 0:
    tokens["admin"] = r["data"]["access_token"]
    test("Admin login", True)
else:
    test("Admin login", False, str(r))

s, r = req("POST", "/accounts/login/", data={"username": "test_user1", "password": "user123"})
if s and r.get("code") == 0:
    tokens["user1"] = r["data"]["access_token"]
    user1_id = r["data"].get("user", {}).get("id")
    test("User1 login", True)
else:
    test("User1 login", False, str(r))

s, r = req("POST", "/accounts/login/", data={"username": "test_user2", "password": "user123"})
if s and r.get("code") == 0:
    tokens["user2"] = r["data"]["access_token"]
    test("User2 login", True)
else:
    test("User2 login", False, str(r))

sec("Step 3: Get Notifications (Initial)")
s, r = req("GET", "/notifications/", token=tokens["admin"])
test("Get notifications list", s and r.get("code") == 0, f"total={r.get('total', 0)}, unread={r.get('unread_count', 0)}")

sec("Step 4: Create User Notification")
s, r = req("POST", "/notifications/", token=tokens["admin"], data={"title": "Welcome", "content": "Test", "type": "SYSTEM", "user": user1_id})
if s:
    notif_id = r.get("id")
    test("Create user notification", True, f"ID={notif_id}")
else:
    test("Create user notification", False, str(r))

sec("Step 5: Create Announcement")
s, r = req("POST", "/notifications/announcement/", token=tokens["admin"], data={"title": "Maintenance", "content": "Test", "type": "ANNOUNCEMENT"})
if s:
    announce_id = r.get("id")
    test("Create announcement", True, f"ID={announce_id}")
else:
    test("Create announcement", False, str(r))

sec("Step 6: User Cannot Post Announcement")
s, r = req("POST", "/notifications/announcement/", token=tokens["user1"], data={"title": "Test", "content": "Test", "type": "ANNOUNCEMENT"})
test("User blocked from announcement", not s or r.get("code") == -1)

sec("Step 7: User1 Get Notifications")
s, r = req("GET", "/notifications/", token=tokens["user1"])
test("User1 get notifications", s and r.get("code") == 0, f"total={r.get('total', 0)}, unread={r.get('unread_count', 0)}")

sec("Step 8: User2 Get Notifications (Should Only See Announcements)")
s, r = req("GET", "/notifications/", token=tokens["user2"])
test("User2 get notifications", s and r.get("code") == 0, f"total={r.get('total', 0)}")
has_only = all(n.get('type') == 'ANNOUNCEMENT' for n in r.get('data', [])) if r.get('data') else True
test("User2 only sees announcements", has_only)

sec("Step 9: Admin Get All Notifications")
s, r = req("GET", "/notifications/", token=tokens["admin"])
test("Admin get all notifications", s and r.get("code") == 0, f"total={r.get('total', 0)}")

sec("Step 10: Mark Single Notification Read")
if notif_id:
    s, r = req("POST", "/notifications/mark_read/", token=tokens["user1"], data={"id": notif_id})
    test("Mark single notification read", s and r.get("code") == 0)
else:
    test("Mark single notification read", False, "No ID")

sec("Step 11: Mark All Notifications Read")
s, r = req("POST", "/notifications/mark_read/", token=tokens["user1"], data={})
test("Mark all notifications read", s and r.get("code") == 0)

sec("Step 12: Get Notification Detail")
if announce_id:
    s, r = req("GET", f"/notifications/{announce_id}/", token=tokens["user1"])
    test("Get notification detail", s and r.get("code") == 0)
else:
    test("Get notification detail", False, "No ID")

sec("Step 13: Update Notification")
if announce_id:
    s, r = req("PUT", f"/notifications/{announce_id}/", token=tokens["admin"], data={"title": "Updated", "content": "Updated", "type": "ANNOUNCEMENT"})
    test("Update notification", s and r.get("code") == 0)
else:
    test("Update notification", False, "No ID")

sec("Step 14: Create Comment Notification")
s, r = req("POST", "/notifications/", token=tokens["admin"], data={"title": "Comment", "content": "Test", "type": "COMMENT", "user": user1_id})
test("Create comment notification", s and r.get("code") == 0)

sec("Step 15: Unauthorized Access")
s, r = req("GET", "/notifications/")
test("Unauthorized access blocked", not s)

sec("Step 16: Delete Notification")
if notif_id:
    s, r = req("DELETE", f"/notifications/{notif_id}/", token=tokens["admin"])
    test("Delete notification", s and r.get("code") == 0)
else:
    test("Delete notification", False, "No ID")

sec("Step 17: Performance Test")
t0 = time.time()
s, r = req("GET", "/notifications/", token=tokens["user1"])
ms = (time.time() - t0) * 1000
test("GET /notifications/ performance", s and r.get("code") == 0, f"{ms:.2f}ms")

sec("Step 18: Announcement Visibility")
for user in ["user1", "user2", "admin"]:
    s, r = req("GET", "/notifications/", token=tokens[user])
    has = any(n.get('type') == 'ANNOUNCEMENT' for n in r.get('data', [])) if s and r.get('data') else False
    test(f"{user} sees announcement", has)

sec("Summary")
total = len(results)
passed = sum(1 for _, p in results if p)
failed = total - passed
print(f"\nTotal Tests: {total}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Pass Rate: {(passed/total*100):.1f}%")
print("\nDetailed Results:")
for name, p in results:
    status = "PASS" if p else "FAIL"
    print(f"  {status} - {name}")
