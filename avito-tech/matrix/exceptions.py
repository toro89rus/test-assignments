class MatrixDownloadError(Exception):
    pass


class MatrixInvalidUrlError(MatrixDownloadError):
    pass


class MatrixConnectionError(MatrixDownloadError):
    pass


class MatrixTimeoutError(MatrixDownloadError):
    pass


class MatrixContentTypeError(MatrixDownloadError):
    pass


class MatrixServerError(MatrixDownloadError):
    pass
