"""
Converts EVE-NG labs into securecrt templates
"""
#pylint: disable=C0301
import json
import os
import time
from pathlib import Path

import click
import requests
from jinja2 import Template


# Required headers for json output
headers: dict[str, str] = {"accept": "application/json"}
# Required cookies to get the correct output from eve
cookies: dict[str, str] = {'html5': '-1'}


def to_padded_hex(number: int) -> str:
    """
    Converts the actual ports to the format that securecrt wants in the template
    """
    hex_str = hex(number)[2:]
    padded_hex_str = hex_str.zfill(8)
    return padded_hex_str


def get_current_epoch_time_ms() -> int:
    """
    Needed for various API calls to eveng
    returns current epoch time
    """
    return int(time.time() * 1000)


def login(eve_ip: str, session: requests.Session, eve_username: str, eve_password: str) -> None:
    """
    Logins into EVE, uses the objects request session to save auth token for future requests
    ran during the objects constructor
    """
    # html5 not being set to -1 in payload results in bad responses. The url is http instead of telnet
    data = {"username": eve_username,
            "password": eve_password, 'html5': '-1'}

    response = session.post(
        f"https://{eve_ip}/api/auth/login",
        data=json.dumps(data),
        headers=headers,
        verify=False
    )
    response.raise_for_status()


@click.group
def menu():
    """Menu for click"""


@menu.command("create-templates")
@click.option("--output-directory", help="Where to save the templated sessions", show_default=True, default=f"{os.getenv('APPDATA')}/VanDyke/Config/Sessions", type=click.STRING)
@click.option("--eve-ip", required=True, help="IP for your eve-ng instance- Ex. 192.168.1.241", type=click.STRING)
@click.option("--eve-username", required=True, help="Username for your eve-ng instance- Ex. admin", type=click.STRING)
@click.option("--eve-password", required=True, help="Password for your eve-ng instance- Ex. eve", type=click.STRING)
@click.option("--lab-name", required=True, help="Lab name that you want sessions for- Ex. mylab", type=click.STRING)
def create_templates(output_directory: str, eve_username: str, eve_password: str, eve_ip: str, lab_name: str) -> None: #pylint: disable=R0914
    """
    Makes an api call to eve-ng getting all nodes in a lab

    Uses jinja to template out the device info into securecrt session templates
    """
    # Create and authenticate using a set session
    requests_session = requests.Session()
    login(eve_ip=eve_ip, session=requests_session,
          eve_username=eve_username, eve_password=eve_password)

    lab_url = f"https://{eve_ip}/api/labs/{lab_name}.unl/nodes?={get_current_epoch_time_ms()}"
    response = requests_session.get(
        lab_url, headers=headers, verify=False, cookies=cookies)
    response.raise_for_status()
    with open("securecrt_template.j2", "r", encoding="UTF-8") as securecrt_temp:
        securecrt_template = Template(securecrt_temp.read())

    for device_values in response.json().get("data").values():
        ip, port = device_values.get("url").split("telnet://")[1].split(":")
        hex_port = to_padded_hex(int(port))
        device_name = device_values.get("name")
        templated_session = securecrt_template.render(
            ip=ip,
            port=hex_port
        )
        output_file = Path(output_directory) / device_name

        with open(f"{output_file}.ini", 'w', encoding="UTF-8") as file:
            file.write(templated_session)


if __name__ == "__main__":
    menu()
