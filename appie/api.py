import requests


class Api(object):

    _username = ''
    _password = ''
    _cookies = {}
    _logged_in = False
    _shoppinglist = 0
    _list = None

    def __init__(self, username, password, login=True):
        self._username = username
        self._password = password

        self.login(username, password)

    def login(self, username, password):
        # Turns out this logon works but doesn't return personal shopping lists
        '''
        url = 'https://www.ah.nl/mijn/api/login'
        payload = {
            'username': username,
            'password': password
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        self._cookies = response.cookies
        '''
        # This login does
        url = 'https://www.ah.nl/service/loyalty/rest/tokens'
        payload = {
            'username': username,
            'password': password,
            'type':    "password",
            'domain':   "NLD"
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        self._cookies = response.cookies

    def add(self, product_id, quantity=1):
        payload = {
            'type':'PRODUCT',
            'item': {
                'id':str(product_id)
            },
            'quantity': int(quantity),
            'originCode': "PSE"
        }

        url = 'https://www.ah.nl/service/rest/shoppinglists/%d/items' % self._shoppinglist
        response = requests.post(url, cookies=self._cookies, json=payload)
        self._cookies = response.cookies
        if response.status_code == 200:
            return True
        else:
            return False

    def _update_list(self):
        url = 'https://www.ah.nl/service/rest/shoppinglists/%d/' % self._shoppinglist
        response = requests.get(url, cookies=self._cookies)
        self._cookies = response.cookies
        self._list = response.json()
        
        return self._list

    @property
    def list(self):
        return self._list

    def is_on_list(self, product_id):
        if self._list:
            self._update_list()

        counter = 0

        for item in self._list['items']['_embedded']['items']:
            if item['item']['id'] == product_id:
                return item['id']

        # @TODO: return proper exception?
        return None
