
class BaseError(Exception):
    pass

class NoProjectFile(BaseError):
    """ No project file could be located """
    pass
