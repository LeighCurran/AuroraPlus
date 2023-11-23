[![buy me a coffee](https://img.shields.io/badge/If%20you%20like%20it-Buy%20us%20a%20coffee-green.svg?style=for-the-badge)](https://www.buymeacoffee.com/leighcurran)

AuroraPlus is a package to pull data from https://api.auroraenergy.com.au/api. To use the Aurora+ API you need a valid account with Aurora.

## Requirements
- Install Python 3.9 (for all users)
- Pip install requests

## Usage

### Obtain a token

Obtaining a token is an interactive process where the user needs to log on to
the AuroraPlus web application.

    >>> import auroraplus
    >>> api = auroraplus.api()
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
    AuroraPlus = auroraplus.api(token={"access_token": "...", "token_type": "bearer"})
    AuroraPlus.get_info()

For backward compatibility with users of the login/password method, the
`access_token` can be passed as the `password` if the `user` is empty.

    import auroraplus
    AuroraPlus = auroraplus.api(password=<ACCESS_TOKEN>)
    AuroraPlus.get_info()

### Get current account information

    AuroraPlus.getcurrent()

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
    
    Note: All data except AverageDailyUsage is updated Daily.

An example getting specific data with getcurrent:

    import auroraplus
    AuroraPlus = auroraplus.api(token={"access_token": "...", "token_type": "bearer"})
    AuroraPlus.get_info()
    if (not AuroraPlus.Error):
        AuroraPlus.getcurrent()
        print(AuroraPlus.AmountOwed)
    else:
        print(AuroraPlus.Error)
        
### Get summary usage information

    AuroraPlus.getsummary()
    
    Note: This returns two collections, DollarValueUsage and KilowattHourUsage.
    
An example getting specific data with getsummary:

    import auroraplus
    AuroraPlus = auroraplus.api(token={"access_token": "...", "token_type": "bearer"})
    AuroraPlus.get_info()
    if (not AuroraPlus.Error):
        AuroraPlus.getsummary()
        print(AuroraPlus.DollarValueUsage['T41'])
        print(AuroraPlus.DollarValueUsage['T31'])
        print(AuroraPlus.DollarValueUsage['Other'])
        print(AuroraPlus.DollarValueUsage['Total'])
        print(AuroraPlus.KilowattHourUsage['T41'])
        print(AuroraPlus.KilowattHourUsage['T31'])
        print(AuroraPlus.KilowattHourUsage['Total'])
    else:
        print(AuroraPlus.Error)
        
    Note: Offpeak tarrifs not listed

### Get usage data use the following

The following returns all available data in json format for each timespan:

    AuroraPlus.getday()
    AuroraPlus.getweek()
    AuroraPlus.getmonth()
    AuroraPlus.getquarter()
    AuroraPlus.getyear()

Full example:

    AuroraPlus = auroraplus.api(token={"access_token": "...", "token_type": "bearer"})
    AuroraPlus.get_info()
    if (not AuroraPlus.Error):
        AuroraPlus.getcurrent()
        print(AuroraPlus.AmountOwed)
        
        AuroraPlus.getday()
        print(AuroraPlus.day)
        
        AuroraPlus.getweek()
        print(AuroraPlus.week)
        
        AuroraPlus.getmonth()
        print(AuroraPlus.month
        
        AuroraPlus.getyear()
        print(AuroraPlus.year)
    else:
        print(AuroraPlus.Error)
