"""
Common exceptions for the API.
"""
from rest_framework.exceptions import APIException


class BloodlinkAPIException(APIException):
    """Base exception for Bloodlink API."""
    status_code = 500
    default_detail = 'An error occurred'


class InvalidBloodGroupException(BloodlinkAPIException):
    """Raised when an invalid blood group is provided."""
    status_code = 400
    default_detail = 'Invalid blood group'


class LocationNotProvidedException(BloodlinkAPIException):
    """Raised when location is not provided."""
    status_code = 400
    default_detail = 'Location coordinates are required'
