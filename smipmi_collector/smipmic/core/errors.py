class SmipmicException(Exception):
    pass

class CommandError(SmipmicException):
    pass

class MessageParseError(SmipmicException):
    pass

class NotImplementedError(SmipmicException):
    pass

class MessageParsingError(SmipmicException):
    pass

class MessageHasUnknownInstanceError(SmipmicException):
    pass

class ApplicationExit(SmipmicException):
    pass
