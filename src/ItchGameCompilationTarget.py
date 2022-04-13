# Does the submission.html
from src.ParsedContents import ParsedContents
from src.CompilationTarget import CompilationTarget
from pathlib import Path

# import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from decouple import config


class ItchGameCompilationTarget(CompilationTarget):
    @classmethod
    def uploadToItch(cls, parsedContents: ParsedContents):
        # selenium.
        browser: Chrome
        with Chrome() as browser:
            browser.get("https://itch.io/login")
            username: WebElement = browser.find_element(By.NAME, "username")
            username.send_keys(config("ITCH_USERNAME"))

            password: WebElement = browser.find_element(By.NAME, "password")
            password.send_keys(config("ITCH_PASSWORD"))

            form: WebElement = browser.find_element(
                By.CSS_SELECTOR, ".login_form_widget form"
            )
            form.submit()
            import time

            time.sleep(1000)

    # @classmethod
    # def compileDescription(cls, data: object) -> str:
    #     pass
    #
    # @classmethod
    # # I suppose this is where the Itch API would come in...butler and such??
    # def compileDescriptionToFile(cls, data: object, outputFile: Path) -> None:
    #     contents = cls.compileDescription(data)
    #     with open(outputFile, "w") as file:
    #         file.write(contents)
