# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class RequiredInput(Error):
    """There should be inputs here"""
    print('Please check for errors')
    pass


class ReactiveOptionsError(Error):
    """Please add options for reaction calculations"""
    pass


class ReactiveConstraintsError(Error):
    """Please add options for reaction calculations"""
    pass
