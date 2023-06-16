# davent

## Create an event and make it easy for your users to register for your event while being able to get payment for any event to tag as paid

### Project overview
* User types = ["users", "admin"]
* Users sign up on the platform
* Users can do all the authentication stuffs (sign up, log in, log out, reset password etc ...  u get)
* Users can register for an event
* If event is a paid event, users can pay for the event
* Tickets are being generated for users for events they reigstered for
* Users can see events around them, based on the location they said they are in
* Users can see events in different locations depending on their filter params
___
* Admin can create an event
* Admin can send emails to participants of an event to give updates
* Admin can update status of an event
* Admin can view payments for an event if the event is paid for
* Admin can see the list of participant that register for their event

...
___
## How to get started

- Make sure you have Docker installed on your machine
- in whatever directory you'll like to work, run the following commands
```
git clone https://github.com/funsojoba/davent.git`
cd davent
touch .env - to create an env file
make build - this builds your Docker image
make up - this should start your project
```
You might want to configure your `.env` file to suit your prefered configuration, the required `.env` values are provided in the `.env.example` file
