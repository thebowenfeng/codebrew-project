import requests
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="codebrew_project")

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
    if command[0] == "locate":
        location = geolocator.reverse(f"{command[1]} , {command[2]}")
        print(location.raw["address"]["suburb"])
        print(location.raw["address"]["postcode"])
    if command[0] == "studentsignup":
        data["username"] = command[1]
        data["password"] = command[2]
        data["highschool"] = command[3]
        data["yearlevel"] = command[4]
        data["lat"] = command[5]
        data["long"] = command[6]
        response = requests.post(url + "/student_signup", data)
        print(response.json())
