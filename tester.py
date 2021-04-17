import requests
from geopy.geocoders import Nominatim
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

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
        data["range"] = 10
        response = requests.post(url + "/student_signup", data)
        print(response.json())
    if command[0] == "mentorsignup":
        data["username"] = command[1]
        data["password"] = command[2]
        data["age"] = command[3]
        data["address"] = command[4]
        data["lat"] = command[5]
        data["long"] = command[6]
        response = requests.post(url + "/mentor_signup", data)
        print(response.json())
    if command[0] == "orgsignup":
        data["name"] = command[1]
        data["username"] = command[2]
        data["password"] = command[3]
        data["lat"] = command[4]
        data["long"] = command[5]
        response = requests.post(url + "/org_signup", data)
        print(response.json())
    if command[0] == "updateuser":
        data["username"] = command[1]
        data["password"] = command[2]
        data["highschool"] = command[3]
        data["yearlevel"] = command[4]
        data["address"] = command[5]
        data["startdate"] = command[6] + " " + command[7]
        data["enddate"] = command[8] + " " + command[9]
        data["suburb"] = command[10]
        response = requests.post(url + "/update_user", data)
        print(response.json())
    if command[0] == "calendar":
        data["username"] = command[1]
        response = requests.post(url + "/calendar", data)
        print(response.json())