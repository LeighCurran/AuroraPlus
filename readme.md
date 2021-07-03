# Aurora+ Library

AuroraPlus.py is a package to pull data from https://api.auroraenergy.com.au/api. To use the Aurora+ API you need a valid account with Aurora.

## Requirements

AuroraPlus.py requires requests.py to run.

## Usage
```sh
Connect to Aurora+ API:
AuroraPlus = api("user.name@outlook.com", "password")

Get information about your current account:
AuroraPlus.getcurrent()

getcurrent gets the following data:

    EstimatedBalance - This is shown in the Aurora+ app as 'Balance'
    UsageDaysRemaining - This is shown in the Aurora+ app as 'Days Prepaid'
    AverageDailyUsaged
    HasSolar
    Address
    AmountOwed -
    ActualBalance
    UnbilledAmount
    BillTotalAmount
    NumberOfUnpaidBills
    BillOverDueAmount

Get day usage infromation:
AuroraPlus.getday()

Get week usage infromation:
AuroraPlus.getweek()

Get month usage infromation:
AuroraPlus.getmonth()

Get quarter usage infromation:
AuroraPlus.getquarter()

Get year usage infromation:
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