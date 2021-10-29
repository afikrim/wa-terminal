import os
import re
import time
from os import path
from typing import Union
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from whatsapp.support.validate import check_element


class Message(object):
    driver: webdriver = None
    sender: str = None
    destination: str = None
    text: str = None

    def __init__(self, sender: str, destination: str, text: str) -> None:
        self.sender = sender
        self.destination = destination
        self.text = text

    def message_user(self) -> Union[bool, Exception, bool]:
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-icon="send"]'))
            )
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-icon="send"]'))
            )
        except TimeoutException as e:
            if check_element(
                self.driver,
                By.CSS_SELECTOR,
                'div.overlay.copyable-area[data-animate-modal-backdrop="true"] div[data-animate-modal-popup="true"] div[data-animate-modal-body="true"] div:nth-child(1)',
            ):
                modal_message = self.driver.find_element(
                    By.CSS_SELECTOR,
                    'div.overlay.copyable-area[data-animate-modal-backdrop="true"] div[data-animate-modal-popup="true"] div[data-animate-modal-body="true"] div:nth-child(1)',
                ).get_attribute("innerText")

                return [False, Exception(modal_message), True]

            return [False, e, False]

        time.sleep(2)
        if check_element(self.driver, By.CSS_SELECTOR, '[data-icon="send"]'):
            send_icon = self.driver.find_element(By.CSS_SELECTOR, '[data-icon="send"]')
            send_button = send_icon.find_element(By.XPATH, "..")

            try:
                send_button.click()

                return [True, None, False]
            except Exception as e:
                return [False, e, False]

        return [False, None, False]

    def message(self) -> Union[str, Exception]:
        try:
            if self.sender[0] == "0":
                return [
                    "Phone format should looks like this, [area][phone] => 628123xxxxxx",
                    Exception("PhoneFormatNotValid"),
                ]

            profile_dir = path.join(os.getcwd(), "profile", self.sender)
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
                self.driver = webdriver.Firefox(options=options)
                self.driver.get(
                    "https://web.whatsapp.com/send/?phone=%s&text=%s"
                    % (self.destination, self.text)
                )

                [success, error, throwable] = self.message_user()
                if not success:
                    self.driver.close()

                    if error:
                        error_message = None
                        if hasattr(error, "message"):
                            error_message = error.message
                        else:
                            error_message = error

                        if throwable:
                            return [error_message, error]
                    continue

            self.driver.close()
            return ["Your message successfully sent", None]
        except Exception as e:
            if self.driver:
                self.driver.close()
            return ["There is an Error", e]

    def broadcast(self) -> Union[str, Exception]:
        try:
            destinations = re.sub(r"(\ )+", "", self.destination).split(",")
            profile_dir = path.join(os.getcwd(), "profile", self.sender)
            success = False

            if self.sender[0] == "0":
                return [
                    "Phone format should looks like this, [area][phone] => 628123xxxxxx",
                    Exception("PhoneFormatNotValid"),
                ]

            if not path.exists(profile_dir):
                return [
                    "You haven't logged in yet, please login first",
                    Exception("NotLogIn"),
                ]

            for destination in destinations:
                if destination[0] == "0":
                    return [
                        "%s: Phone format should looks like this, [area][phone] => 628123xxxxxx"
                        % destination,
                        Exception("PhoneFormatNotValid"),
                    ]

            options = webdriver.FirefoxOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--window-size=1920x1080")
            options.add_argument("-profile")
            options.add_argument(profile_dir)

            self.driver = webdriver.Firefox(options=options)
            for destination in destinations:
                success = False
                while not success:
                    self.driver.get(
                        "https://web.whatsapp.com/send/?phone=%s&text=%s"
                        % (destination, self.text)
                    )

                    [success, error, throwable] = self.message_user()
                    if not success:
                        if error:
                            error_message = None
                            if hasattr(error, "message"):
                                error_message = error.message
                            else:
                                error_message = error

                            if throwable:
                                return [error_message, error]
                        continue

            self.driver.close()
            return ["Your message successfully sent", None]
        except Exception as e:
            if self.driver:
                self.driver.close()
            return ["There is an Error", e]


if __name__ == "__main__":
    try:
        Message("6281327693570", "6281327693570", "TEST").message()
    except KeyboardInterrupt:
        print("\rProgram stop running!")
