from LocalLogger import LocalLogger
from RemoteLogger import RemoteLogger

class Logger(object):
    def __init__(self):
        super().__init__()
        self.rem_logger = RemoteLogger()
        self.loc_logger = LocalLogger()

logger = Logger()
