from textwrap import dedent
from typing import Callable
import pytest
from requests import Request
import requests_mock

from auroraplus import AuroraPlusApi
from tests.consts import CUSTOMER_ID, SERVICE_AGREEMENT_ID


@pytest.fixture
def token() -> dict:
    return {
        "id_token": "id_token-from-fixture",
        "token_type": "bearer",
        "not_before": 1766569720,
        "id_token_expires_in": 3600,
        "profile_info": "eyJ2ZXIiOiIxLjAiLCJ0aWQiOiI1OTlhNjkxMi05NmViLTQ4NzctODJjOC1jMmZlY2Y5NGRhZjciLCJzdWIiOm51bGwsIm5hbWUiOiJMYXN0LCBGaXJzdCIsInByZWZlcnJlZF91c2VybmFtZSI6bnVsbCwiaWRwIjoiTG9jYWwifQo",
        "scope": "openid offline_access",
        "refresh_token": "eyJraWQiOiJSRUZSRVNIS0lEUkVGUkVTSEtJRFJFRlJFU0hLSURSRUZSRVNIS0lEUkVGIiwidmVyIjoiMS4wIiwiemlwIjoiRGVmbGF0ZSIsInNlciI6IjEuMCJ9Cg.WFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWAo.XXXXXXXXXX-XXXXX.WFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYClhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWAo.XXXXXXXXXX-XXXXXXXXXXX",
        "refresh_token_expires_in": 86400,
        "access_token": "accessToken-from-fixture",
        "cookie_RefreshToken": "refreshTokenCookie-from-fixture",
    }


@pytest.fixture
def api(token: dict) -> AuroraPlusApi:
    return AuroraPlusApi(token=token)


@pytest.fixture
def current_response() -> str:
    return dedent("""
        [
            {
                "ABN": null,
                "BusinessName": null,
                "ConcessionStatus": false,
                "ConflictingCustomers": null,
                "ConflictingEmail": false,
                "CustomerID": "100100001",
                "CustomerType": "Residential",
                "EmailAddress": "customer@example.net",
                "FirstName": "First",
                "GivenNames": null,
                "HasHadPAYGProduct": true,
                "HasHadSolarProduct": true,
                "HasMatchingEmail": true,
                "HasPAYGProduct": true,
                "HasSolarProduct": true,
                "IsFromHubCX": true,
                "IsNewlyCreated": false,
                "LastActivityTime": null,
                "LastLoginTime": null,
                "LastName": "Last",
                "MobileNumber": "0400000000",
                "Premises": [
                    {
                        "AccountStatus": "BILL",
                        "ActualBalance": -73.71,
                        "Address": "1 EXAMPLE ST HOBART 7000 TAS",
                        "AmountOwed": 0.0,
                        "AverageDailyUsage": 4.33,
                        "BalanceLastUpdatedDate": "2025-12-23T13:00:00+00:00",
                        "BillDue": null,
                        "BillFrom": null,
                        "BillId": "18337887",
                        "BillIdToPay": null,
                        "BillNextRun": "2026-01-09T13:00:00+00:00",
                        "BillNextTo": "2026-01-06T13:00:00+00:00",
                        "BillOverDueAmount": 0.0,
                        "BillTo": null,
                        "BillTotalAmount": 0.0,
                        "ConcessionDetail": null,
                        "CurrentAppExperience": "PAYG",
                        "CurrentTimeOfUse": "Peak - Residential Time of Use - Tariff 93",
                        "CurrentTimeOfUsePeriodEndDate": "2025-12-26T11:00:01Z",
                        "CurrentTimeOfUseType": "PEAK",
                        "EstimatedBalance": -81.56,
                        "HasActivePaymentExtension": false,
                        "HasActivePaymentPlans": false,
                        "HasConcessionsApplied": null,
                        "HasExplicitInformedConsent": null,
                        "HasInterimStatus": false,
                        "HasOffProductStatus": false,
                        "HasOnProductStatus": true,
                        "HasPAYGPlus": true,
                        "HasSolar": true,
                        "IsActive": true,
                        "LastMeterReadDate": null,
                        "LifeSupport": "N",
                        "Meters": [
                            {
                                "BadgeNumber": null,
                                "MeterID": "8000000100",
                                "MeterType": "COMMS4D",
                                "NMI": "8000000100",
                                "NetworkTarriffs": null
                            }
                        ],
                        "NumberOfUnpaidBills": 0,
                        "ParentAccountID": "100100010",
                        "ParentAccountNumber": "100100010",
                        "ParentAccountNumberCheckDigit": "4",
                        "ParentPremiseID": "100100010",
                        "PostCode": "7000",
                        "ServiceAgreementID": "100100010",
                        "ServiceAgreementOfferNumber": "TERAP010",
                        "ServiceAgreementStartDate": "2023-05-18T14:00:00+00:00",
                        "ServiceAgreementStatus": "Active",
                        "ServiceAgreementType": "Residential",
                        "Status": null,
                        "SubmissionTime": null,
                        "Suburb": "HOBART",
                        "UnbilledAmount": -73.71,
                        "UnbilledAmountAsAt": "2025-12-23T13:00:00+00:00",
                        "UsageDaysRemaining": 0
                    }
                ],
                "ProductLevel": "ONPRODUCT",
                "Title": "MR",
                "UnreadNotificationsCount": 0,
                "lifeSupport": false
            }
        ]
    """)


@pytest.fixture
def premises_response() -> str:
    return dedent("""
        {
            "ABN": null,
            "BusinessName": null,
            "ConcessionStatus": false,
            "ConflictingCustomers": null,
            "ConflictingEmail": false,
            "CustomerID": "100100001",
            "CustomerType": "Residential",
            "EmailAddress": "customer@example.net",
            "FirstName": "First",
            "GivenNames": null,
            "HasHadPAYGProduct": false,
            "HasHadSolarProduct": false,
            "HasMatchingEmail": false,
            "HasPAYGProduct": false,
            "HasSolarProduct": false,
            "IsFromHubCX": true,
            "IsNewlyCreated": false,
            "LastActivityTime": null,
            "LastLoginTime": null,
            "LastName": "Last",
            "MobileNumber": "0400000000",
            "Premises": [
                {
                    "AccountStatus": "BILL",
                    "ActualBalance": -73.71,
                    "Address": "1 EXAMPLE ST HOBART 7000 TAS",
                    "AmountOwed": 0.0,
                    "AverageDailyUsage": 4.33,
                    "BalanceLastUpdatedDate": "2025-12-23T13:00:00+00:00",
                    "BillDue": null,
                    "BillFrom": null,
                    "BillId": "18337887",
                    "BillIdToPay": null,
                    "BillNextRun": "2026-01-09T13:00:00+00:00",
                    "BillNextTo": "2026-01-06T13:00:00+00:00",
                    "BillOverDueAmount": 0.0,
                    "BillTo": null,
                    "BillTotalAmount": 0.0,
                    "ConcessionDetail": null,
                    "CurrentAppExperience": null,
                    "CurrentTimeOfUse": null,
                    "CurrentTimeOfUsePeriodEndDate": null,
                    "CurrentTimeOfUseType": null,
                    "EstimatedBalance": -81.29,
                    "HasActivePaymentExtension": false,
                    "HasActivePaymentPlans": false,
                    "HasConcessionsApplied": null,
                    "HasExplicitInformedConsent": null,
                    "HasInterimStatus": false,
                    "HasOffProductStatus": false,
                    "HasOnProductStatus": true,
                    "HasPAYGPlus": false,
                    "HasSolar": true,
                    "IsActive": true,
                    "LastMeterReadDate": null,
                    "LifeSupport": "N",
                    "Meters": [
                        {
                            "BadgeNumber": null,
                            "MeterID": "8000000100",
                            "MeterType": "COMMS4D",
                            "NMI": "8000000100",
                            "NetworkTarriffs": null
                        }
                    ],
                    "NumberOfUnpaidBills": 0,
                    "ParentAccountID": "100100010",
                    "ParentAccountNumber": "100100010",
                    "ParentAccountNumberCheckDigit": "4",
                    "ParentPremiseID": "100100010",
                    "PostCode": "7000",
                    "ServiceAgreementID": "100100010",
                    "ServiceAgreementOfferNumber": "TERST010",
                    "ServiceAgreementStartDate": "2021-10-06T13:00:00+00:00",
                    "ServiceAgreementStatus": "Stopped",
                    "ServiceAgreementType": "Residential",
                    "Status": null,
                    "SubmissionTime": null,
                    "Suburb": "HOBART",
                    "UnbilledAmount": -73.71,
                    "UnbilledAmountAsAt": "2025-12-23T13:00:00+00:00",
                    "UsageDaysRemaining": 0
                },
                {
                    "AccountStatus": "BILL",
                    "ActualBalance": -73.71,
                    "Address": "1 EXAMPLE ST HOBART 7000 TAS",
                    "AmountOwed": 0.0,
                    "AverageDailyUsage": 4.33,
                    "BalanceLastUpdatedDate": "2025-12-23T13:00:00+00:00",
                    "BillDue": null,
                    "BillFrom": null,
                    "BillId": "18337887",
                    "BillIdToPay": null,
                    "BillNextRun": "2026-01-09T13:00:00+00:00",
                    "BillNextTo": "2026-01-06T13:00:00+00:00",
                    "BillOverDueAmount": 0.0,
                    "BillTo": null,
                    "BillTotalAmount": 0.0,
                    "ConcessionDetail": null,
                    "CurrentAppExperience": null,
                    "CurrentTimeOfUse": null,
                    "CurrentTimeOfUsePeriodEndDate": null,
                    "CurrentTimeOfUseType": null,
                    "EstimatedBalance": -81.29,
                    "HasActivePaymentExtension": false,
                    "HasActivePaymentPlans": false,
                    "HasConcessionsApplied": null,
                    "HasExplicitInformedConsent": null,
                    "HasInterimStatus": false,
                    "HasOffProductStatus": false,
                    "HasOnProductStatus": true,
                    "HasPAYGPlus": true,
                    "HasSolar": true,
                    "IsActive": true,
                    "LastMeterReadDate": null,
                    "LifeSupport": "N",
                    "Meters": [
                        {
                            "BadgeNumber": null,
                            "MeterID": "8000000100",
                            "MeterType": "COMMS4D",
                            "NMI": "8000000100",
                            "NetworkTarriffs": null
                        }
                    ],
                    "NumberOfUnpaidBills": 0,
                    "ParentAccountID": "100100010",
                    "ParentAccountNumber": "100100010",
                    "ParentAccountNumberCheckDigit": "4",
                    "ParentPremiseID": "100100010",
                    "PostCode": "7000",
                    "ServiceAgreementID": "100100010",
                    "ServiceAgreementOfferNumber": "TERAP010",
                    "ServiceAgreementStartDate": "2023-05-18T14:00:00+00:00",
                    "ServiceAgreementStatus": "Active",
                    "ServiceAgreementType": "Residential",
                    "Status": null,
                    "SubmissionTime": null,
                    "Suburb": "HOBART",
                    "UnbilledAmount": -73.71,
                    "UnbilledAmountAsAt": "2025-12-23T13:00:00+00:00",
                    "UsageDaysRemaining": 0
                }
            ],
            "ProductLevel": null,
            "Title": "MR",
            "UnreadNotificationsCount": null,
            "lifeSupport": false
        }
    """)


@pytest.fixture
def usage_day_response() -> str:
    return dedent("""
        {
            "EndDate": "2025-12-25T13:00:00Z",
            "HasSolarTariff": true,
            "MeteredUsageRecords": [
                {
                    "DollarValueUsage": {
                        "T140": -0.791609,
                        "T93OFFPEAK": 2.568006,
                        "T93PEAK": 1.972943
                    },
                    "EndTime": "2025-12-25T13:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": null,
                    "KilowattHourUsageAEST": null,
                    "StartTime": "2025-12-24T13:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Day"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-24T14:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.0, "T93OFFPEAK": 0.539},
                    "KilowattHourUsageAEST": {"T140": 0.0, "T93OFFPEAK": 1.232},
                    "StartTime": "2025-12-24T13:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-24T15:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.0, "T93OFFPEAK": 1.232},
                    "KilowattHourUsageAEST": {"T140": 0.0, "T93OFFPEAK": 2.323},
                    "StartTime": "2025-12-24T14:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-24T16:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.0, "T93OFFPEAK": 2.323},
                    "KilowattHourUsageAEST": {"T140": 0.0, "T93OFFPEAK": 2.159},
                    "StartTime": "2025-12-24T15:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-24T17:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.0, "T93OFFPEAK": 2.159},
                    "KilowattHourUsageAEST": {"T140": 0.0, "T93OFFPEAK": 0.955},
                    "StartTime": "2025-12-24T16:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-24T18:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.0, "T93OFFPEAK": 0.955},
                    "KilowattHourUsageAEST": {"T140": 0.0, "T93OFFPEAK": 0.983},
                    "StartTime": "2025-12-24T17:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-24T19:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.0, "T93OFFPEAK": 0.983},
                    "KilowattHourUsageAEST": {"T140": 0.0, "T93OFFPEAK": 0.74},
                    "StartTime": "2025-12-24T18:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-24T20:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.0, "T93OFFPEAK": 0.74},
                    "KilowattHourUsageAEST": {"T140": 0.036, "T93OFFPEAK": 0.106},
                    "StartTime": "2025-12-24T19:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-24T21:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.036, "T93OFFPEAK": 0.106},
                    "KilowattHourUsageAEST": {"T140": 0.394, "T93PEAK": 0.032},
                    "StartTime": "2025-12-24T20:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-24T22:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.394, "T93PEAK": 0.032},
                    "KilowattHourUsageAEST": {"T140": 0.719, "T93PEAK": 0.574},
                    "StartTime": "2025-12-24T21:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-24T23:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.719, "T93PEAK": 0.574},
                    "KilowattHourUsageAEST": {"T140": 1.916, "T93PEAK": 0.076},
                    "StartTime": "2025-12-24T22:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-25T00:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 1.916, "T93PEAK": 0.076},
                    "KilowattHourUsageAEST": {"T140": 2.178, "T93OFFPEAK": 0.073},
                    "StartTime": "2025-12-24T23:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-25T01:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 2.178, "T93OFFPEAK": 0.073},
                    "KilowattHourUsageAEST": {"T140": 1.266, "T93OFFPEAK": 0.36},
                    "StartTime": "2025-12-25T00:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-25T02:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 1.266, "T93OFFPEAK": 0.36},
                    "KilowattHourUsageAEST": {"T140": 0.523, "T93OFFPEAK": 2.036},
                    "StartTime": "2025-12-25T01:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-25T03:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.523, "T93OFFPEAK": 2.036},
                    "KilowattHourUsageAEST": {"T140": 1.061, "T93OFFPEAK": 0.674},
                    "StartTime": "2025-12-25T02:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-25T04:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 1.061, "T93OFFPEAK": 0.674},
                    "KilowattHourUsageAEST": {"T140": 0.655, "T93OFFPEAK": 0.721},
                    "StartTime": "2025-12-25T03:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-25T05:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.655, "T93OFFPEAK": 0.721},
                    "KilowattHourUsageAEST": {"T140": 0.247, "T93OFFPEAK": 1.132},
                    "StartTime": "2025-12-25T04:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-25T06:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.247, "T93OFFPEAK": 1.132},
                    "KilowattHourUsageAEST": {"T140": 0.003, "T93PEAK": 1.239},
                    "StartTime": "2025-12-25T05:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-25T07:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.003, "T93PEAK": 1.239},
                    "KilowattHourUsageAEST": {"T140": 0.016, "T93PEAK": 0.772},
                    "StartTime": "2025-12-25T06:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-25T08:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.016, "T93PEAK": 0.772},
                    "KilowattHourUsageAEST": {"T140": 0.0, "T93PEAK": 0.532},
                    "StartTime": "2025-12-25T07:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-25T09:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.0, "T93PEAK": 0.532},
                    "KilowattHourUsageAEST": {"T140": 0.0, "T93PEAK": 1.145},
                    "StartTime": "2025-12-25T08:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-25T10:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.0, "T93PEAK": 1.145},
                    "KilowattHourUsageAEST": {"T140": 0.0, "T93PEAK": 1.191},
                    "StartTime": "2025-12-25T09:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-25T11:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.0, "T93PEAK": 1.191},
                    "KilowattHourUsageAEST": {"T140": 0.0, "T93OFFPEAK": 0.696},
                    "StartTime": "2025-12-25T10:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-25T12:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.0, "T93OFFPEAK": 0.696},
                    "KilowattHourUsageAEST": {"T140": 0.0, "T93OFFPEAK": 0.682},
                    "StartTime": "2025-12-25T11:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                },
                {
                    "DollarValueUsage": null,
                    "EndTime": "2025-12-25T13:00:00Z",
                    "HasSubstitutedData": false,
                    "KilowattHourUsage": {"T140": 0.0, "T93OFFPEAK": 0.682},
                    "KilowattHourUsageAEST": {"T140": 0.0, "T93OFFPEAK": 0.518},
                    "StartTime": "2025-12-25T12:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Hour"
                }
            ],
            "NoDataDayThresholdExceededFlag": false,
            "NoDataFlag": false,
            "NonMeteredUsageRecords": [
                {
                    "Description": "Supply Charge - Residential Time of Use - Tariff 93",
                    "DollarAmount": 1.511814,
                    "EndTime": "2025-12-25T13:00:00Z",
                    "StartTime": "2025-12-24T13:00:00Z",
                    "TimeMeasureCount": 1,
                    "TimeMeasureUnit": "Day"
                }
            ],
            "ServiceAgreementID": "100100010",
            "ServiceAgreements": {
                "100100010": {
                    "EndDate": "0001-01-01T00:00:00",
                    "Id": "100100010",
                    "IsPaygServiceAgreement": true,
                    "PremiseName": "1 EXAMPLE ST HOBART 7000",
                    "PremiseSuburb": "HOBART",
                    "Solar": true,
                    "StartDate": "2023-05-18T14:00:00+00:00",
                    "Status": "A",
                    "Type": "TERAP010"
                }
            },
            "StartDate": "2025-12-24T13:00:00Z",
            "SummaryTotals": {
                "DayContainsSubstitutedUsage": false,
                "DollarValueUsage": {
                    "Other": 1.511814,
                    "T140": -0.791609,
                    "T93OFFPEAK": 2.568006,
                    "T93PEAK": 1.972943,
                    "Total": 5.261153
                },
                "HasDailyBillSegments": false,
                "KilowattHourUsage": {
                    "T140": 9.014,
                    "T93OFFPEAK": 15.39,
                    "T93PEAK": 5.561,
                    "Total": 29.965
                }
            },
            "TariffTypes": ["T140", "T93OFFPEAK", "T93PEAK"],
            "TimeMeasureCount": 1,
            "TimeMeasureUnit": "Day"
        }
    """)


@pytest.fixture
def usage_week_response() -> str:
    return dedent("""
       {
        "EndDate": "2025-12-21T13:00:00Z",
        "HasSolarTariff": true,
        "MeteredUsageRecords": [
            {
                "DollarValueUsage": {
                    "T140": -0.753496,
                    "T93OFFPEAK": 1.505596,
                    "T93PEAK": 1.806905
                },
                "EndTime": "2025-12-15T13:00:00Z",
                "HasSubstitutedData": false,
                "KilowattHourUsage": {"T140": 8.58, "T93OFFPEAK": 9.023, "T93PEAK": 5.093},
                "KilowattHourUsageAEST": null,
                "StartTime": "2025-12-14T13:00:00Z",
                "TimeMeasureCount": 1,
                "TimeMeasureUnit": "Day"
            },
            {
                "DollarValueUsage": {
                    "T140": -2.070356,
                    "T93OFFPEAK": 1.683638,
                    "T93PEAK": 1.655413
                },
                "EndTime": "2025-12-16T13:00:00Z",
                "HasSubstitutedData": false,
                "KilowattHourUsage": {
                    "T140": 23.575,
                    "T93OFFPEAK": 10.09,
                    "T93PEAK": 4.666
                },
                "KilowattHourUsageAEST": null,
                "StartTime": "2025-12-15T13:00:00Z",
                "TimeMeasureCount": 1,
                "TimeMeasureUnit": "Day"
            },
            {
                "DollarValueUsage": {
                    "T140": -1.214112,
                    "T93OFFPEAK": 1.671123,
                    "T93PEAK": 2.998617
                },
                "EndTime": "2025-12-17T13:00:00Z",
                "HasSubstitutedData": false,
                "KilowattHourUsage": {
                    "T140": 13.825,
                    "T93OFFPEAK": 10.015,
                    "T93PEAK": 8.452
                },
                "KilowattHourUsageAEST": null,
                "StartTime": "2025-12-16T13:00:00Z",
                "TimeMeasureCount": 1,
                "TimeMeasureUnit": "Day"
            },
            {
                "DollarValueUsage": {
                    "T140": -0.452449,
                    "T93OFFPEAK": 2.067587,
                    "T93PEAK": 2.905665
                },
                "EndTime": "2025-12-18T13:00:00Z",
                "HasSubstitutedData": false,
                "KilowattHourUsage": {
                    "T140": 5.152,
                    "T93OFFPEAK": 12.391,
                    "T93PEAK": 8.19
                },
                "KilowattHourUsageAEST": null,
                "StartTime": "2025-12-17T13:00:00Z",
                "TimeMeasureCount": 1,
                "TimeMeasureUnit": "Day"
            },
            {
                "DollarValueUsage": {
                    "T140": -0.077896,
                    "T93OFFPEAK": 1.768403,
                    "T93PEAK": 2.993296
                },
                "EndTime": "2025-12-19T13:00:00Z",
                "HasSubstitutedData": false,
                "KilowattHourUsage": {
                    "T140": 0.887,
                    "T93OFFPEAK": 10.598,
                    "T93PEAK": 8.437
                },
                "KilowattHourUsageAEST": null,
                "StartTime": "2025-12-18T13:00:00Z",
                "TimeMeasureCount": 1,
                "TimeMeasureUnit": "Day"
            },
            {
                "DollarValueUsage": {"T140": -1.599466, "T93OFFPEAK": 3.202249},
                "EndTime": "2025-12-20T13:00:00Z",
                "HasSubstitutedData": false,
                "KilowattHourUsage": {"T140": 18.213, "T93OFFPEAK": 19.191},
                "KilowattHourUsageAEST": null,
                "StartTime": "2025-12-19T13:00:00Z",
                "TimeMeasureCount": 1,
                "TimeMeasureUnit": "Day"
            },
            {
                "DollarValueUsage": {"T140": -1.348476, "T93OFFPEAK": 3.287181},
                "EndTime": "2025-12-21T13:00:00Z",
                "HasSubstitutedData": false,
                "KilowattHourUsage": {"T140": 15.355, "T93OFFPEAK": 19.7},
                "KilowattHourUsageAEST": null,
                "StartTime": "2025-12-20T13:00:00Z",
                "TimeMeasureCount": 1,
                "TimeMeasureUnit": "Day"
            }
        ],
        "NoDataDayThresholdExceededFlag": false,
        "NoDataFlag": false,
        "NonMeteredUsageRecords": [
            {
                "Description": "Supply Charge - Residential Time of Use - Tariff 93",
                "DollarAmount": 10.582698,
                "EndTime": "2025-12-21T13:00:00Z",
                "StartTime": "2025-12-14T13:00:00Z",
                "TimeMeasureCount": 1,
                "TimeMeasureUnit": "Week"
            }
        ],
        "ServiceAgreementID": "100100010",
        "ServiceAgreements": {
            "100100010": {
                "EndDate": "0001-01-01T00:00:00",
                "Id": "100100010",
                "IsPaygServiceAgreement": true,
                "PremiseName": "1 EXAMPLE ST HOBART 7000",
                "PremiseSuburb": "HOBART",
                "Solar": true,
                "StartDate": "2023-05-18T14:00:00+00:00",
                "Status": "A",
                "Type": "TERAP010"
            }
        },
        "StartDate": "2025-12-14T13:00:00Z",
        "SummaryTotals": {
            "DayContainsSubstitutedUsage": false,
            "DollarValueUsage": {
                "Other": 10.582698,
                "T140": -7.51625,
                "T93OFFPEAK": 15.185777,
                "T93PEAK": 12.359895,
                "Total": 30.61212
            },
            "HasDailyBillSegments": false,
            "KilowattHourUsage": {
                "T140": 85.587,
                "T93OFFPEAK": 91.008,
                "T93PEAK": 34.838,
                "Total": 211.433
            }
        },
        "TariffTypes": ["T140", "T93OFFPEAK", "T93PEAK"],
        "TimeMeasureCount": 1,
        "TimeMeasureUnit": "Week"
    }
    """)


@pytest.fixture
def mock_api_request(
    current_response: str,
    premises_response: str,
    usage_day_response: str,
    usage_week_response: str,
) -> requests_mock.Mocker:
    m = requests_mock.Mocker()

    m.get(_aurora_url("customers/current"), text=current_response)
    # m.get(_aurora_url("customers/current"), text=current_response)
    m.get(_aurora_url("customers/premises"), text=premises_response)

    m.get(
        _aurora_url(
            "usage/day?serviceAgreementID=100100010&customerId=100100001&index=-1"
        ),
        text=usage_day_response,
    )
    m.get(
        _aurora_url(
            "usage/week?serviceAgreementID=100100010&customerId=100100001&index=-1"
        ),
        text=usage_week_response,
    )

    return m
def _aurora_url(endpoint: str) -> str:
    return AuroraPlusApi.API_URL + "/" + endpoint
