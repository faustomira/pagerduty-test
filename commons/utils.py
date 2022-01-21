import logging
import os
from datetime import datetime

def setup_logging():
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)

    dttime_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    fileHandler = logging.FileHandler(os.path.join("logs", f"exec_{dttime_str}.log"))
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    rootLogger.log

    return rootLogger
