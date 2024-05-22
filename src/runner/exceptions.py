class CustomException(Exception):
    pass


class ElementNotFoundException(CustomException):
    pass


class OperationAlreadyDoneException(CustomException):
    pass


class ElementNotAvailableException(CustomException):
    pass
