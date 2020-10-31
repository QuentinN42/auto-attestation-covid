""" Selenium example

Use the https://attestation-covid.web.app/ website to generate pdf.

"""
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from json import loads as json_load
from pathlib import Path


class Filler:
    def __init__(self, driver: WebDriver, xpaths_file: Path = Path("xpaths.json")):
        self.driver = driver
        self.xpaths = json_load(xpaths_file.read_text())

    def _get_element(self, field: str) -> WebElement:
        try:
            xpath = self.xpaths[field]
        except AttributeError:
            print(f"Field {field} not found in {self.xpaths.keys}")
            raise
        else:
            return self.driver.find_element_by_xpath(xpath)

    def validate(self, field: str) -> None:
        self._get_element(field).click()

    def fill(self, field: str, content: str) -> None:
        self._get_element(field).send_keys(content)


def main(driver: WebDriver):
    driver.get('https://attestation-covid.web.app/')
    filler = Filler(driver)
