from logging.handlers import TimedRotatingFileHandler
import logging.handlers as handlers
import logging
import datetime
import os

def intialize_logging():
    console_display = False
    file_write = True
    debug_level = "DEBUG"

    if debug_level == 'DEBUG':
        _level = logging.DEBUG

    if debug_level == 'INFO':
        _level = logging.INFO

    # setting common value
    logger = logging.getLogger()
    logger.setLevel(_level)
    formatter = logging.Formatter('%(asctime)s : %(message)s',
                              "%Y-%m-%d %H:%M:%S")

    # remove all previous added handler
    # if present
    # print(logger.hasHandlers())
    while logger.hasHandlers():
        logger.removeHandler(logger.handlers[0])

    # again add them accordingly
    if console_display:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    if file_write:
        date = datetime.date.today()
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y",)
        # timestamp = datetime.datetime.now().strftime("%H-%M-%S")
        log_path = os.path.join(os.getcwd())
        # if not os.path.exists(log_path):
        #     os.makedirs(log_path)

        # file_handler = logging.FileHandler(filename = log_path + '/' + timestamp + '.log')
        file_handler = TimedRotatingFileHandler(
            filename=log_path + '/' + timestamp + '.log', when="midnight", interval=1)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

intialize_logging()
logging.debug(f"Timeout - Enabling camera restart functionality")