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

**Response format** JSON object with the following fields:

- ```status```. Will either be ```"success"``` or
```"failure"``` depending on if the credentials are correct
  
- `postcode`: User's postcode 
- `suburb`: User's suburb
- `type`: User's account type (student/mentor)
- `username`: User's username
- `password`: User's password
- `range`: User's range

**IF `type` = ```"student"```**
- `high_school`: Student's High school
- `year_level`: Student's year level

**IF `type` = ```"mentor"```**
- `address`: Mentor's address
- `age`: Mentor's age

**Example**: ```{'postcode': 3053, 'status': 'success', 'suburb': 'Carlton', 'type': 'test', 'username': 'test', 'password': 'test', 'high_school': 'test', 'year_level': 12}```

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
- `range`: Range (in km) that the user is willing to volunteer from his Suburb

**Example**: `{username: "admin", password="admin", highschool:"example_hs", yearlevel:10, lat:-36.926079, long:174.727066, range:10}`

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

### Mentors

**URL** = `http://host_url/mentor_signup` **Method** = POST

**Request format**: JSON object with fields:

- `username`: Username
- `password`: Password
- `age`: Their age **must be digit(s)**
- `address`: Their address
- `lat`: Latitude of the current location of the user
- `longitude`: Longitude of the current location of the user
- `range`: Range (in km) that the user is willing to volunteer from his Suburb

**Example** `{username: "admin", password="admin", age:21, address:"10 abc St XYZ", lat:-36.926079, long:174.727066, range:10}`

**Response format** Exact same as student signup. Same failure conditions, please refer to above.

Mentor signup and student signup works in very similar fashion, just different URLs.

### Organisations

**URL** = `http://host_url/org_signup` **Method** = POST

**Request format**: JSON object with fields:

- `name`: Name of the business
- `username`: Username
- `password`: Password
- `lat`: Latitude of the current location of the user
- `longitude`: Longitude of the current location of the user

**Example** `{name: "businessA", username: "admin", password="admin", lat:-36.926079, long:174.727066, isEvent:False}`

**Response format** Exact same as student/mentor signup. Same failure conditions, please refer to above.

Organisation signup and student signup works in very similar fashion, just different URLs.

## Creating an Event

**URL** = `http://host_url/create_event` **Method** = POST

**Request format**: JSON object with fields:

- `username`: Username of selected Organisation
- `password`: Password of selected Organisation
- `event_name`: Name of the event
- `event_begin`: DateTime of when the event starts
- `event_end`: **Optional** DateTime of when the event ends
- `address`: Address of the event as just a string
- `description`: Description of the event

**Example** `{username: "admin", password="admin", event_name: "Test", event_begin: 2021-04-17 16:39:56.964868, event_end: 2021-04-17 16:39:56.964868, address: '24 Batman Rd', description: 'Test'}`

**Response format**: A success response will be: `{status:"success"}`. Failure conditions:

- If the organisation is not eligible to host an event. `status` will be `"failure"` and `error` will be `"Organisation is not eligible to create a new event this week"`
- The username and/or password don't match. `status` will be `"failure"` and `error` will be `"Issue with user information"`

## Updating a user profile

**URL** `http://host_url/update_user` **Method** = POST

**Request format**: JSON object with fields:

- `username`
- `password` (Username and password must both be non-empty)
- `address`
- `highschool`
- `yearlevel` Must be digits
- `startdate` This must be in `dd/mm/yy hh:mm:ss` format
- `enddate` This must be in `dd/mm/yy hh:mm:ss` format
- `suburb` This is the name of the suburb
- `postcode` This is the suburb postcode

**Example**: `{username: "test", password:"test", address:"test st", highschool:"test", 
yearlevel:10, startdate:"01/01/21 10:11:12", enddate:"01/02/21 13:14:15", suburb: "Carlton", postcode:3053}`

**Response format**: JSON object with fields:

- `status` Can either be success or failure. Failure will indicate something is wrong
- `error` Will only appear if status is failure. 

**Example** `{'error': "Suburb doesn't exist", 'status': 'failure'}`

## Searching for events

**URL** `http://host_url/search` **Method** = POST

**Request format**: JSON object with fields:

- `address`
- `range` Must be above 0 (in km)

**Example**: `{address: "Melbourne", range: "30"}`

**Response format**: JSON object with fields:

- `status` Either success or failure
- `error` Only when status is failure, always for when address is not valid
- `events` List of all the events that fit the search

## Setting up events for the week

**URL** `http://host_url/set_events` **Method** = POST

**Request format**: JSON object with fields:

- `token` using the correct token to be able to set up the events

**Response format**: JSON object with fields:

- `status` Either success or failure
- `error` Only when status is failure, always for when token isn't valid

## Adding event to Google Calendar

**URL** `http://host_url/calendar` **Method** = POST

**Request format**: JSON object with `username` field. `username` would be the username of
the currently logged in user. 

**Example**: `{username: "test"}`

**Response format**: `url` field which contains a URL the user needs to click. URL is a google login
URL that basically gives my Google App permission to access user's google calendar via Calendar API.
Front end needs to extract that url, and pop it in a new window or something. Once the user has
logged in with the Google URL, their latest event will be automatically added to their calendar.

**Example** `{url: "some_long_ass_url"}`

## Getting an Event

**URL** `http://host_url/get_event` **Method** = POST

**Request format** : JSON Object with `event_id` field

**Example**: `{event_id: 1}`

**Response format** JSON object with the following fields:

- ```status```. Will either be ```"success"``` or
```"failure"``` depending on if the event_id is correct

**IF it is success**

- `event_id` ID of the event
- `org_id` ID of the organisation
- `event_name` Name of the event
- `begin` DateTime of when the event begins
- `end` DateTime of when the event ends (can be ```None```)
- `address` String value of the address of the event
- `description` Description of the event
- `completed` Boolean on whether the event has been completed or not

**Example** `{event_id: 1, org_id: 1, event_name: "Test", begin: :"01/01/21 10:11:12", end: "01/02/21 13:14:15", address: "24 Batman Rd", description: "Test", completed: False}`

## Paypal integration

Simply put the following script (which will generate paypal buttons) into the website

```  <script
    src="https://www.paypal.com/sdk/js?client-id=Ab-TmVOOF38HXqyvqZN8T5pvj_mgN5WYSW2RE7kbwLoFFYqVB18CF7bMrWtZAjp-8IzZnYUsx2VELDBf"> // Required. Replace YOUR_CLIENT_ID with your sandbox client ID.
  </script>
  <script>
    paypal.Buttons({
    createOrder: function(data, actions) {
      // This function sets up the details of the transaction, including the amount and line item details.
      return actions.order.create({
        purchase_units: [{
          amount: {
            value: '100'
          }
        }]
      });
    },
    onApprove: function(data, actions) {
      // This function captures the funds from the transaction.
      return actions.order.capture().then(function(details) {
        // This function shows a transaction success message to your buyer.
        alert('Transaction completed by ' + details.payer.name.given_name);
      });
    }
  }).render('body');
  </script>
```
Currently paypal would only work within a "sandbox environment". Meaning, transactions are tot real
and only dummy accounts can be used. Details of the dummy account (used for demo purposes)

- Email: sb-r4y6p5950974@personal.example.com
- Password: o0zy%Zu9
