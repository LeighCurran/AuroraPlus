# Aurora+ Library

AuroraPlus.py is a package to pull data from https://api.auroraenergy.com.au/api. To use the Aurora+ API you need a valid account with Aurora.

## Requirements

AuroraPlus.py requires requests.py to run.

## Usage
```sh
Connect to Aurora+ API:
AuroraPlus = api("user.name@outlook.com", "password")

TO get information about your current account use the following:
AuroraPlus.getcurrent()

getcurrent gets the following data:
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
    AuroraPlus.AmountOwed

To get usage data use the following, thios returns all available data in json format for each timespan:
    AuroraPlus.getday()
    AuroraPlus.getweek()
    AuroraPlus.getmonth()
    AuroraPlus.getquarter()
    AuroraPlus.getyear()

Full example:

AuroraPlus = api("user.name@outlook.com", "password")
if (not AuroraPlus.Error):
    print(AuroraPlus.AmountOwed)
    print(AuroraPlus.day)
    print(AuroraPlus.week)
    print(AuroraPlus.month)
    print(AuroraPlus.year)
else:
    print(AuroraPlus.Error)
```
## ChangeLog
```sh
0.0.2: Initial relase
```

## License

MIT