"""Abstraction of the Aurora+ API"""
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import Timeout

from requests_oauthlib import OAuth2Session


class api:
    USER_AGENT = 'python/auroraplus'

    OAUTH_BASE_URL = 'https://customers.auroraenergy.com.au' \
        '/auroracustomers1p.onmicrosoft.com/b2c_1a_sign_in/'
    AUTHORIZE_URL = OAUTH_BASE_URL + '/oauth2/v2.0/authorize'
    TOKEN_URL = OAUTH_BASE_URL + '/oauth2/v2.0/token'
    CLIENT_ID = '2ff9da64-8629-4a92-a4b6-850a3f02053d'
    REDIRECT_URI = 'https://my.auroraenergy.com.au/login/redirect'

    API_URL = 'https://api.auroraenergy.com.au/api'
    BEARER_TOKEN_URL = API_URL + '/identity/LoginToken'

    SCOPE = ['openid', 'profile', 'offline_access']

    def __init__(self,
                 username: str = None, password: str = None,
                 token: dict = None):
        """Initialise the API.

        Parameters:
        -----------

        username: str
            Deprecated, kept for backward compatibility

        password: str
            Deprecated, kept for backward compatibility. If passed with an empty
            username and no token, the password will be use as a bearer
            access_token.

        token : dict
            A pre-established token. It should contain at least an access_token
            and a token_type.

        """
        self.Error = None
        backward_compat = False
        if not username and not token:
            # Backward compatibility: if no username and no token,
            # assume the passowrd is a bearer access token
            token = {'access_token': password, 'token_type': 'bearer'}
            backward_compat = True
        self.token = token
        api_adapter = HTTPAdapter(max_retries=2)

        """Create a session and perform all requests in the same session"""
        session = OAuth2Session(
            self.CLIENT_ID,
            redirect_uri=self.REDIRECT_URI,
            scope=self.SCOPE,
            token=token
        )
        session.mount(self.API_URL, api_adapter)
        session.headers.update({
            'Accept': 'application/json',
            'User-Agent': self.USER_AGENT,
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        self.session = session

        if backward_compat:
            self.get_info()

    def get_token(self, username=None, password=None):
        """
        Deprecated, kept for backward compatibility
        """
        self.get_info()

    def get_info(self):
        """Get CustomerID and ServiceAgreementID"""
        try:
            r = self.session.get(
                self.API_URL + '/customers/current'
            )
            r.raise_for_status()
            current = r.json()[0]
            self.customerId = current['CustomerID']

            """Loop through premises to get active """
            premises = current['Premises']
            for premise in premises:
                if (premise['ServiceAgreementStatus'] == 'Active'):
                    self.Active = premise['ServiceAgreementStatus']
                    self.serviceAgreementID = premise['ServiceAgreementID']
            if (self.Active != 'Active'):
                self.Error = 'No active premise found'
        except Timeout:
            self.Error = 'Info request timed out'

    def request(self, timespan, index=-1):
        if not self.serviceAgreementID:
            self.get_info()
        try:
            request = self.session.get(
                self.API_URL
                + '/usage/'
                + timespan
                + '?serviceAgreementID='
                + self.serviceAgreementID
                + '&customerId='
                + self.customerId
                + '&index='
                + str(index)
            )
            if (request.status_code == 200):
                return request.json()
            else:
                self.Error = 'Data request failed: ' + request.reason
        except Timeout:
            self.Error = 'Data request timed out'

    def getsummary(self, index=-1):
        summarydata = self.request("day", index)
        self.DollarValueUsage = summarydata['SummaryTotals']['DollarValueUsage']
        self.KilowattHourUsage = summarydata['SummaryTotals']['KilowattHourUsage']

    def getday(self, index=-1):
        self.day = self.request("day", index)

    def getweek(self, index=-1):
        self.week = self.request("week", index)

    def getmonth(self, index=-1):
        self.month = self.request("month", index)

    def getquarter(self, index=-1):
        self.quarter = self.request("quarter", index)

    def getyear(self, index=-1):
        self.year = self.request("year", index)

    def getcurrent(self):
        try:
            """Request current customer data"""
            current = self.session.get(
                self.API_URL + '/customers/current'
            )

            if (current.status_code == 200):
                currentjson = current.json()[0]

                """Loop through premises to match serviceAgreementID already found in token request"""
                premises = currentjson['Premises']
                found = ''
                for premise in premises:
                    if (premise['ServiceAgreementID'] == self.serviceAgreementID):
                        found = 'true'
                        self.AmountOwed = "{:.2f}".format(premise['AmountOwed'])
                        self.EstimatedBalance = "{:.2f}".format(premise['EstimatedBalance'])
                        self.AverageDailyUsage = "{:.2f}".format(premise['AverageDailyUsage'])
                        self.UsageDaysRemaining = premise['UsageDaysRemaining']
                        self.ActualBalance = "{:.2f}".format(premise['ActualBalance'])
                        self.UnbilledAmount = "{:.2f}".format(premise['UnbilledAmount'])
                        self.BillTotalAmount = "{:.2f}".format(premise['BillTotalAmount'])
                        self.NumberOfUnpaidBills = premise['NumberOfUnpaidBills']
                        self.BillOverDueAmount = "{:.2f}".format(premise['BillOverDueAmount'])
                if (found != 'true'):
                    self.Error = 'ServiceAgreementID not found'
            else:
                self.Error = 'Current request failed: ' + current.reason
        except Timeout:
            self.Error = 'Current request timed out'
