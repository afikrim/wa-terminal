import os
import json
import re
import time
from os import path
from typing import Union
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchAttributeException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def check_element(driver, by, locator):
    try:
        driver.find_element(by, locator)

        return True
    except NoSuchElementException:
        return False


def check_attribute(element, attribute):
    try:
        attribute = element.get_attribute(attribute)

        return True if attribute else False
    except NoSuchAttributeException:
        return False


def message_user(driver) -> Union[bool, Exception, bool]:
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-icon="send"]'))
        )
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-icon="send"]'))
        )
    except TimeoutException as e:
        if check_element(
            driver,
            By.CSS_SELECTOR,
            'div.overlay.copyable-area[data-animate-modal-backdrop="true"] div[data-animate-modal-popup="true"] div[data-animate-modal-body="true"] div:nth-child(1)',
        ):
            modal_message = driver.find_element(
                By.CSS_SELECTOR,
                'div.overlay.copyable-area[data-animate-modal-backdrop="true"] div[data-animate-modal-popup="true"] div[data-animate-modal-body="true"] div:nth-child(1)',
            ).get_attribute("innerText")

            return [False, Exception(modal_message), True]

        return [False, e, False]

    time.sleep(2)
    if check_element(driver, By.CSS_SELECTOR, '[data-icon="send"]'):
        send_icon = driver.find_element(By.CSS_SELECTOR, '[data-icon="send"]')
        send_button = send_icon.find_element(By.XPATH, "..")

        try:
            send_button.click()

            return [True, None, False]
        except Exception as e:
            return [False, e, False]

    return [False, None, False]


def message(sender: str, destination: str, text: str) -> Union[str, Exception]:
    try:
        if sender[0] == "0":
            return [
                "Phone format should looks like this, [area][phone] => 628123xxxxxx",
                Exception("PhoneFormatNotValid"),
            ]

        profile_dir = path.join(os.getcwd(), "profile", sender)
        success = False

        if not path.exists(profile_dir):
            return [
                "You haven't logged in yet, please login first",
                Exception("NotLogIn"),
            ]

        options = webdriver.FirefoxOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("-profile")
        options.add_argument(profile_dir)

        while not success:
            driver = webdriver.Firefox(options=options)
            driver.get(
                "https://web.whatsapp.com/send/?phone=%s&text=%s" % (destination, text)
            )

            [success, error, throwable] = message_user(driver)
            if not success:
                driver.close()

                if error:
                    error_message = None
                    if hasattr(error, "message"):
                        error_message = error.message
                    else:
                        error_message = error

                    if throwable:
                        return [error_message, error]
                continue

        driver.close()
        return ["Your message successfully sent", None]
    except Exception as e:
        if driver:
            driver.close()
        return ["There is an Error", e]


if __name__ == "__main__":
    try:
        message()
    except KeyboardInterrupt:
        print("\rProgram stop running!")
