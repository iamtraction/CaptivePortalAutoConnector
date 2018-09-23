import configparser
from selenium import webdriver
import sys


config = configparser.ConfigParser()
config.read('configurations.ini')


def get_config(section, field):
    """Returns the value of the specified field in the parsed config file.

    Args:
        section: A section in the parsed config file
        field: A configiguration field in the parsed config file.

    Returns:
        A string containing the value of the specified field in the specified
        section of the parsed config file.
    """
    if section in config and field in config[section]:
        return config[section][field]
    else:
        return None


def get_default_browser(platform):
    """Returns the default pre-installed browser for the specified platform.

    Args:
        platform: A string representing the current platform. preferably, the
            returned value of `sys.platform`.

    Returns:
        A string representing the slug of the default browser pre-installed in
        the specified platform.
    """
    if platform.startswith('linux'):
        return 'firefox'
    elif platform == 'darwin':
        return 'safari'
    elif platform == 'win32':
        return 'ie'
    else:
        return None


def get_webdriver(browser):
    """Returns the WebDriver for the specified browser.

    Args:
        platform: A string representing browser for which the WebDriver should
            be returned.

    Returns:
        The WebDriver for the specified browser.
    """
    browser = browser.lower()

    # If no browser is specifid, use the default browser pre-installed with
    # the operating system.
    if not browser:
        browser = get_default_browser(sys.platform)

    if browser == 'chrome':
        return webdriver.Chrome()
    elif browser == 'firefox':
        return webdriver.Firefox()
    elif browser == 'ie' or browser == 'internetexplorer':
        return webdriver.Ie()
    elif browser == 'opera':
        return webdriver.Opera()
    elif browser == 'safari':
        return webdriver.Safari()
    else:
        return None


captive_portal_url = get_config('Environment', 'captive_portal_url') \
    or 'http://localhost'
username_field_name = get_config('Environment', 'username_field_name') \
    or 'username'
password_field_name = get_config('Environment', 'password_field_name') \
    or 'password'
login_button_name = get_config('Environment', 'login_button_name') \
    or 'login'
username = get_config('Credentials', 'username')
password = get_config('Credentials', 'password')
web_driver = get_webdriver(get_config('Default', 'browser'))


# Check if a WebDriver was set successfully.
if not web_driver:
    print("Error:\tUnable to bind to any browser.")
    print("\tPlease specify a browser in the configurations.ini file.")

    print("\nExiting...")
    sys.exit(1)


# Connect to the Captive Portal.
try:
    web_driver.get(captive_portal_url)
except Exception:
    # Connection to the Captive Portal failed.
    print("Error:\tUnable to connect to the Captive Portal.")
    print("\tPlease verify the URL in the configurations.ini file.")

    print("\nExiting...")

    # Close the browser.
    web_driver.close()

    sys.exit(1)


# Clear Username & Password fields. They might be automatically filled by
# autocomplete.
username_field = web_driver.find_element_by_name(username_field_name)
username_field.clear()

password_field = web_driver.find_element_by_name(password_field_name)
password_field.clear()

# Send the Username & Password (specified in the config file), to the input
# fields of the Captive Portal.
password_field.send_keys(username)
password_field.send_keys(password)

# Emulate the click of the Login button in the Captive Portal.
web_driver.find_element_by_name(login_button_name).click()


print("Success:\tLogged in to the Captive Portal.")


# Close the browser after successfully logging in.
web_driver.close()
