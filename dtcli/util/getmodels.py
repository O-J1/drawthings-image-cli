"""Contains code anticipating a model list endpoint being made available"""
# Install requests module if needed
import json
import requests
# from dtcli.constants import CONFIG_TEMPLATE
import dtcli.util.log as log

# Function to retrieve available models from the API
def get_available_models(url):
    """Checks available models from the DT endpoint"""

    response = requests.get(url=f'{url}/sdapi/v1/available_models', timeout=5)

    if response.status_code == 200:
        try:
            available_models = response.json()
            if isinstance(available_models, list):
                return available_models
            else:
                log.warning("API response is not a list")
        except json.JSONDecodeError as error:
            log.error(f"Error decoding JSON: {error}")
    elif response.status_code == 404:
        log.warning("No model list endpoint available, either has not been implemented yet or server is down.\nProceeding with manual list for user input") # pylint: disable=line-too-long
    else:
        log.warning(f"API request failed with status code: {response.status_code}")

    return []  # Return an empty list in case of errors
