import time
import configparser

class Auth:

    def __init__(self, username=None, password=None):
        
        CREDENTIAL_FILE = 'credentials/credentials.ini'
        
        if username is not None:
            self._username = username
        else:
            config = configparser.ConfigParser()
            print(config.read(CREDENTIAL_FILE))
            
            self._username = config['appnexus-read-write']['appnexus_username']
            self._password = config['appnexus-read-write']['appnexus_password']
            
        if password is not None:
            self._password = password
        else:
            config = configparser.ConfigParser()
            config.read(CREDENTIAL_FILE)
            self._password = config['appnexus-read-write']['appnexus_password']
    
        self._http = None
        self._auth_data = None
        self.createCredentialJson()

        
    def __str__(self):
        return "Login: " + self._username + "\nPassword: " + self._password
    
    
    def setUsername(self, username):
        self._username = username
    
    def getUsername(self):
        return self._username

    username = property(getUsername, setUsername)
    
    
    def setPassword(self, password):
        self._password = password
            
    def getPassword(self):
        return self._password
    
    password = property(getPassword, setPassword)
    
    
    def createCredentialJson(self):
        self._auth_data = {"auth":{"username":self._username,"password":self._password}}
        print(self._auth_data)
    
    def authorizationRequest(self, http=None):
        if http is not None:
            self._http = http
        self._http._service="auth"
        return self._http.postRequest(self._auth_data)

    def readResponse(self, r):
        response_json = r.json()['response']
        if 'error' not in response_json:
            if response_json['status'] == "OK":
                return (response_json['token'])
            else:
                print("Something went wrong. Check Auth Module")
        else:
            if 'No match found for user/pass' in response_json['error']:
                raise AuthException(self._username)
            else:
                print('Error: ' + str(response_json['error']))
                print("Trying to authorize again in 15 seconds.")
                time.sleep(15)
                self.readResponse(self.authorizationRequest())


# Import was kinda broken, so this Exception-class is (now) part of this file
class AuthException(Exception):

    def __init__(self, login):
        self.login = login
    
    def __str__(self):
        return "Login mit Credentials " + self.login + " nicht möglich"