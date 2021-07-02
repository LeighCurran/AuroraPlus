import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import Timeout
from requests.sessions import Request
#rom requests.api import head

PACKAGE_VERSION = '0.0.1'

class api:

    """
    Abstraction of the Aurora+ API
    """

    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.Error = ''
        self.url = 'https://api.auroraenergy.com.au/api'

        api_adapter = HTTPAdapter(max_retries=2)
        
        #Create a session and perform all requests in the same session
        session = requests.Session()
        session.mount(self.url, api_adapter)
        session.headers.update({'Accept': 'application/json', 'User-Agent': 'AuroraPlus.py', 'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive' })
        self.session = session
        print('session')

    def request(self, username, password, timespan):

            #Get access token
            try:
                token = self.session.post(self.url+'/identity/login',data={'username': username, 'password': password}, timeout=(2, 5))
        
                if (token.status_code == requests.codes.ok):

                    tokenjson = token.json()
                    self.token = tokenjson['accessToken']

                    #Request current customer data
                    current = self.session.get(self.url+'/customers/current',headers={'Authorization': self.token})
                    currentjson = current.json()[0]
                    customerId = currentjson['CustomerID']

                    #Loop through premises to get active premise
                    premises = currentjson['Premises']
                    for premise in premises:
                        if (premise['ServiceAgreementStatus'] == 'Active'):
                            #Get all service data here
                            serviceAgreementID = premise['ServiceAgreementID']

                            #Request data
                            self.data = self.session.get(self.url + '/usage/' + timespan +'?serviceAgreementID=' + serviceAgreementID + '&customerId=' + customerId + '&index=-1', headers={'Authorization': self.token}).json()
                    if (self.Active != 'Active'):
                        self.Error = 'No active premise found'
                else:
                    self.Error = token.reason
            except Timeout:
                self.Error = 'The request timed out'

    def day(self):
        self.request(self.username, self.password, "day")

    def week(self):
       self.request(self.username, self.password, "week")

    def month(self):
       self.request(self.username, self.password, "month")

    def quarter(self):
       self.request(self.username, self.password, "quarter")

    def year(self):
       self.request(self.username, self.password, "year")

    def current(self):
     
        #Get access token
        try:
            token = self.session.post(self.url+'/identity/login',data={'username': self.username, 'password': self.password}, timeout=(2, 5))
      
            if (token.status_code == requests.codes.ok):

                tokenjson = token.json()
                self.token = tokenjson['accessToken']

                #Request current customer data
                current = self.session.get(self.url+'/customers/current',headers={'Authorization': self.token})
                currentjson = current.json()[0]

                #Loop through premises to get active premise
                premises = currentjson['Premises']
                for premise in premises:
                    if (premise['ServiceAgreementStatus'] == 'Active'):

                        #Get all service data here
                        self.Active = premise['ServiceAgreementStatus'] 
                        self.AmountOwed = premise['AmountOwed']
                        self.EstimatedBalance = premise['EstimatedBalance']
                        self.AverageDailyUsaged = premise['AverageDailyUsage']
                        self.UsageDaysRemaining = premise['UsageDaysRemaining']
                        self.AmountOwed = premise['AmountOwed']

                if (self.Active != 'Active'):
                    self.Error = 'No active premise found'
            else:
                self.Error = token.reason
        except Timeout:
            self.Error = 'The request timed out'

AuroraPlus = api("leigh.curran@outlook.com", "MuCEiD49%3Z%&y")
AuroraPlus.current()
AuroraPlus.week()

if (not AuroraPlus.Error):
    print(AuroraPlus.AmountOwed)
    print(AuroraPlus.data)
else:
    print(AuroraPlus.Error)