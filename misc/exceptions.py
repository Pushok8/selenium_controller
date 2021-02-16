class WebDriverFileIsNotFoundException(BaseException):
    pass


class SuchBrowserIsNotSupportedError(BaseException):
    pass


class WebDriversDownloadedAutomaticallyWarning(Warning):
    pass


class WebDriversDownloadedInTMPFileWarning(Warning):
    pass