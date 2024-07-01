"""Abstraction of the Aurora+ API"""
import base64
import hashlib
import json
import random
import string
import uuid

from requests.adapters import HTTPAdapter
from requests.exceptions import Timeout
from requests_oauthlib import OAuth2Session

from .get_token import get_token

class api:
    '''
    A client to interact with the Aurora+ API.

    Obtaining a new OAuth token is done in two steps:

        >>> import auroraplus
        >>> api = auroraplus.api()
        >>> api.oauth_authorize()
        'https://customers.auroraenergy.com.au/...'

    After following the prompts, the URL of the (error) page that's returned should be passed as the redirect URI.

        >>> token = api.oauth_redirect('https://my.auroraenergy.com.au/login/redirect?state=...')

    The `api` object is now authenticated.


    Data can then be fetched with

        >>> api.getcurrent()
        >>> api.getday()
        >>> api.getmonth()
        >>> api.getquarter()
        >>> api.getyear()

    and inspected in, e.g.,

        >>> api.day
        {'StartDate': '2023-12-25T13:00:00Z', 'EndDate': '2023-12-26T13:00:00Z', 'TimeMeasureCount': 1, ...

    '''
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

        An authenticated object can be recreated from a preexisting OAuth `token` with

            >>> api = auroraplus.api(token)


        Alternatively, a backward compatible way exists to only pass the `access_token`

            >>> api = auroraplus.api(password=token['access_token'])

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
        if not token and password and not username:
            # Backward compatibility: if no username and no token,
            # assume the password is a bearer access token
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

        if backward_compat and self.token:
            self.get_info()

    def oauth_authorize(self) -> str:
        """
        Start an OAuth Web Application authentication with Aurora Plus

        Returns:
        --------

        str: the URL to query interactively to authorize this session

        """
        state = {
            "id": str(uuid.uuid4()),
            "meta": {"interactionType": "redirect"},
        }

        self.code_verifier = ''.join([random.choice(
            string.ascii_letters
            + string.digits
            + '-_')
            for i in range(43)])
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(self.code_verifier.encode()).digest()
        ).strip(b'=')

        self.authorization_url, _ = self.session.authorization_url(
            self.AUTHORIZE_URL,
            client_request_id=uuid.uuid4(),
            client_info=1,
            code_challenge=code_challenge,
            code_challenge_method='S256',
            state=base64.encodebytes(json.dumps(state).encode()))

        return self.authorization_url

    def oauth_redirect(self, authorization_response: str):
        """
        Continue an OAuth Web Application authentication with Aurora Plus.

        Needs to be called after oauth_authorize.

        Parameters:
        -----------

        authorization_response: str

            The full URI of the response (error) page after authentication.

        Returns:
        --------

        dict: full token information

        """
        if not self.session.compliance_hook['access_token_response']:
            self.session.register_compliance_hook(
                'access_token_response',
                self._include_access_token)

        return self.session.fetch_token(
            self.TOKEN_URL,
            authorization_response=authorization_response,
            code_verifier=self.code_verifier,
        )

    def oauth_dump(self) -> dict:
        """
        Export partial OAuth state, for use in asynchronous or request/response-based
        workflows.

        Returns:
        --------

        dict: a dict of all the relevant state
        """
        return {
            'authorization_url': self.authorization_url,
            'code_verifier': self.code_verifier,
        }

    def oauth_load(self,
                   authorization_url: str,
                   code_verifier: str,
                   ):
        """
        Import partial OAuth state.

        Params:
        -------

        kwargs: pass the state dict returned from oauth_dump.
        """
        self.authorization_url = authorization_url
        self.code_verifier = code_verifier

    def _include_access_token(self, r) -> dict:
        """
        OAuth compliance hook to fetch the bespoke LoginToken,
        and present it as a standard access_token.

        Returns:
        --------

        dict: the full token
        """
        rjs = r.json()
        id_token = rjs.get('id_token')

        atr = self.session.post(self.BEARER_TOKEN_URL,
                                json={'token': id_token}
                                )
        access_token = atr.json().get('accessToken')

        rjs.update({
            'access_token': access_token.split()[1],
            'scope': 'openid profile offline_access',
        })

        r._content = json.dumps(rjs).encode()

        return r

    def gettoken(self, username=None, password=None):
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
