# 🛡️ LDAP Injection Vulnerability Exploitation Script

This repository contains a Python script designed for exploiting LDAP injection vulnerabilities in a controlled environment. The script allows you to extract and visualize user descriptions, phone numbers, and usernames by leveraging LDAP injection techniques. The environment setup and configuration can be found in [this repository](https://github.com/motikan2010/LDAP-Injection-Vuln-App).

![image](https://github.com/user-attachments/assets/354485b6-5527-4082-9cfe-701339b718e2|200)


## 📚 Table of Contents

- [Features](#-features)
- [Prerequisites](#%EF%B8%8F-prerequisites)
  - [Adding Users](#-adding-users)
- [Installation](#-installation)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
  - [Signal Handling](#-signal-handling)
  - [User Enumeration](#-user-enumeration)
  - [Email Extraction](#email-extraction)
  - [Description and Phone Number Extraction](#-description-and-phone-number-extraction)
  - [Customization](#-customization)
- [Disclaimer](#-disclaimer)
- [License](#-license)

## ✨ Features

- **User Enumeration:** Identifies potential usernames by brute-forcing using LDAP injection.
- **Email Extraction:** Extracts valid email addresses associated with discovered usernames.
- **Description Extraction:** Retrieves user descriptions by exploiting the LDAP injection vulnerability.
- **Phone Number Extraction:** Obtains phone numbers of users through injected queries.

## 🛠️ Prerequisites

- **Python 3.x** is required.
- **Burp Suite** or any other proxy tool should be configured and running.
- Install dependencies via `pip install -r requirements.txt` if a `requirements.txt` is provided.

## ➕ Adding Users
To use the script effectively, you need to add users to the LDAP directory. You can do this by creating and modifying a newuser.ldif file. Below is an example of what the newuser.ldif file might look like:

``` txt
dn: uid=newuser,ou=users,dc=example,dc=org
objectClass: inetOrgPerson
sn: User
cn: New User
uid: newuser
mail: newuser@example.org
userPassword: password
telephoneNumber: 123456789
description: This is a test user
```

After creating the newuser.ldif file, modify the user details as needed and add them to the LDAP directory using the following command:

``` bash
ldapadd -x -H ldap://localhost -D "cn=admin,dc=example,dc=org" -w admin -f newuser.ldif
```

## 📥 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/S4njer/ldap-injection-exploit.git
   cd ldap-injection-exploit
   ```

2. Set up the vulnerable environment by following the instructions in [this repository](https://github.com/motikan2010/LDAP-Injection-Vuln-App).

3. Ensure Burp Suite or the configured proxy is running and listening on the specified port (default: `127.0.0.1:8080`).

## 🚀 Usage

Run the script to begin the enumeration and extraction process:

```bash
python3 script.py
```

## 🧩 How It Works

### 🛑 Signal Handling

The script starts by setting up a signal handler to gracefully exit when interrupted (Ctrl+C).

### 🔍 User Enumeration

- The script sends HTTP POST requests to the target URL with various `user_id` values (constructed using characters from a predefined set).
- If the server responds with a status code `301`, the current character is considered part of a valid username.

### ✉️ Email Extraction

- For each valid username, the script performs LDAP injection to retrieve associated email addresses.

### 📜 Description and Phone Number Extraction

- The script further injects queries to obtain user descriptions and phone numbers by iterating through potential values.

### ⚙️ Customization

- Modify `main_url` and `burp` variables to match your testing environment.
- Adjust the `characters` variable to refine the set of characters used during brute-force attacks.

## ⚠️ Disclaimer

This script is intended for educational purposes and should only be used in environments where you have explicit permission to test for security vulnerabilities. Misuse of this script could result in legal consequences.

## 📄 License

This project is licensed under the MIT License.

---

This version of the `README.md` is more visually appealing and organized, making it easier to navigate and understand.
