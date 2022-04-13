# Does the submission.html
from src.ParsedContents import ParsedContents
from src.CompilationTarget import CompilationTarget
from pathlib import Path

# import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from decouple import config
import time


class ItchGameCompilationTarget(CompilationTarget):
    @classmethod
    def uploadToItch(cls, parsedContents: ParsedContents):
        # selenium.
        browser: Chrome
        with Chrome() as browser:
            cls.login(browser)

            if not cls.gameExists(browser, parsedContents.metadata.correctedGameSlug):
                browser.get("https://itch.io/game/new")

            cls.fillData(browser, parsedContents)
            # TODO figure out what to do at this point
            time.sleep(1000)

    @classmethod
    def pollForSelector(cls, browser: Chrome, selector: str) -> WebElement:
        for i in range(20):
            try:
                print("attempt " + str(i))
                return browser.find_element(By.CSS_SELECTOR, selector)
            except NoSuchElementException:
                time.sleep(0.05)

        raise NoSuchElementException

    @classmethod
    def fillData(cls, browser, parsedContents: ParsedContents):
        tagline: WebElement = cls.pollForSelector(
            browser=browser, selector='[name="game[short_text]"]'
        )
        tagline.send_keys(parsedContents.metadata.tagline)

        descriptionHtmlButton: WebElement = cls.pollForSelector(
            browser=browser, selector='.redactor-toolbar a[aria-label="HTML"]'
        )
        descriptionHtmlButton.click()
        descriptionTextArea: WebElement = cls.pollForSelector(
            browser=browser, selector=".redactor-box textarea.open"
        )
        # TODO use the rendered description
        descriptionTextArea.send_keys(parsedContents.metadata.description)

        width: WebElement = cls.pollForSelector(
            browser=browser, selector='[name="embed[width]"]'
        )
        width.clear()
        width.send_keys("750")
        height: WebElement = cls.pollForSelector(
            browser=browser, selector='[name="embed[height]"]'
        )
        height.clear()
        height.send_keys("680")

        cls.configureCheckBoxes(browser=browser)

    @classmethod
    def configureCheckBoxes(cls, browser: Chrome):
        # Configure checkboxes
        # mobileFriendlyCheck: WebElement = cls.pollForSelector(
        #     browser=browser, selector='[name="embed[mobile_friendly]"]'
        # )
        # TODO do this conditionally based on metadata - maybe we have a mouse only game
        cls.ensureCheckboxChecked(
            browser=browser, selector='[name="embed[mobile_friendly]"]'
        )
        cls.ensureCheckboxChecked(
            browser=browser, selector='[name="embed[mobile_friendly]"]'
        )
        cls.ensureCheckboxChecked(browser=browser, selector='[name="embed[autostart]"]')
        # try:
        #     browser.find_element(
        #         By.CSS_SELECTOR, '[name="embed[mobile_friendly]"]:checked'
        #     )
        # except NoSuchElementException:
        #     mobileFriendlyCheck.click()

    @classmethod
    def ensureCheckboxChecked(cls, browser: Chrome, selector: str):
        checkBox: WebElement = cls.pollForSelector(browser=browser, selector=selector)
        try:
            browser.find_element(By.CSS_SELECTOR, f"{selector}:checked")
        except NoSuchElementException:
            checkBox.click()

    @classmethod
    def getGameUrl(cls, slug: str) -> str:
        return f'https://{config("ITCH_HANDLE")}.itch.io/{slug}'

    @classmethod
    def gameExists(cls, browser, correctedGameSlug) -> bool:
        browser.get(cls.getGameUrl(correctedGameSlug))
        try:
            editGameElement: WebElement = browser.find_element(
                By.CSS_SELECTOR, 'a[href^="https://itch.io/game/edit/"]'
            )
            editGameElement.click()
            return True

        except NoSuchElementException:
            return False

    @classmethod
    def login(cls, browser: Chrome):
        browser.get("https://itch.io/login")
        username: WebElement = browser.find_element(By.NAME, "username")
        username.send_keys(config("ITCH_USERNAME"))

        password: WebElement = browser.find_element(By.NAME, "password")
        password.send_keys(config("ITCH_PASSWORD"))

        form: WebElement = browser.find_element(
            By.CSS_SELECTOR, ".login_form_widget form"
        )
        form.submit()

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
