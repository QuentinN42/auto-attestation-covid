""" Selenium example

Use the https://attestation-covid.web.app/ website to generate pdf.

"""
from os import getenv
import json
from pathlib import Path
from time import sleep
import shutil

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def json_load(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def get_pdf():
    pdfs = list(Path(".").glob("*.pdf"))
    if not pdfs:
        return None
    else:
        return pdfs[0]


def generate_todo():
    di = dict()
    env_vars_str = json_load(Path("env_vars_str.json"))
    env_vars_bool = json_load(Path("env_vars_bool.json"))
    for var in env_vars_str:
        di[var] = getenv(var.upper(), "")
    for var in env_vars_bool:
        di[var] = True if getenv(var.upper()) == "1" else False
    return di


class Filler:
    def __init__(self, driver: WebDriver, xpaths_file: Path = Path("xpaths.json")):
        self.driver = driver
        self.xpaths: dict = json_load(xpaths_file)

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


class Worker:
    def __init__(self, filler: Filler, todo: dict):
        self.filler: Filler = filler
        self.todo: dict = todo

    def generate(self):
        self.filler.validate("generate")

    def work_one(self, field, action):
        if action is True:
            self.filler.validate(field)
        elif isinstance(action, str) and action != "":
            self.filler.fill(field, action)

    def work(self):
        for field, action in self.todo.items():
            self.work_one(field, action)
        self.generate()


def main(driver: WebDriver):
    driver.get("https://attestation-covid.web.app/")
    filler = Filler(driver)
    todo = generate_todo()
    worker = Worker(filler, todo)
    worker.work()
    while get_pdf() is None:
        sleep(0.1)
    shutil.move(str(get_pdf()), Path("./out/"))


if __name__ == '__main__':
    from selenium import webdriver
    from dotenv import load_dotenv
    load_dotenv()
    main(webdriver.Chrome())
