"""{project_name} library."""


def hello(name: str = "World") -> str:
    """Return a greeting message.

    Args:
        name: Name to greet.

    Returns:
        Greeting string.
    """
    return f"Hello, {name}!"
