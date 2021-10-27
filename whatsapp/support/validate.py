from selenium import webdriver
from selenium.common.exceptions import NoSuchAttributeException, NoSuchElementException
from selenium.webdriver.common.by import By


def check_element(driver: webdriver, by: By, locator: str):
    try:
        driver.find_element(by, locator)

        return True
    except NoSuchElementException:
        return False


def check_attribute(element, attribute: str):
    try:
        attribute = element.get_attribute(attribute)

        return True if attribute else False
    except NoSuchAttributeException:
        return False
