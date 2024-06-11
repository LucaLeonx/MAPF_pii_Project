class CustomException(Exception):
    pass


class EmptyElementException(CustomException):
    pass


class ElementNotFoundException(CustomException):
    pass


class ElementNotAvailableException(CustomException):
    pass


class InvalidElementException(CustomException):
    pass


class DuplicateElementException(CustomException):
    pass


class OperationAlreadyDoneException(CustomException):
    pass
