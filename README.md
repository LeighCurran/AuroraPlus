[![buy me a coffee](https://img.shields.io/badge/If%20you%20like%20it-Buy%20us%20a%20coffee-green.svg?style=for-the-badge)](https://www.buymeacoffee.com/leighcurran)

AuroraPlus is a package to pull data from https://api.auroraenergy.com.au/api. To use the Aurora+ API you need a valid account with Aurora.

## Requirements
- Install Python 3.9 (for all users)
- `pip install .`

## Usage

### Obtain a token

The easieast way to obtain a new token is to use the `auroraplus_get_token`
script.

To do this more programatically, obtaining a token is an interactive process
where the user needs to log on to the AuroraPlus web application.

    >>> import auroraplus
    >>> api = auroraplus.AuroraPlusApi()
    >>> api.oauth_authorize()
    'https://customers.auroraenergy.com.au/auroracustomers1p.onmicrosoft.com/b2c_1a_sign_in//oauth2/v2.0/authorize?response_type=code&client_id=2ff9da64-8629-4a92-a4b6-850a3f02053d&redirect_uri=https%3A%2F%2Fmy.auroraenergy.coom.au%2Flogin%2Fredirect&scope=openid+profile+offline_access&state=...&client_info=1'

Follow the URL above in a browser to authenticate with username+password and
MFA. This will redirect to an error page (Cradle Mountain). Copy the full URL,
of the error page and continue.

    >>> api.oauth_redirect('https://my.auroraenergy.com.au/login/redirect?state=...')
    {'id_token': 'ey...', 'access_token': 'ey...', 'token_type': 'bearer', ...}

The `api` object is now ready to use (start with `api.get_info()`. The token
returned in the last step can be saved for later use when re-initialising the
`api` object without having to follow the OAuth flow to obtain a new
authorisation.

### Connect to Aurora+ API with a pre-issued token

    import auroraplus
    api = auroraplus.AuroraPlusApi(token={"access_token": "...", "token_type": "bearer"})
    api.get_info()

For backward compatibility with users of the login/password method, the
`access_token` can be passed as the `password` if the `user` is empty.

    import auroraplus
    api = auroraplus.AuroraPlusApi(password=<ACCESS_TOKEN>)
    api.get_info()

### Get current account information

    api.getcurrent()

getcurrent() gets the following data:

    EstimatedBalance - This is shown in the Aurora+ app as 'Balance'
    UsageDaysRemaining - This is shown in the Aurora+ app as 'Days Prepaid'
    AverageDailyUsage
    AmountOwed
    ActualBalance
    UnbilledAmount
    BillTotalAmount
    NumberOfUnpaidBills
    BillOverDueAmount
    
    Note: All data except EstimatedBalance is updated Daily.

    If relevant, time-of-use tariffs can be found in the following attributes:

    CurrentTimeOfUse
    CurrentTimeOfUsePeriodEndDate
    CurrentTimeOfUseType

An example getting specific data with getcurrent:

    import auroraplus
    api = auroraplus.AuroraPlusApi(token={"access_token": "...", "token_type": "bearer"})
    api.get_info()
    if (not api.Error):
        api.getcurrent()
        print(api.AmountOwed)
    else:
        print(api.Error)
        
### Get summary usage information

    api.getsummary()
    
    Note: This returns two collections, DollarValueUsage and KilowattHourUsage.
    
An example getting specific data with getsummary:

    import auroraplus
    api = auroraplus.AuroraPlusApi(token={"access_token": "...", "token_type": "bearer"})
    api.get_info()
    if (not api.Error):
        api.getsummary()
        print(api.DollarValueUsage['T41'])
        print(api.DollarValueUsage['T31'])
        print(api.DollarValueUsage['Other'])
        print(api.DollarValueUsage['Total'])
        print(api.KilowattHourUsage['T41'])
        print(api.KilowattHourUsage['T31'])
        print(api.KilowattHourUsage['Total'])
    else:
        print(api.Error)
        
    Note: Offpeak tarrifs not listed

### Get usage data

The following returns all available data in json format for each timespan:

    api.getday()
    api.getweek()
    api.getmonth()
    api.getquarter()
    api.getyear()

Full example:

    api = auroraplus.AuroraPlusApi(token={"access_token": "...", "token_type": "bearer"})
    api.get_info()
    if (not api.Error):
        api.getcurrent()
        print(api.AmountOwed)
        
        api.getday()
        print(api.day)
        
        api.getweek()
        print(api.week)
        
        api.getmonth()
        print(api.month
        
        api.getyear()
        print(api.year)
    else:
        print(api.Error)

### Get Power Hour

Information about upcoming Power Hour can be obtained with the `getpowerhour` method. It ppopulates a `powerhour` attribute. 

    import json
    api = auroraplus.AuroraPlusApi(token={"access_token": "...", "token_type": "bearer"})
    api.getcurrent()
    api.getpowerhour()
    print(json.dumps(api.powerhour, indent=2))
    [
      {
        "EventName": "Grand Final Weekend",
        "PowerHourEventId": 114,
        "StartDateTime": "2026-08-25T09:32:42",
        "OfferExpiryDateTime": "2026-09-27T12:55:00",
        "TimeslotAccepted": {
          "PowerHourTimeSlotId": 906,
          "StartDateTime": "2026-09-25T13:00:00",
          "EndDateTime": "2026-09-25T17:00:00",
          "ExpiryDateTime": "2026-09-25T12:55:00"
        },
        "TimeslotAll": [
          {
            "PowerHourTimeSlotId": 901,
            "StartDateTime": "2026-09-24T11:00:00",
            "EndDateTime": "2026-09-24T15:00:00",
            "ExpiryDateTime": "2026-09-24T10:55:00"
          },
    ...

## Development

### Tests

Currently, tests only do a lint check.

    pip install -e .[test]
    pytest

Some errors can be fixed automatically with

    ruff check --fix
