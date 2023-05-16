class ValidationError(Exception):
    """
    Custom validation error for handling exceptions in internal logic
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
