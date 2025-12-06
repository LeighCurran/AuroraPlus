#!/usr/bin/env python

import json
import logging
import os

import auroraplus

logging.basicConfig(level="DEBUG")

token = os.environ.get("AURORAPLUS_TOKEN")
id_token = os.environ.get("AURORAPLUS_ID_TOKEN")

if not token and not id_token:
    raise Exception("Neither AURORAPLUS_TOKEN nor AURORAPLUS_ID_TOKEN exist in the environment")

if token:
    print("Using AURORAPLUS_TOKEN...")
    api=auroraplus.AuroraPlusApi(token=json.loads(token))

if id_token:
    print("Using AURORAPLUS_ID_TOKEN...")
    api=auroraplus.AuroraPlusApi(id_token=id_token)

breakpoint()
api.get_info()
print(api.serviceAgreementID)
