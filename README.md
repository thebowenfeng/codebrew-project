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



