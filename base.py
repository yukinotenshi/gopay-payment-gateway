import requests
import json


class Request:
    '''Base request object to simplify gojek requests'''
    def __init__(self, version='3.4.1', 
                 secret='83415d06-ec4e-11e6-a41b-6c40088ab51e',
                 location='-6.953946,107.677765', token='',
                 uid='9774d56d682e549c'):
        self.version = version
        self.secret = secret
        self.location = location
        self.token = token
        self.uid = uid
        self.base = 'https://api.gojekapi.com'


    def headers(self) -> dict:
        '''Generate headers required by gojek api'''
        return {
            'content-type' : 'application/json',
            'X-AppVersion' : self.version,
            'X-UniqueId' : self.uid,
            'X-Location' : self.location,
            'Authorization' : 'Bearer ' + self.token
        }


    def get(self, link: str):
        '''Send a get request to gojek API'''
        r = requests.get(self.base + link, headers=self.headers())

        return r


    def post(self, link: str, data={}):
        '''Send a POST request to gojek API'''
        r = requests.post(self.base + link, headers=self.headers(), json=data)

        return r


class Gopay:
    '''Base class for interacting with gojek login and gopay'''
    def __init__(self, email: str,  **kwargs):
        self.email = email
        self.request = Request(**kwargs)


    def login(self, **kwargs):
        r = self.request.post('/v3/customers/login_with_email', data={'email': self.email})
        otp = input('Please enter your phone verification token : ')

        result = json.loads(r.text)
        login_token = result['data']['login_token']

        data = {
            'scopes': 'gojek:customer:transaction gojek:customer:readonly',
            'grant_type': 'otp',
            'data': {
                'otp_token': login_token,
                'otp': otp,
            },
            'client_name': 'gojek:cons:ios',
            'client_secret': self.request.secret
        }

        r = self.request.post('/v3/customers/verify', data=data)

        self.request.token = json.loads(r.text)['data']['access_token']

        return self.request.token

    def history(self, limit):
        result = self.request.get('/wallet/history?page=1&limit=%d' % limit)

        return json.loads(result.text)['data']['success']


    @classmethod
    def load(cls, token: str, **kwargs):
        instance = cls('anything@gmail.com')
        instance.request.token = token

        return instance