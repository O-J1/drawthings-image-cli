import os
from pathlib import Path
import tomllib
import tomli_w
import dtcli.constants
import dtcli.util.log as log


def check_output_folder_exists():
    """Checks if folder for img out exists and if not creates"""

    # Check if the folder exists and create it if not
    if not dtcli.constants.FOLDER_PATH.exists():
        dtcli.constants.FOLDER_PATH.mkdir(exist_ok=True)
        log.success(f"Output folder has been created at: {dtcli.constants.FOLDER_PATH}")
    else:
        log.info("Output folder already exists, skipping")

def check_config_template_exists():
    """Checks if config file (that users can edit) exists and if not creates"""

    # Check if the TOML file exists
    if dtcli.constants.CONFIG_PATH.exists():
        log.info(f"The file '{dtcli.constants.CONFIG_FILENAME}' exists.")
    else:
        # Create a valid TOML file if it doesn't exist
        toml_data = dtcli.constants.CONFIG_TEMPLATE

        with dtcli.constants.CONFIG_PATH.open(mode="wb") as toml_file:
            tomli_w.dump(toml_data, toml_file)
            log.success(f"The file '{dtcli.constants.CONFIG_FILENAME}' has been created with default DrawThings values")

        with dtcli.constants.CONFIG_PATH.open(mode="rb") as f:
            data = tomllib.load(f)
            #print(data)
            log.success(f"{dtcli.constants.CONFIG_FILENAME} is valid TOML syntax, success") 

check_config_template_exists()
check_output_folder_exists()
