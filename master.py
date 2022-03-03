from cmath import log
from app import main
from multiprocessing import Process
import time
import os
import requests
import traceback
import logging

from eth import WALLET_ADDRESS
# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logHandler = logging.StreamHandler()
filelogHandler = logging.FileHandler("logs.log")
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logHandler.setFormatter(formatter)
filelogHandler.setFormatter(formatter)
logger.addHandler(filelogHandler)
logger.addHandler(logHandler)


def check_activation():
    url = "https://7857c3e018df.ngrok.io/activation/%s" % WALLET_ADDRESS
    try:
        response = requests.get(url)
        resp_json = response.json()
        if not resp_json["paired"]:
            return False, "", ""
        else:
            return True, resp_json["OWNER_ETH_ADDRESS"], resp_json["COMMUNICATION_PUBLIC_KEY"]
    except:
        traceback.print_exc()
        logger.error("Request to check activation failed.")
        return False, "", ""


if __name__ == "__main__":
    logger.info("Checking activation status")
    IS_PAIRED, OWNER_ETH_ADDRESS, COMMUNICATION_PUBLIC_KEY = check_activation()
    if(IS_PAIRED):
        logger.info("I have been paired by %s" % OWNER_ETH_ADDRESS)
    else:
        logger.info("Not paired yet")

    logger.info("Starting GATT server.")
    os.environ["OWNER_ETH_ADDRESS"] = OWNER_ETH_ADDRESS
    os.environ["COMMUNICATION_PUBLIC_KEY"] = COMMUNICATION_PUBLIC_KEY
    gatt_proc = Process(target=main)
    gatt_proc.start()
    logger.info("GATT Server started.")
    time.sleep(5)
    logger.info("Entering activation check loop")
    try:
        while True:
            _IS_PAIRED, _OWNER_ETH_ADDRESS, _COMMUNICATION_PUBLIC_KEY = check_activation()
            if(_IS_PAIRED != IS_PAIRED or _OWNER_ETH_ADDRESS != OWNER_ETH_ADDRESS or _COMMUNICATION_PUBLIC_KEY != COMMUNICATION_PUBLIC_KEY):
                logger.info("Change detected in activation")
                logger.info("Killing GATT server")
                gatt_proc.terminate()
                gatt_proc.join()
                gatt_proc = None
                logger.info("Killed GATT server")
                os.environ["OWNER_ETH_ADDRESS"] = _OWNER_ETH_ADDRESS
                os.environ["COMMUNICATION_PUBLIC_KEY"] = _COMMUNICATION_PUBLIC_KEY
                IS_PAIRED = _IS_PAIRED
                OWNER_ETH_ADDRESS = _OWNER_ETH_ADDRESS
                COMMUNICATION_PUBLIC_KEY = _COMMUNICATION_PUBLIC_KEY
                logger.info("Starting GATT server.")
                gatt_proc = Process(target=main)
                gatt_proc.start()
                logger.info("GATT Server started.")

            time.sleep(5)

    except KeyboardInterrupt:
        logger.info("Recieved Ctrl-C exit")
        if(gatt_proc):
            logger.info("Killing GATT server")
            gatt_proc.terminate()
            gatt_proc.join()
            logger.info("Killed GATT server")
