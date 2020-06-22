# tagged-pets-bot

## Setup
This is a request library based python application which calls Hi5/Tagged pets APIs. Useable with two cookies for each user account in tagged or hi5. Currently the URL is assigned the Hi5 base link.

In order to change the URL:

```
# bot.py
url = "http://www.hi5.com/api/?application_id=user&format=JSON"
```
 
 needs to be changed to 
 
```
# bot.py
url = "http://www.tagged.com/api/?application_id=user&format=JSON"
```

---

Cookies are located in config.py. These must be extracted from your favorite browser. Simply copy pasting them will work.

```
# config.py
COOKIE_BHA = 'This should be the cookies for one user'
COOKIE_NIKKI = 'This should be the cookies for other user'
```

---
## Usage

1. The user you think of buying has an id which can be found moving to his/her pets profile. At the end of the URL a number like `6119757178` can be seen. This is the pet ID. Simply replacing this USER_ID with the ID found in above step is sufficient for buying the user.

```
# bot.py
def buy_two_way():
    x = 0
    print("Your account")
    x += payload_generator(COOKIE_BHA, USER_ID)
    print("Your fake account")
    x += payload_generator(COOKIE_NIKKI, USER_ID)
    return x
```
2. Now run the application with `python3 bot.py`. Before that you may need to install required libraries `json`, `requests`.
     
