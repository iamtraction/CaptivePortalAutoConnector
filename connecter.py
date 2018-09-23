import configparser
import sys
import os
from selenium import webdriver

config = configparser.ConfigParser()
config.read('configurations.ini')


def get_config(section, field):
    if section in config and field in config[section]:
        return config[section][field]
    else:
        return None


def get_default_browser(platform):
    if platform.startswith('linux'):
        return 'firefox'
    elif platform == 'darwin':
        return 'safari'
    elif platform == 'win32':
        return 'ie'
    else:
        return None


def get_webdriver(browser):
    browser = browser.lower()

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
webdriver = get_webdriver(get_config('Default', 'browser'))


if not webdriver:
    print("Error:\tUnable to bind to any browser.")
    print("\tPlease specify a browser in the configurations.ini file.")

    print("\nExiting...")
    sys.exit(1)


try:
	webdriver.get(captive_portal_url)
except:
    print("Error:\tUnable to connect to the Captive Portal.")
    print("\tPlease verify the URL in the configurations.ini file.")

    print("\nExiting...")
    webdriver.close()
    sys.exit(1)


username_field = webdriver.find_element_by_name(username_field_name)
username_field.clear()

password_field = webdriver.find_element_by_name(password_field_name)
password_field.clear()

password_field.send_keys(username)
password_field.send_keys(password)

webdriver.find_element_by_name(login_button_name).click()


print("Success:\tLogged in to the Captive Portal.")


webdriver.close()
