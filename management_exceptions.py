
class IncorrectFormattedDateAndTime(ValueError):
    """
        This class is used to create an erorr if the date and time is not formatted correctly.
    """
    def __init__(self, *args, **kwargs):
        """
        This is used to initialise the class.
        """
        ValueError.__init__(self, *args, **kwargs)

class FormattedTimeAndDateError(ValueError):
    """
        This class is used to create an erorr if the date and time is not formatted correctly.
    """
    def __init__(self, *args, **kwargs):
        """
        This is used to initialise the class.
        """
        ValueError.__init__(self, *args, **kwargs)

class FormattedUserError(ValueError):
    """
        This class is used to create an erorr if the user is not formatted correctly.
    """
    def __init__(self, *args, **kwargs):
        """
        This is used to initialise the class.
        """
        ValueError.__init__(self, *args, **kwargs)

class BookingError(ValueError):
    """
        A Generic custom error for booking.
    """
    def __init__(self, *args, **kwargs):
        """
        This is used to initialise the class.
        """
        ValueError.__init__(self, *args, **kwargs)

class FailedToLoginToUser(ValueError):
    """
        This is used to raise an error when the user fails to login.
    """
    def __init__(self, *args, **kwargs):
        """
        This is used to initialise the class.
        """
        ValueError.__init__(self, *args, **kwargs)

class BookingSaveError(ValueError):
    """
        This is used to raise an error when the user fails to login.
    """
    def __init__(self, *args, **kwargs):
        """
        This is used to initialise the class.
        """
        ValueError.__init__(self, *args, **kwargs)
class PermissionDeniedToCreateAccount(ValueError):
    """
        This is used to raise an error when the user fails to create an account.
    """
    def __init__(self, *args, **kwargs):
        """
        This is used to initialise the class.
        """
        ValueError.__init__(self, *args, **kwargs)


class PermissionDenied(SystemError):
    """
        This is used to raise an error when the user does not have permission to do something.
    """
    def __init__(self, *args, **kwargs):
        """
        This is used to initialise the class.
        """
        SystemError.__init__(self, *args, **kwargs)

class InvalidAccountLevel(ValueError):
    """
        This is used to raise an error when the user does not have the correct account level.
    """
    def __init__(self, *args, **kwargs):
        """
        This is used to initialise the class.
        """
        ValueError.__init__(self, *args, **kwargs)

class FailedToMakeUserInstance(ValueError):
    """
        This is used to raise an error when the user fails to make a user instance.
    """
    def __init__(self, *args, **kwargs):
        """
        This is used to initialise the class.
        """
        ValueError.__init__(self, *args, **kwargs)


class PasswordValidationError(ValueError):
    """
        This is used to raise an error when the user fails to validate their password.
    """
    def __init__(self, *args, **kwargs):
        """
        This is used to initialise the class.
        """
        ValueError.__init__(self, *args, **kwargs)

class ManagementSetupFailure(SystemError):
    """
    Used to notify the user if the file has not
    correctly setup.
    """

    def __init__(self, *args, **kwargs):
        """
        This is used to initialise the class.
        """
        SystemError.__init__(self, *args, **kwargs)
