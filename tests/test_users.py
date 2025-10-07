# tests/test_users.py
import pytest

def user_payload(uid=1, name="Paul", email="pl@atu.ie", age=25, sid="S1234567"):
 return {"user_id": uid, "name": name, "email": email, "age": age, "student_id": 
sid}

def test_create_user_ok(client):
 r = client.post("/api/users", json=user_payload())
 assert r.status_code == 201
 data = r.json()
 assert data["user_id"] == 1
 assert data["name"] == "Paul"

def test_duplicate_user_id_conflict(client):
 client.post("/api/users", json=user_payload(uid=2))
 r = client.post("/api/users", json=user_payload(uid=2))
 assert r.status_code == 409 # duplicate id -> conflict
 assert "exists" in r.json()["detail"].lower()
@pytest.mark.parametrize("bad_sid", ["BAD123", "s1234567", "S123", "S12345678"])

def test_bad_student_id_422(client, bad_sid):
 r = client.post("/api/users", json=user_payload(uid=3, sid=bad_sid))
 assert r.status_code == 422 # pydantic validation error

def test_get_user_404(client):
 r = client.get("/api/users/999")
 assert r.status_code == 404
 
def test_delete_then_404(client):
 client.post("/api/users", json=user_payload(uid=10))
 r1 = client.delete("/api/users/10")
 assert r1.status_code == 204
 r2 = client.delete("/api/users/10")
 assert r2.status_code == 404

def test_update_user_then_404(client):
    # Creating user with id 11 
    r_create = client.post("/api/users", json=user_payload(uid=11))
    assert r_create.status_code == 201 #check if it was created 

    # ensuring that the user_id in path and body are the same
    updated_user = user_payload(uid=999)  #ignored by endpoint because it's not 11
    updated_user["name"] = "Updated Name"

    #user's name with id 11 is updated
    r1 = client.put("/api/users/11", json=updated_user) 
    assert r1.status_code == 202 #Used 202 because module 'starlette.status' has no attribute 'HTTP_200_SUCCESS'
    data = r1.json()
    assert data["user_id"] == 11
    assert data["name"] == "Updated Name"

    # updating a non-existing user
    r2 = client.put("/api/users/999", json=updated_user)
    assert r2.status_code == 404
 
 
 