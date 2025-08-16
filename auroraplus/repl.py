#!/bin/env python

import code
import json
import logging
import os
import sys

import auroraplus
from auroraplus.get_token import get_token

log_level = logging.DEBUG
logger = logging.getLogger(__name__)

AURORAPLUS_ACCESS_TOKEN = "AURORAPLUS_ACCESS_TOKEN"
AURORAPLUS_ID_TOKEN = "AURORAPLUS_ID_TOKEN"
AURORAPLUS_TOKEN = "AURORAPLUS_TOKEN"


def repl():
    logging.basicConfig(level=log_level)

    access_token = os.getenv(AURORAPLUS_ACCESS_TOKEN)
    id_token = os.getenv(AURORAPLUS_ID_TOKEN)
    token = None
    if token_json := os.getenv(AURORAPLUS_TOKEN):
        try:
            token = json.loads(token_json)
        except json.JSONDecodeError:
            logger.warning(f"{AURORAPLUS_TOKEN} is not valid JSON")

    if not any([token, id_token, access_token]):
        logger.info(
            f"All of {AURORAPLUS_TOKEN}, {AURORAPLUS_ID_TOKEN} and {AURORAPLUS_ACCESS_TOKEN} environment variables are empty, requesting interactively ..."
        )
        id_token = get_token()

    try:
        api = auroraplus.AuroraPlusApi(
            token=token, id_token=id_token, access_token=access_token
        )
        api.get_info()
    except Exception as exc:
        logger.exception("exception when setting up", exc_info=exc)
    sys.ps1 = "AuroraPlus >>> "
    code.interact(
        local=locals(),
        banner="\nInitialised AuroraPlus API object available as `api`.\n",
    )


if __name__ == "__main__":
    repl()
