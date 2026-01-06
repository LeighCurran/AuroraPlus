import requests_mock
from urllib.parse import urlparse, parse_qs

from auroraplus import AuroraPlusApi


def test_auth(mock_oauth_request: requests_mock.Mocker):
    api = AuroraPlusApi()

    url = api.oauth_authorize()

    parts = urlparse(url)
    assert parts.netloc == "customers.auroraenergy.com.au"
    assert (
        parts.path
        == "/auroracustomers1p.onmicrosoft.com/b2c_1a_sign_in/oauth2/v2.0/authorize"
    )

    query = parse_qs(parts.query)
    assert query["client_id"].pop() == AuroraPlusApi.CLIENT_ID
    assert query["scope"].pop() == "openid profile offline_access"
    assert query["response_type"].pop() == "code"
    assert query["code_challenge_method"].pop() == "S256"
    assert query["state"]

    # XXX: It's a bit shallow, but it tests the overall flow.
    state = "state-from-test"
    code = "code-from-test"

    with mock_oauth_request as m:
        token = api.oauth_redirect(
            f"https://my.auroraenergy.com.au/login/redirect?state={state}&code={code}"
        )

        assert m.request_history

    assert token


def test_id_token(mock_api_request: requests_mock.Mocker):
    api = AuroraPlusApi(token={"id_token": "id_token-from-test"})

    with mock_api_request as m:
        api.get_info()

        assert (
            m.request_history[0].url
            == "https://api.auroraenergy.com.au/api/identity/LoginToken"
        )

        assert (
            m.request_history[1].url
            == "https://api.auroraenergy.com.au/api/customers/current"
        )

        assert api.token.get("access_token") == "accessToken-from-LoginToken"
        assert api.session.token.get("access_token") == "accessToken-from-LoginToken"
