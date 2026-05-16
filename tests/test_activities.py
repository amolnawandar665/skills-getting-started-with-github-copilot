import urllib.parse


def test_get_activities_returns_activities(client):
    # Arrange: fixture-provided client
    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_participant(client):
    # Arrange
    email = "test_student@example.com"
    activity = "Chess Club"

    # Pre-assert (ensure not already signed up)
    resp0 = client.get("/activities")
    assert email not in resp0.json()[activity]["participants"]

    # Act
    url = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    resp = client.post(url)

    # Assert
    assert resp.status_code == 200
    resp2 = client.get("/activities")
    assert email in resp2.json()[activity]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    email = "dup_student@example.com"
    activity = "Chess Club"

    # First signup should succeed
    url = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    r1 = client.post(url)
    assert r1.status_code == 200

    # Act: sign up again
    r2 = client.post(url)

    # Assert
    assert r2.status_code == 400


def test_remove_participant(client):
    # Arrange
    email = "remove_student@example.com"
    activity = "Chess Club"

    # Ensure participant exists by signing up
    signup_url = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    r_signup = client.post(signup_url)
    assert r_signup.status_code == 200

    # Act: remove participant
    del_url = f"/activities/{urllib.parse.quote(activity)}/participants?email={urllib.parse.quote(email)}"
    r_del = client.delete(del_url)

    # Assert
    assert r_del.status_code == 200
    r_after = client.get("/activities")
    assert email not in r_after.json()[activity]["participants"]


def test_remove_nonexistent_returns_404(client):
    # Arrange
    email = "noone@example.com"
    activity = "Chess Club"

    # Ensure not present
    r0 = client.get("/activities")
    assert email not in r0.json()[activity]["participants"]

    # Act
    del_url = f"/activities/{urllib.parse.quote(activity)}/participants?email={urllib.parse.quote(email)}"
    r = client.delete(del_url)

    # Assert
    assert r.status_code == 404
