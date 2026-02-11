import requests
import time

BASE = "http://localhost:8000/api"
tokens = {}
results = []

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

print("="*60)
print("Final Integration Test Suite")
print("="*60)

print("\n" + "="*60)
print("Step 1: User Login (using existing users)")
print("="*60)
s, r = req("POST", "/accounts/login/", data={"username": "admin", "password": "admin123"})
if s and r.get("code") == 0:
    tokens["admin"] = r["data"]["access_token"]
    test("Admin login", True)
else:
    test("Admin login", False, str(r))

s, r = req("POST", "/accounts/login/", data={"username": "user1", "password": "user123"})
if s and r.get("code") == 0:
    tokens["user1"] = r["data"]["access_token"]
    user1_id = r["data"].get("user", {}).get("id")
    test("User1 login", True)
else:
    req("POST", "/accounts/register/", data={"username": "user1", "password": "user123", "password_confirm": "user123", "real_name": "User1"})
    s, r = req("POST", "/accounts/login/", data={"username": "user1", "password": "user123"})
    if s and r.get("code") == 0:
        tokens["user1"] = r["data"]["access_token"]
        user1_id = r["data"].get("user", {}).get("id")
        test("User1 login (created)", True)
    else:
        test("User1 login", False)
        user1_id = None

s, r = req("POST", "/accounts/login/", data={"username": "user2", "password": "user123"})
if s and r.get("code") == 0:
    tokens["user2"] = r["data"]["access_token"]
    test("User2 login", True)
else:
    req("POST", "/accounts/register/", data={"username": "user2", "password": "user123", "password_confirm": "user123", "real_name": "User2"})
    s, r = req("POST", "/accounts/login/", data={"username": "user2", "password": "user123"})
    if s and r.get("code") == 0:
        tokens["user2"] = r["data"]["access_token"]
        test("User2 login (created)", True)
    else:
        test("User2 login", False)

print("\n" + "="*60)
print("Step 2: Get Notifications (Initial)")
print("="*60)
s, r = req("GET", "/notifications/", token=tokens["admin"])
test("Get notifications list", s and r.get("code") == 0, f"total={r.get('total', 0)}, unread={r.get('unread_count', 0)}")

print("\n" + "="*60)
print("Step 3: Create User Notification")
print("="*60)
s, r = req("POST", "/notifications/", token=tokens["admin"], data={"title": "Welcome", "content": "Test", "type": "SYSTEM", "user": user1_id})
if s:
    notif_id = r.get("id")
    test("Create user notification", True, f"ID={notif_id}")
else:
    test("Create user notification", False, str(r))
    notif_id = None

print("\n" + "="*60)
print("Step 4: Create Announcement")
print("="*60)
s, r = req("POST", "/notifications/announcement/", token=tokens["admin"], data={"title": "Maintenance", "content": "Test", "type": "ANNOUNCEMENT"})
if s:
    announce_id = r.get("id")
    test("Create announcement", True, f"ID={announce_id}")
else:
    test("Create announcement", False, str(r))
    announce_id = None

print("\n" + "="*60)
print("Step 5: User Cannot Post Announcement")
print("="*60)
s, r = req("POST", "/notifications/announcement/", token=tokens["user1"], data={"title": "Test", "content": "Test", "type": "ANNOUNCEMENT"})
test("User blocked", not s or r.get("code") == -1)

print("\n" + "="*60)
print("Step 6: User1 Get Notifications")
print("="*60)
s, r = req("GET", "/notifications/", token=tokens["user1"])
test("User1 get notifications", s and r.get("code") == 0, f"total={r.get('total', 0)}, unread={r.get('unread_count', 0)}")

print("\n" + "="*60)
print("Step 7: User2 Get Notifications")
print("="*60)
s, r = req("GET", "/notifications/", token=tokens["user2"])
test("User2 get notifications", s and r.get("code") == 0)
has_only = all(n.get('type') == 'ANNOUNCEMENT' for n in r.get('data', [])) if r.get('data') else True
test("User2 only sees announcements", has_only)

print("\n" + "="*60)
print("Step 8: Admin Get All")
print("="*60)
s, r = req("GET", "/notifications/", token=tokens["admin"])
test("Admin get all", s and r.get("code") == 0)

print("\n" + "="*60)
print("Step 9: Mark Single Read")
print("="*60)
if notif_id:
    s, r = req("POST", "/notifications/mark_read/", token=tokens["user1"], data={"id": notif_id})
    test("Mark single read", s and r.get("code") == 0)
else:
    test("Mark single read", False, "No ID")

print("\n" + "="*60)
print("Step 10: Mark All Read")
print("="*60)
s, r = req("POST", "/notifications/mark_read/", token=tokens["user1"], data={})
test("Mark all read", s and r.get("code") == 0)

print("\n" + "="*60)
print("Step 11: Get Detail")
print("="*60)
if announce_id:
    s, r = req("GET", f"/notifications/{announce_id}/", token=tokens["user1"])
    test("Get detail", s and r.get("code") == 0)
else:
    test("Get detail", False, "No ID")

print("\n" + "="*60)
print("Step 12: Update")
print("="*60)
if announce_id:
    s, r = req("PUT", f"/notifications/{announce_id}/", token=tokens["admin"], data={"title": "Updated", "content": "Updated", "type": "ANNOUNCEMENT"})
    test("Update notification", s and r.get("code") == 0)
else:
    test("Update notification", False, "No ID")

print("\n" + "="*60)
print("Step 13: Create Comment")
print("="*60)
s, r = req("POST", "/notifications/", token=tokens["admin"], data={"title": "Comment", "content": "Test", "type": "COMMENT", "user": user1_id})
test("Create comment notification", s and r.get("code") == 0)

print("\n" + "="*60)
print("Step 14: Unauthorized Access")
print("="*60)
s, r = req("GET", "/notifications/")
test("Unauthorized blocked", not s)

print("\n" + "="*60)
print("Step 15: Delete")
print("="*60)
if notif_id:
    s, r = req("DELETE", f"/notifications/{notif_id}/", token=tokens["admin"])
    test("Delete notification", s and r.get("code") == 0)
else:
    test("Delete notification", False, "No ID")

print("\n" + "="*60)
print("Step 16: Performance")
print("="*60)
t0 = time.time()
s, r = req("GET", "/notifications/", token=tokens["user1"])
ms = (time.time() - t0) * 1000
test("Performance", s and r.get("code") == 0, f"{ms:.2f}ms")

print("\n" + "="*60)
print("Step 17: Announcement Visibility")
print("="*60)
for user in ["user1", "user2", "admin"]:
    s, r = req("GET", "/notifications/", token=tokens[user])
    has = any(n.get('type') == 'ANNOUNCEMENT' for n in r.get('data', [])) if s and r.get('data') else False
    test(f"{user} sees announcement", has)

print("\n" + "="*60)
print("Summary")
print("="*60)
total = len(results)
passed = sum(1 for _, p in results if p)
failed = total - passed
print(f"\nTotal: {total}, Passed: {passed}, Failed: {failed}")
print(f"Pass Rate: {(passed/total*100):.1f}%")
for name, p in results:
    print(f"  {"PASS" if p else "FAIL"} - {name}")
