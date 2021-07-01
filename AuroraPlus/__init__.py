import requests
#from requests.structures import CaseInsensitiveDict
#import sys
#from datetime import datetime

from requests.api import head

PACKAGE_VERSION = '0.0.1'

class api:

    """
    Abstraction of the Aurora+ API
    """

    def __init__(self, username, password, timespan):

        self.url = 'https://api.auroraenergy.com.au/api'
        
        #Create a session and perform all requests in same session
        session = requests.Session()
        session.headers.update({'Accept': 'application/json', 'User-Agent': 'AuroraPlus.py', 'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive' })
        self.session = session
     
        #Get access token
        token = self.session.post(self.url+'/identity/login',data={'username': username, 'password': password})
        #print(token.status_code)

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
                print(premise['IsActive'])
                if (premise['IsActive']):
                    print("found active")
                    #Get all service data here
                    serviceAgreementID = currentjson['Premises'][0]['ServiceAgreementID']

                    self.AmountOwed = currentjson['Premises'][0]['AmountOwed']
                    self.EstimatedBalance = currentjson['Premises'][0]['EstimatedBalance']
                    self.AverageDailyUsaged = currentjson['Premises'][0]['AverageDailyUsage']
                    self.UsageDaysRemaining = currentjson['Premises'][0]['UsageDaysRemaining']
                    self.AmountOwed = currentjson['Premises'][0]['AmountOwed']

                    #Request data
                    self.data = self.session.get(self.url + '/usage/' + timespan +'?serviceAgreementID=' + serviceAgreementID + '&customerId=' + customerId + '&index=-1', headers={'Authorization': self.token})
                else:
                    self.Error = 'No active premise found'
        else:
            self.Error = token.reason

AuroraPlus = api("leigh.curran@outlook.com", "MuCEiD49%3Z%&y", "day")

if (not AuroraPlus.Error):
    print(AuroraPlus.AmountOwed)
else:
    print(AuroraPlus.Error)