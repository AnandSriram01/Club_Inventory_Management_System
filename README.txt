Clone this git repository to the preferred location in the system.

git clone <repo url>

Preferably create a Python virtual environment and activate it.

Proceed to the root directory of this project and run the following command to install the required packages.

pip install -r requirements.txt

Create a superuser to access the default Django admin view using the following command.

python manage.py createsuperuser

And fill in the username and password of your choice.

Then Execute the 2 following commands.

- python manage.py makemigrations
= python manage.py migrate


Run the below command to have the Django server running.

python manage.py runserver


Enter the following URL in the browser to view the default Django admin page and enter the credentials as entered before.

http://127.0.0.1:8000/admin

Create Admin Profile:

Under 'AUTHENTICATION AND AUTHORIZATION', click on 'Add' next to 'Users'.
Enter the username and password of your choice and press 'Enter'.
You will then be redirected to 'Change User' page.
Fill in the Personal Info details.
Scroll down to find 'Groups'.
Over there, select 'Admin' only.
Scroll to the bottom and click Save.

Click on 'Add' next to 'Clubs'.
Create a dummy club (just for the admin).

Click on 'Add' next to 'User Profiles'.
Select the 'username' under user and 'club' you add previously created above.

With this, the Admin profile has been created.


Navigate to Application :

Enter the following URL to reach the login page : http://127.0.0.1:8000/user/user_login
Enter the credentials of the admin profile.
You will be redirected to Admin dashboard.


Ideal Flow of Control :

For the best way of entering details without any hiccups, follow the below order in the Admin Dashboard :

1. Create a set of clubs.
2. Create a set of user profiles for each club.
- While creating the user profiles, assign role of 'Convenor' for at least one person.
3. Logout from the admin account.
4. Enter the credentials for the Convenor.
5. Create a set of items for the corresponding club.

Now that we have sufficient data of items, clubs and users, login to a member account, create requests and toy around with the entire application freely.

Note : Any other order of execution would give meaningless errors/results.


List of implemented features :

1. Admin, Convenor and Member Dashboards
2. Create User, Club (Admin)
3. Create Item (Convenor)
4. Create Request (Member)
5. Accept or Deny request (Convenor)
6. Delete User (Admin)
7. Login, Logout functionalities
8. Role-Based Access Control for all web pages.
9. Request Approval Flow with certain corner cases handled. 


List of non-implemented/planned features : 

1. Assigning role to user (Admin)
2. Convenor can't remark on the request
3. Sort and Filter list of data objects in client side.
4. Reset password, Forgot password
5. Member can request for multiple items of varying quantity in a single request. 
6. Convenor can accept, deny or partially accept such requests.
7. Revamp the UI to be responsive and appealing.
8. Segregate each list into different webpages for more clarity.
8. The given bonus tasks


List of known bugs : 

1. User can login to a different account without logging out of the previous account.
2. All fields are compulsory. So differing from 'Ideal Flow of Control' can inhibit the UX.


References Used :

https://docs.djangoproject.com/
https://medium.com/@himanshuxd/how-to-create-registration-login-webapp-with-django-2-0-fd33dc7a6c67
https://www.techwithtim.net/tutorials/django/user-specific-pages-data/
https://www.youtube.com/watch?v=EX6Tt-ZW0so&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=12
https://medium.com/djangotube/django-roles-groups-and-permissions-introduction-a54d1070544









