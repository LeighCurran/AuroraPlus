#!/bin/env python

import code
import logging
import os
import sys

import auroraplus
from auroraplus.get_token import get_token

log_level = logging.DEBUG
logger = logging.getLogger(__name__)

AURORAPLUS_ID_TOKEN = "AURORAPLUS_ID_TOKEN"


def repl():
    logging.basicConfig(level=log_level)
    if not (id_token := os.getenv(AURORAPLUS_ID_TOKEN)):
        logger.info(
            f"{AURORAPLUS_ID_TOKEN} environment variable unset or empty, requesting interactively ..."
        )
        id_token = get_token()

    api = auroraplus.AuroraPlusApi(id_token=id_token)
    api.get_info()
    sys.ps1 = "AuroraPlus >>> "
    code.interact(
        local=locals(),
        banner="\nInitialised AuroraPlus API object available as `api`.\n",
    )


if __name__ == "__main__":
    repl()
