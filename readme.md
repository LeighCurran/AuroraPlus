[![buy me a coffee](https://img.shields.io/badge/If%20you%20like%20it-Buy%20us%20a%20coffee-green.svg?style=for-the-badge)](https://www.buymeacoffee.com/leighcurran)

AuroraPlus is a package to pull data from https://api.auroraenergy.com.au/api. To use the Aurora+ API you need a valid account with Aurora.

## Requirements
- Install Python 3.9 (for all users)
- Pip install requests

## Usage

Connect to Aurora+ API:

    import auroraplus
    AuroraPlus = auroraplus.api(token={"access_token": "...", "token_type": "bearer"})
    AuroraPlus.get_info()

To get current account information use the following:

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
        
To get summary usage information use the following:

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

To get usage data use the following, this returns all available data in json format for each timespan:

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
