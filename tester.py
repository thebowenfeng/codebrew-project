import requests

url = "http://127.0.0.1:5000"

while True:
    command = input().split()
    data = {}
    if command[0] == "userlogin":
        data["username"] = command[1]
        data["password"] = command[2]
        response = requests.post(url + "/user_login", data)
        print(response.json())
    if command[0] == "orglogin":
        data["username"] = command[1]
        data["password"] = command[2]
        response = requests.post(url + "/org_login", data)
        print(response.json())
