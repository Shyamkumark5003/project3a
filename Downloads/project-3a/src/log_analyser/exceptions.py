"""Log Analyser"""


class LogAnalyserError(Exception):
    """Log Analyser Exception"""


class LogFileNotFoundError(LogAnalyserError):
    """Log Not Found Exception"""


class MalformedLineError(LogAnalyserError):
    """Malformed Log Exception"""
