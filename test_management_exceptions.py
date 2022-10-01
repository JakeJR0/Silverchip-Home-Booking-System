"""
    This file contains all the exceptions used within the management module.
"""

import pytest

from management_exceptions import IncorrectFormattedDateAndTime, FormattedTimeAndDateError
from management_exceptions import FormattedUserError, BookingError, FailedToLoginToUser
from management_exceptions import PermissionDeniedToCreateAccount, PermissionDenied
from management_exceptions import InvalidAccountLevel, FailedToMakeUserInstance
from management_exceptions import PasswordValidationError, ManagementSetupFailure

def test_incorrect_formatted_date_and_time():
    """
        This tests the IncorrectFormattedDateAndTime class.
    """
    with pytest.raises(IncorrectFormattedDateAndTime):
        raise IncorrectFormattedDateAndTime("Test")

def test_formatted_time_and_date_error():
    """
        This tests the FormattedTimeAndDateError class.
    """
    with pytest.raises(FormattedTimeAndDateError):
        raise FormattedTimeAndDateError("Test")

def test_formatted_user_error():
    """
        This tests the FormattedUserError class.
    """
    with pytest.raises(FormattedUserError):
        raise FormattedUserError("Test")

def test_booking_error():
    """
        This tests the BookingError class.
    """
    with pytest.raises(BookingError):
        raise BookingError("Test")

def test_failed_to_login_to_user():
    """
        This tests the FailedToLoginToUser class.
    """
    with pytest.raises(FailedToLoginToUser):
        raise FailedToLoginToUser("Test")

def test_permission_denied_to_create_account():
    """
        This tests the PermissionDeniedToCreateAccount class.
    """
    with pytest.raises(PermissionDeniedToCreateAccount):
        raise PermissionDeniedToCreateAccount("Test")

def test_permission_denied():
    """
        This tests the PermissionDenied class.
    """
    with pytest.raises(PermissionDenied):
        raise PermissionDenied("Test")

def test_invalid_account_level():
    """
        This tests the InvalidAccountLevel class.
    """
    with pytest.raises(InvalidAccountLevel):
        raise InvalidAccountLevel("Test")

def test_failed_to_make_user_instance():
    """
        This tests the FailedToMakeUserInstance class.
    """
    with pytest.raises(FailedToMakeUserInstance):
        raise FailedToMakeUserInstance("Test")

def test_password_validation_error():
    """
        This tests the PasswordValidationError class.
    """
    with pytest.raises(PasswordValidationError):
        raise PasswordValidationError("Test")

def test_management_setup_failure():
    """
        This tests the ManagementSetupFailure class.
    """
    with pytest.raises(ManagementSetupFailure):
        raise ManagementSetupFailure("Test")
