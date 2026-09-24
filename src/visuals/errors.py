class VisulisationError(Exception):
    """Raised when the rendering state is inconsistent."""
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
