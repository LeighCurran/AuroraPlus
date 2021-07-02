import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import Timeout
#rom requests.api import head

PACKAGE_VERSION = '0.0.1'

class api:

    """
    Abstraction of the Aurora+ API
    """

    def __init__(self, username, password, timespan):

        self.Error = ''
        self.url = 'https://api.auroraenergy.com.au/api'

        api_adapter = HTTPAdapter(max_retries=2)
        
        #Create a session and perform all requests in the same session
        session = requests.Session()
        session.mount('https://api.auroraenergy.com.au/api', api_adapter)
        session.headers.update({'Accept': 'application/json', 'User-Agent': 'AuroraPlus.py', 'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive' })
        self.session = session
     
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
                        self.Active = premise['ServiceAgreementStatus'] 
                        self.AmountOwed = premise['AmountOwed']
                        self.EstimatedBalance = premise['EstimatedBalance']
                        self.AverageDailyUsaged = premise['AverageDailyUsage']
                        self.UsageDaysRemaining = premise['UsageDaysRemaining']
                        self.AmountOwed = premise['AmountOwed']

                        #Request data
                        self.data = self.session.get(self.url + '/usage/' + timespan +'?serviceAgreementID=' + serviceAgreementID + '&customerId=' + customerId + '&index=-1', headers={'Authorization': self.token})
                    
                if (self.Active != 'Active'):
                    self.Error = 'No active premise found'
            else:
                self.Error = token.reason
        except Timeout:
            self.Error = 'The request timed out'

AuroraPlus = api("leigh.curran@outlook.com", "MuCEiD49%3Z%&y", "day")

if (not AuroraPlus.Error):
    print(AuroraPlus.AmountOwed)
else:
    print(AuroraPlus.Error)