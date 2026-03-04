from termcolor import colored


def error(message: str, show_emoji: bool = True) -> None:
    """
    Prints an error message.

    Args:
        message (str): The error message
        show_emoji (bool): Whether to show the marker

    Returns:
        None
    """
    marker = "[X]" if show_emoji else ""
    print(colored(f"{marker} {message}", "red"))


def success(message: str, show_emoji: bool = True) -> None:
    """
    Prints a success message.

    Args:
        message (str): The success message
        show_emoji (bool): Whether to show the marker

    Returns:
        None
    """
    marker = "[OK]" if show_emoji else ""
    print(colored(f"{marker} {message}", "green"))


def info(message: str, show_emoji: bool = True) -> None:
    """
    Prints an info message.

    Args:
        message (str): The info message
        show_emoji (bool): Whether to show the marker

    Returns:
        None
    """
    marker = "[i]" if show_emoji else ""
    print(colored(f"{marker} {message}", "magenta"))


def warning(message: str, show_emoji: bool = True) -> None:
    """
    Prints a warning message.

    Args:
        message (str): The warning message
        show_emoji (bool): Whether to show the marker

    Returns:
        None
    """
    marker = "[!]" if show_emoji else ""
    print(colored(f"{marker} {message}", "yellow"))


def question(message: str, show_emoji: bool = True) -> str:
    """
    Prints a question message and returns the user's input.

    Args:
        message (str): The question message
        show_emoji (bool): Whether to show the marker

    Returns:
        user_input (str): The user's input
    """
    marker = "[?]" if show_emoji else ""
    return input(colored(f"{marker} {message}", "magenta"))
