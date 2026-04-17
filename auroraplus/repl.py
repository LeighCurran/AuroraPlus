#!/bin/env python

import code
import json
import logging
import os
import sys

from .api import AuroraPlusApi

from .get_token import get_token

log_level = logging.DEBUG
logger = logging.getLogger(__name__)

AURORAPLUS_TOKEN = "AURORAPLUS_TOKEN"


def repl():
    logging.basicConfig(level=log_level)

    token = None
    if token_json := os.getenv(AURORAPLUS_TOKEN):
        try:
            token = json.loads(token_json)
        except json.JSONDecodeError:
            logger.warning(f"{AURORAPLUS_TOKEN} is not valid JSON")

    if not token:
        logger.info(
            f"{AURORAPLUS_TOKEN} environment variable is empty, requesting interactively ..."
        )
        token = get_token()

    try:
        api = AuroraPlusApi(token=token)
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
