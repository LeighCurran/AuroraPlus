import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import Timeout

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

        #Get access token
        try:
            token = self.session.post(self.url+'/identity/login',data={'username': username, 'password': password}, timeout=(2, 5))
    
            if (token.status_code == 200):
                tokenjson = token.json()
                self.token = tokenjson['accessToken']

                #Get CustomerID and ServiceAgreementID
                current = self.session.get(self.url+'/customers/current',headers={'Authorization': self.token}).json()[0]
                self.customerId = current['CustomerID']

                #Loop through premises to get active premise
                premises = current['Premises']
                for premise in premises:
                    if (premise['ServiceAgreementStatus'] == 'Active'):
                        self.Active = premise['ServiceAgreementStatus'] 
                        self.serviceAgreementID = premise['ServiceAgreementID']
                if (self.Active != 'Active'):
                    self.Error = 'No active premise found'
            else:
                self.Error = 'Token request failed: ' + token.reason
        except Timeout:
            self.Error = 'Token request timed out'

    def request(self, timespan):
        try:
            request = self.session.get(self.url + '/usage/' + timespan +'?serviceAgreementID=' + self.serviceAgreementID + '&customerId=' + self.customerId + '&index=-1', headers={'Authorization': self.token})
            if (request.status_code == 200):
                return request.json()
            else:
                self.Error = 'Data request failed: ' + request.reason  
        except Timeout:
            self.Error = 'Data request timed out'

    def getday(self):
        self.day = self.request("day")

    def getweek(self):
       self.week = self.request("week")

    def getmonth(self):
       self.month = self.request("month")

    def getquarter(self):
       self.quarter = self.request("quarter")

    def getyear(self):
       self.year = self.request("year")

    def getcurrent(self):
        try:
            #Request current customer data
            current = self.session.get(self.url+'/customers/current',headers={'Authorization': self.token})

            if (current.status_code == 200):
                currentjson = current.json()[0]

                #Loop through premises to match serviceAgreementID already found in token request
                premises = currentjson['Premises']
                found = ''
                for premise in premises:
                    if (premise['ServiceAgreementID'] == self.serviceAgreementID):
                        found = 'true'
                        self.AmountOwed = premise['AmountOwed']
                        self.EstimatedBalance = premise['EstimatedBalance']
                        self.AverageDailyUsaged = premise['AverageDailyUsage']
                        self.UsageDaysRemaining = premise['UsageDaysRemaining']
                        self.HasSolar = premise['HasSolar']
                        self.Address = premise['Address']
                        self.ActualBalance = premise['ActualBalance']
                        self.UnbilledAmount = premise['UnbilledAmount']
                        self.BillTotalAmount = premise['BillTotalAmount']
                        self.NumberOfUnpaidBills = premise['NumberOfUnpaidBills']
                        self.BillOverDueAmount = premise['BillOverDueAmount']
                if (found != 'true'):
                    self.Error = 'ServiceAgreementID not found'
            else:
                self.Error = 'Current request failed: ' + current.reason
        except Timeout:
            self.Error = 'Current request timed out'