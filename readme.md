AuroraPlus.py is a package to pull data from https://api.auroraenergy.com.au/api. To use the Aurora+ API you need a valid account with Aurora.

## Install
- Install Python 3.9 (for all users)
- Pip install requests (Requests is a requirement of AuroraPlus)
- pip install auroraplus

## Usage

Connect to Aurora+ API:

    import auroraplus
    AuroraPlus = auroraplus.api("user.name@outlook.com", "password")

To get information about your current account use the following:

    AuroraPlus.getcurrent()

getcurrent() gets the following data:

    EstimatedBalance - This is shown in the Aurora+ app as 'Balance'
    UsageDaysRemaining - This is shown in the Aurora+ app as 'Days Prepaid'
    AverageDailyUsaged
    HasSolar
    Address
    AmountOwed
    ActualBalance
    UnbilledAmount
    BillTotalAmount
    NumberOfUnpaidBills
    BillOverDueAmount

An example getting specific data with getcurrent:

    import auroraplus
    AuroraPlus = auroraplus.api("user.name@outlook.com", "password")
    if (not AuroraPlus.Error):
        AuroraPlus.getcurrent()
        print(AuroraPlus.AmountOwed)
    else:
        print(AuroraPlus.Error)

To get usage data use the following, this returns all available data in json format for each timespan:

    AuroraPlus.getday()
    AuroraPlus.getweek()
    AuroraPlus.getmonth()
    AuroraPlus.getquarter()
    AuroraPlus.getyear()

Full example:

    AuroraPlus = auroraplus.api("user.name@outlook.com", "password")
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