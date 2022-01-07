import os

TESTING = False

## UKG Service Account Credentials
UKGUID = os.getenv('UID')
UKGPWD = os.getenv('PWD')
ClientAccessKey = os.getenv('CUSTOMERAPIKEY')
UserAccessKey = os.getenv('USERAPIKEY')
BaseURL = os.getenv('APIURLBASE')
RestURL = os.getenv('RESTURLBASE')
