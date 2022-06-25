import json
from fastapi import status


def test_create_article(client, normal_user_token_headers):
    data = {
        "title": "SDE super",
        "description": "python",
        "text": "It is our first lesson!",
        "date_posted": "2022-03-20"
        }
    response = client.post("/articles/create-article/",json.dumps(data), headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["description"] == "python"
    assert response.json()["text"] == "It is our first lesson!"

def test_read_article(client):
    data = {
        "title": "SDE super",
        "description": "python",
        "text": "It is our first lesson!",
        "date_posted": "2022-03-20"
        }
    response = client.post("/articles/create-article/",json.dumps(data))

    response = client.get("/articles/get/1/")
    assert response.status_code == 200
    assert response.json()['title'] == "SDE super"

def test_read_all_articles(client):
    data = {
        "title": "SDE super",
        "description": "python",
        "text": "It is our first lesson!",
        "date_posted": "2022-03-20"
    }
    client.post("/articles/create-article/", json.dumps(data))
    client.post("/articles/create-article/", json.dumps(data))

    response = client.get("/articles/all/")
    assert response.status_code == 200
    assert response.json()[0]
    assert response.json()[1]

def test_update_an_article(client):
    data = {
        "title": "New Article super",
        "description": "fastapi",
        "text": "It is our first ebook!",
        "date_posted": "2022-03-20"
        }
    client.post("/articles/create-article/",json.dumps(data))
    data["title"] = "test new title"
    response = client.put("/articles/update/1",json.dumps(data))
    assert response.json()["msg"] == "Successfully updated data."

def test_delete_an_article(client):
    data = {
        "title": "New Article super",
        "description": "fastapi",
        "text": "It is our first ebook!",
        "date_posted": "2022-03-20"
        }
    client.post("/articles/create-article/",json.dumps(data))
    msg = client.delete("/articles/delete/1")
    response = client.get("/articles/get/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND