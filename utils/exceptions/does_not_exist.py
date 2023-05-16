from typing import Optional


class DoesNotExist(Exception):
    """Exception raised for errors in empty queryset (response) from DB.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: Optional[str] = "Matching query does not exist."):
        self.message = message
        super().__init__(self.message)
