def test_requires_json(client):
    r = client.post("/v1/survey", data="not json", headers={'Content-type':"text/plain"})
    assert r.status_code == 400 

def test_validation_error(client):
    bad_payload = {"name":"", "email":"not_an_email", "role":"", "languages":[], "proficiencies":{}}
    r = client.post("/v1/survey", json=bad_payload)
    assert r.status_code == 422
    assert r.json["error"] == "validation_error"

def test_validation_error_2(client):
    incomplete_payload = {"name":"Alice", "email":"alice@example.com", "role":"Data Scientist", "languages":["Python","R"], "proficiencies":{"R":"Beginner"}}
    r = client.post("/v1/survey", json=incomplete_payload)
    assert r.status_code == 422
    assert r.json["error"] == "validation_error"

def test_validation_success(client):
    good_payload = {"name":"Alice", "email":"alice@example.com", "role":"Data Scientist", "languages":["Python","R"], "proficiencies":{"Python":"Intermediate","R":"Beginner"}}
    r = client.post("/v1/survey", json=good_payload)
    assert r.status_code == 201

    assert r.json["status"] == "ok"
