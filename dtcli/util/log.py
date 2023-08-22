from colorama import init, Fore, Style

# Initialize colorama on Windows
init(autoreset=True)

def success(message):
    success_message = f"{Fore.GREEN}{Style.BRIGHT}SUCCESS: {message}{Style.RESET_ALL}"
    print(success_message)

def warning(message):
    warning_message = f"{Fore.YELLOW}{Style.BRIGHT}WARNING: {message}{Style.RESET_ALL}"
    # print(warning_message)

def error(message):
    error_message = f"{Fore.RED}{Style.BRIGHT}ERROR: {message}{Style.RESET_ALL}"
    # print(error_message)

def info(message):
    info_message = f"{Fore.WHITE}{Style.BRIGHT}INFO: {message}{Style.RESET_ALL}"
    print(info_message)
