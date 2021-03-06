import os
import shutil
import time
from os import path
from typing import Union
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from whatsapp.support.validate import check_attribute, check_element


class Login(object):
    driver: webdriver = None
    phone: str = None
    force: bool = False

    def __init__(self, phone: str) -> None:
        self.phone = phone

    def save_user_qr(self, element, path) -> None:
        element.screenshot(path)

    def login_user(self) -> Union[bool, Exception]:
        print("INFO: prepare qr code name")
        qr_code_name = path.join(os.getcwd(), "qr_codes", "%s.png" % self.phone)
        last_qr_code_ref = None

        try:
            qr_code_scanned = False

            while not qr_code_scanned:
                print("INFO: wait qr code to be scanned")
                time.sleep(1)

                if not check_element(self.driver, By.CSS_SELECTOR, ".landing-wrapper"):
                    qr_code_scanned = True

                if not check_element(
                    self.driver,
                    By.XPATH,
                    '//*[@id="app"]/div[1]/div/div[2]/div[1]/div/div[2]',
                ):
                    continue

                if not check_element(
                    self.driver,
                    By.XPATH,
                    '//*[@id="app"]/div[1]/div/div[2]/div[1]/div/div[2]/div',
                ):
                    continue

                if check_element(
                    self.driver,
                    By.XPATH,
                    '//*[@id="app"]/div[1]/div/div[2]/div[1]/div/div[2]/div/span/button',
                ):
                    qr_code_reload = self.driver.find_element(
                        By.XPATH,
                        '//*[@id="app"]/div[1]/div/div[2]/div[1]/div/div[2]/div/span/button',
                    )
                    qr_code_reload.click()

                    time.sleep(0.5)
                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    '//*[@id="app"]/div[1]/div/div[2]/div[1]/div/div[2]/div',
                                )
                            )
                        )
                    except TimeoutException as e:
                        if path.exists(qr_code_name):
                            os.remove(qr_code_name)

                        return [False, TimeoutException("QR Load timeout")]

                if not check_element(
                    self.driver,
                    By.XPATH,
                    '//*[@id="app"]/div[1]/div/div[2]/div[1]/div/div[2]/div',
                ):
                    continue

                qr_code = self.driver.find_element(
                    By.XPATH, '//*[@id="app"]/div[1]/div/div[2]/div[1]/div/div[2]/div'
                )
                if not check_attribute(qr_code, "data-ref"):
                    continue

                qr_code_ref = qr_code.get_attribute("data-ref")
                if last_qr_code_ref == qr_code_ref:
                    continue

                last_qr_code_ref = qr_code_ref

                time.sleep(1)
                self.save_user_qr(qr_code, qr_code_name)

                print("Please scan your QR Code")

            try:
                time.sleep(5)

                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[4]')
                    )
                )
            except TimeoutException as e:
                if path.exists(qr_code_name):
                    os.remove(qr_code_name)

                return [False, TimeoutException("Login process takes to much time")]
            except Exception as e:
                if path.exists(qr_code_name):
                    os.remove(qr_code_name)

                return [False, Exception("Login process takes to much time")]

            print("Successfully logged in")
            if path.exists(qr_code_name):
                os.remove(qr_code_name)

            return [True, None]
        except Exception as e:
            return [False, e]

    def check_session_exists(
        self, profile_dir: str, force: bool
    ) -> Union[bool, str, Exception]:
        if path.exists(profile_dir):
            if not force:
                return [False, "You already logged in.", None]

            try:
                shutil.rmtree(profile_dir)
            except Exception as e:
                return [False, "There is an error while deleting directory", e]

        return [True, None, None]

    def login(self, force: bool = False) -> Union[str, Exception]:
        try:
            if self.phone[0] == "0":
                return [
                    "Phone format should looks like this, [area][phone] => 628123xxxxxx",
                    Exception("PhoneFormatNotValid"),
                ]

            profile_dir = path.join(os.getcwd(), "profile", self.phone)
            success = False

            [
                session_status,
                session_message,
                session_error,
            ] = self.check_session_exists(profile_dir, force)
            if not session_status:
                return [session_message, session_error]

            os.mkdir(profile_dir)

            options = webdriver.FirefoxOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--window-size=1920x1080")
            options.add_argument("-profile")
            options.add_argument(profile_dir)

            while not success:
                self.driver = webdriver.Firefox(options=options)

                print("INFO: get whatsapp web page")
                self.driver.get("https://web.whatsapp.com")

                [success, error] = self.login_user()
                if not success:
                    self.driver.close()

                    if error:
                        if hasattr(error, "message"):
                            print("WARNING: %s" % error.message)
                        else:
                            print("WARNING: %s" % error)
                    continue

            self.driver.close()
            return ["You have successfully logged in", None]
        except Exception as e:
            if self.driver:
                self.driver.close()
            return ["There is an Error", e]


if __name__ == "__main__":
    try:
        Login("081327693570")
    except KeyboardInterrupt:
        print("\rProgram stop running!")
