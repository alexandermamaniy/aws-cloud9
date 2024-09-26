class MyBaseException(Exception):
    
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return f'MyBaseException: {self.message}'

class AWSBucketCreateException(MyBaseException):
    
    def __init__(self, message: str, error_code: str):
        super().__init__(message)
        self.error_code = error_code

    def __str__(self) -> str:
        return f'AWSBucketCreateException [{self.error_code}]: {self.message}'