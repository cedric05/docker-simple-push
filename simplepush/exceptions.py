
class SimplePushException(Exception):
    pass


class TarFileGenerationFileException(SimplePushException):
    pass


class PathNotExists(TarFileGenerationFileException):
    pass


class ArgNotDefined(SimplePushException):
    pass