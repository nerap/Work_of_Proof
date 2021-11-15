import logging

class ColorFormatter(logging.Formatter):
    def __init__(self, fmt="%(asctime)s - Blockchain - %(message)s"):
        super(ColorFormatter, self).__init__(fmt)
        red = '\033[0;31m'
        nc = '\033[0m'
        cyan = '\033[0;96m'

        err_fmt = f"{red}%(asctime)s - Blockchain{nc} - %(message)s"
        info_fmt = f"{cyan}%(asctime)s - Blockchain{nc} - %(message)s"
        self.err = logging.Formatter(err_fmt)
        self.log = logging.Formatter(info_fmt)

    def format(self, record):
        if record.levelno == logging.ERROR:
            return self.err.format(record)
        else:
            return self.log.format(record)
    