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


def test_getpowerhours(api: AuroraPlusApi, mock_api_request: requests_mock.Mocker):
    with mock_api_request:
        api.get_info()
        powerhours = api.getpowerhours()

    assert powerhours == api.powerhours
    assert len(powerhours) == 1

    event = powerhours[0]
    assert event["EventName"] == "Power Hours - Test Event"
    assert "OfferExpiryDateTime" in event
    assert event["TimeslotAccepted"]["StartDateTime"] == "2026-08-07T14:00:00"
    assert event["TimeslotAccepted"]["EndDateTime"] == "2026-08-07T16:00:00"

    for slot in event["TimeslotAll"]:
        assert "PowerHourTimeSlotId" in slot
        assert "StartDateTime" in slot
        assert "EndDateTime" in slot
        assert "ExpiryDateTime" in slot


def test_getpowerhours_all(api: AuroraPlusApi, mock_api_request: requests_mock.Mocker):
    with mock_api_request:
        api.get_info()
        powerhours = api.getpowerhours(upcoming_only=False)

    assert len(powerhours) == 1
    assert powerhours[0]["EventName"] == "Power Hours - Test Event"


def test_getpowerhours_no_events(
    api: AuroraPlusApi, mock_api_request: requests_mock.Mocker
):
    with mock_api_request:
        api.get_info()

        mock_api_request.get(
            AuroraPlusApi.API_URL + "/powerhour/upcoming-active",
            status_code=404,
            text='{"Message": "No events"}',
        )
        powerhours = api.getpowerhours()

    assert powerhours == []
    assert api.powerhours == []
