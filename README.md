# Finin-Internship
### Basic Setup
- Setting up a django server
```
$ virtualenv -p python3 venv     
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
```
- Create a superuser for accessing the API doc
```
$ python manage.py createsuperuser
```
- Run the django development server
```
$ python manage.py runserver
```
- Visit the [API documentation](http://localhost:8000/docs/) to view all the end points


### Handling concurrent session
- Custom model `UserSessions` defined to store the sessions details like client-ip,client-agent,etc along with is_active attribute that determines if the session is active.



- When a user logs in the signal  `user_logged_in_handler` invalidates all the old active sessions of the user and creates a new valid session.


- When a user logs out the signal `user_logged_out_handle` invalidates the current session by updating `is_active=False`.


- To test if the user is operating the same account on multiple devices, a custom permission  `ValidSessionPermission` is defined which returns `False` if the current session's attribute `is_active=False`.

### Testing concurrent session handlers
- Create a [user with username and mobile number](http://localhost:8000/users/signup/)
- Login with that [username and password](http://localhost:8000/api-auth/login/?next=/users/list/) on two different browsers simultaneously and [visit this link](http://localhost:8000/users/list/).
- An `HTTP 403` response is encountered on the browser that logged in first and has older concurrent session with error message ```{"detail": "There is already another session up and running, please logout and login again.}"```  
### Checking the session details of a user
- Login as a superuser and visit either [the docs](http://localhost:8000/docs/#session-read) or directly visit http://localhost:8000/users/session/{mobile_number} with the users mobile number in place of {mobile_number} in the url.


- To see a detailed list of user sessions visit [the docs](/users/session/{mobile_number}/v) or http://localhost:8000/users/session/{mobile_number}/v
with mobile number of the user in place of {mobile_number of the user}
