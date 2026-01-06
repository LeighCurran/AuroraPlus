import requests_mock

from auroraplus import AuroraPlusApi
from tests.consts import CUSTOMER_ID, PREMISE_ADDRESS, SERVICE_AGREEMENT_ID


def test_get_info(api: AuroraPlusApi, mock_api_request: requests_mock.Mocker):
    with mock_api_request:
        api.get_info()

    assert api.customerId == CUSTOMER_ID
    assert api.premiseAddress == PREMISE_ADDRESS
    assert api.serviceAgreementID == SERVICE_AGREEMENT_ID


def test_getcurrent(api: AuroraPlusApi, mock_api_request: requests_mock.Mocker):
    with mock_api_request:
        api.get_info()
        api.getcurrent()

    assert api.ActualBalance == "-73.71"
    assert api.AmountOwed == "0.00"
    assert api.AverageDailyUsage == "4.33"
    assert api.BillOverDueAmount == "0.00"
    assert api.BillTotalAmount == "0.00"
    assert api.EstimatedBalance == "-81.56"
    assert api.NumberOfUnpaidBills == 0
    assert api.UnbilledAmount == "-73.71"
    assert api.UsageDaysRemaining == 0


def test_getday(api: AuroraPlusApi, mock_api_request: requests_mock.Mocker):
    with mock_api_request:
        api.get_info()
        api.getday()

    assert api.day
    assert "StartDate" in api.day
    assert "MeteredUsageRecords" in api.day

    for mur in api.day["MeteredUsageRecords"]:
        assert "StartTime" in mur
        assert "EndTime" in mur
        assert "DollarValueUsage" in mur
        assert "KilowattHourUsage" in mur


def test_getweek(api: AuroraPlusApi, mock_api_request: requests_mock.Mocker):
    with mock_api_request:
        api.get_info()
        api.getweek()

    assert api.week
    assert "TariffTypes" in api.week
    assert "T93PEAK" in api.week["TariffTypes"]
    assert "T93OFFPEAK" in api.week["TariffTypes"]
    assert "T140" in api.week["TariffTypes"]
