def get_description():
    description = """
Dock challenge digital account's API

## User
Implemented Endpoints:
* **Insert User** - Insert user and its digital account
* **Delete User** - Delete user and its digital account and transactions if they exists
* **Get User** - Retrieve user info

## Digital Account
Implemented Endpoints:
* **Get Digital Account** - Retrieve digital account info of a user. Uses 'user_id' has search parameter
* **Get Statement** - Retrieve statement of a digital account. Uses 'start_date' and 'end_date'
 has period search parameters - if not given uses start_date=FirstDayOfTodayMonth and end_date=LastDayOfTodayMonth.
 **Provide the dates in the format o YYYYMMDD. ex.: 20220312**
* **Post Transaction** - Make a deposit or withdraw transaction on a digital account. 
**Use 1 for 'withdraw' and 2 to 'deposit' on request field 'transaction_type_id'.** 
* **Put Change Active Status** - Change the 'is_active' attribute of a given digital account. 
It works by updating the field with the opposite value that is stored. 
**ex: if the value 'true' is stored, it will change to 'false' and vice-versa.**
* **Put Change Blocked Status** - Change the 'is_blocked' attribute of a given digital account.
It works by updating the field with the opposite value that is stored.
**ex: if the value 'true' is stored, it will change to 'false' and vice-versa.**
"""
    return description
