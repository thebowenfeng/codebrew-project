# codebrew-project

###Database relational structure

#####Users 

- attended (List of events the user has attended)
- suburb (A singular ```Suburbs``` Object)
- suburb_id (ID of the user's suburb)
- attended (A list of ```Events``` object)

#####Organisation

- suburb (A singular ```Suburbs``` Object)
- suburb_id (ID of the user's suburb)
- events (A list of ```Events``` objects.)

#####Events

- organisation (A singular ```Organisation``` object)
- org_id (ID of the event's org)
- attendees (A list of ```Users``` object)

####Suburbs

- users (A list of ```Users``` object)
- orgs (A list of ```Organisation``` objects)
