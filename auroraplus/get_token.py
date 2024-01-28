#!/bin/env python

import auroraplus


def get_token():
    api = auroraplus.api()
    url = api.oauth_authorize()

    print("Please visit the following URL in a browser, "
          "and follow the login prompts ...\n")
    print(url)

    print("\nThis will redirect to an error page (Cradle Mountain).\n")

    redirect_uri = input("Please enter the full URL of the error page: ")

    token = api.oauth_redirect(redirect_uri)

    print("\nThe new token is\n")
    print(token)

    print("\n The access token is\n")
    print(token['access_token'])


if __name__ == "__main__":
    get_token()
