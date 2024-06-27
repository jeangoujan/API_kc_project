import requests
import pytest
import allure
import random

URL = "https://demoqa.com"
PASSWORD = "@12Az@12Az"
USERS = ["Damir", "Rimad", "PashaTechnik", "MichaelJordan", "SteveJobs", "SteveBuscemi", "Gargamel", "Baibek",
         "SnoopDogg", "2pac", "Eminem", "YuriyLoza", "User13", "User14", "User15", "User16", "User17", "User18",
         "User19", "User20",
         "User21", "User22", "User23", "User24", "User25", "User26", "User27", "User28", "User29", "User30",
         "User31", "User32", "User33", "User34", "User35", "User36", "User37", "User38", "User39", "User40",
         "User41", "User42", "User43", "User44", "User45", "User46", "User47", "User48", "User49", "User50",
         "User51", "User52", "User53", "User54", "User55", "User56", "User57", "User58", "User59", "User60",
         "User61", "User62", "User63", "User64", "User65", "User66", "User67", "User68", "User69", "User70",
         "User71", "User72", "User73", "User74", "User75", "User76", "User77", "User78", "User79", "User80",
         "User81", "User82", "User83", "User84", "User85", "User86", "User87", "User88", "User89", "User90",
         "User91", "User92", "User93", "User94", "User95", "User96", "User97", "User98", "User99", "User100"
         ]


# Фикстура создания пользователя
@pytest.fixture(scope="module")
def user_data():
    url = f"{URL}/Account/v1/User"
    username = random.choice(USERS)
    payload = {
        "userName": username,
        "password": PASSWORD
    }
    response = requests.post(url, json=payload)

    assert response.status_code == 201
    response_data = response.json()
    return {
        "userID": response_data["userID"],
        "username": username,
        "password": PASSWORD
    }


# Фикстура генерации токена для получения информации о пользователе и удаления пользователя
@pytest.fixture(scope="module")
def auth_token(user_data):
    url = f"{URL}/Account/v1/GenerateToken"
    payload = {
        "userName": user_data["username"],
        "password": user_data["password"]
    }
    response = requests.post(url, json=payload)

    assert response.status_code == 200
    response_data = response.json()
    return response_data["token"]


@allure.title("Создание нового пользователя")
def test_post_create_user():
    url = f"{URL}/Account/v1/User"
    username = random.choice(USERS)
    payload = {
        "userName": username,
        "password": PASSWORD
    }
    response = requests.post(url, json=payload)
    with allure.step("Проверка создания пользователя " + username):
        assert response.status_code == 201
        response_data = response.json()
        assert "userID" in response_data
        assert response_data["username"] == username
        assert response_data["books"] == []
        print(response_data)
        print(username)


@allure.title("Проверка авторизации пользователя")
def test_post_authorized(user_data):
    url = f"{URL}/Account/v1/Authorized"
    payload = {
        "userName": user_data["username"],
        "password": user_data["password"]
    }
    response = requests.post(url, json=payload)
    with allure.step("Проверка успешной авторизации пользователя " + user_data['username']):
        assert response.status_code == 200
        print(response.json())


@allure.title("Генерация токена")
def test_post_generate_token(auth_token):
    with allure.step("Проверка генерации токена"):
        assert auth_token is not None


@allure.title("Получение информации о пользователе")
def test_get_user_information(user_data, auth_token):
    url = f"{URL}/Account/v1/User/{user_data['userID']}"
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.get(url, headers=headers)

    with allure.step("Проверка успешного получения информации о пользователе" + user_data['username']):
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["userId"] == user_data["userID"]
        assert response_data["username"] == user_data["username"]
        assert "books" in response_data


@allure.title("Удаление пользователя")
def test_delete_user(user_data, auth_token):
    url = f"{URL}/Account/v1/User/{user_data['userID']}"
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.delete(url, headers=headers)

    with allure.step(f"Проверка успешного удаления пользователя" + user_data['username']):
        assert response.status_code == 204

