# codebrew-project

### Database relational structure

##### Users 

- suburb (A singular ```Suburbs``` Object)
- suburb_id (ID of the user's suburb)
- attended (A list of ```Events``` object)

##### Organisation

- suburb (A singular ```Suburbs``` Object)
- suburb_id (ID of the user's suburb)
- events (A list of ```Events``` objects.)

##### Events

- organisation (A singular ```Organisation``` object)
- org_id (ID of the event's org)
- attendees (A list of ```Users``` object)

##### Suburbs

- users (A list of ```Users``` object)
- orgs (A list of ```Organisation``` objects)

## Logging in

### Users: 

**URL** = ```http://host_url/user_login``` **Method** = POST

**Request format**: JSON object with fields ```username``` and ```password```. Both fields should be 
strings.

**Example**: ```{username: "test", password: "test"}```

**Response format** JSON object with field ```status```. Will either be ```"success"``` or
```"failure"``` depending on if the credentials are correct

**Example**: ```{status: "success"}```

All other request methods (such as GET) will return a plaintext error message.

### Organisations:

**URL** = ```http://host_url/org_login``` **Method** = POST

Request and Response format same as **Users**. Refer to above.

## Signing up

### Students:

**URL** = `http://host_url/student_signup` **Method** = POST

**Request format**: JSON object with fields:

- `username`: Username
- `password`: Password
- `highschool`: Which high school they were in
- `yearlevel`: Which year level, **must be digit(s)**
- `lat`: Latitude of the current location of the user
- `longitude`: Longitude of the current location of the user

**Example**: `{username: "admin", password="admin", highschool:"example_hs", yearlevel:10, lat:-36.926079, long:174.727066}`

**Response format**: A success response will be: `{status:"success"}`. Failure conditions:

- Empty username or empty password fields. `status` will be `"failure"` and `error` will be `"Empty fields"`
- The username is already registered. `status` will be `"failure"` and `error` will be `"Duplicate username"`
- An invalid longitude and latitude. `status` will be `"failure"` and `error` will be `"Invalid location"`

**Example**: 

- `{username: "admin", password="admin", highschool:"example_hs", yearlevel:10, lat:-36.926079, long:174.727066}`
will result in `{status: "success"}`
  
- `{username: "", password="admin", highschool:"example_hs", yearlevel:10, lat:-36.926079, long:174.727066}`
will result in `{status: "failure" error:"Empty fields"}`
  
- `{username: "admin", password="admin", highschool:"example_hs", yearlevel:10, lat:12345, long:67890abc}`
will result in `{status: "failure" error:"Invalid location"}`
  
Make sure the longtitude and latitude is stored correctly in `long` and `lat` respsectively. 
Mixing the 2 up will result in an incorrect suburb being assigned to the user.




