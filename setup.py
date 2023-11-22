from setuptools import setup
from distutils.core import setup
from os import path

setup(
    name='auroraplus',
    packages=['auroraplus'],
    version='1.1.6',
    license='MIT',
    description='Python library to access the Aurora+ API: https://api.auroraenergy.com.au/api',
    long_description="""AuroraPlus is a package to pull data from https://api.auroraenergy.com.au/api. To use the Aurora+ API you need a valid account with Aurora.

## Requirements
- Install Python 3.9 (for all users)
- Pip install requests

## Usage

Connect to Aurora+ API:

    import auroraplus
    AuroraPlus = auroraplus.api(token)
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
        print(AuroraPlus.Error)""",
    long_description_content_type='text/markdown',
    author='Leigh Curran',
    author_email='AuroraPlusPy@outlook.com',
    url='https://github.com/leighcurran/AuroraPlus',
    keywords=['Aurora+', 'AuroraPlus', 'Aurora', 'Tasmania', 'API'],
    install_requires=[
        'requests',
        'requests_oauthlib',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
