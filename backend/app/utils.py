import validators


def validate_url(url: str) -> None:
    """
    Validates whether a given string is a valid URL.

    Args:
        url (str): The URL string to validate

    Raises:
        ValueError: If the URL is invalid according to URL formatting standards

    Returns:
        None
    """
    valid = validators.url(url)
    if not valid:
        raise ValueError("The provided url is invalid")
