

import loguru

from utils.Singleton import Singleton

class Log(metaclass=Singleton):
    def __init__(self, log_name='tars.log') -> None:
        self.logger = loguru.logger
        self.logger.add(log_name, rotation="10 MB")

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)


    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)


    def critical(self, message):
        self.logger.critical(message)
