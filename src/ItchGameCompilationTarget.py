# Does the submission.html
from src.ParsedContents import ParsedContents
from src.CompilationTarget import CompilationTarget
from pathlib import Path
from src.TemplateEvaluator import TemplateEvaluator, TemplateFileEnum

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
            isNewGame: bool = False
            if not cls.gameExists(browser, parsedContents):
                browser.get("https://itch.io/game/new")
                isNewGame = True

            cls.fillData(browser, parsedContents, isNewGame)
            # TODO figure out what to do at this point
            time.sleep(1000)

    @classmethod
    def getDescriptionHtml(cls, parsedContents: ParsedContents) -> str:
        return TemplateEvaluator.evaluateTemplateToString(
            parsedContents=parsedContents,
            template=TemplateFileEnum.ITCH_GAME_DESCRIPTION_MD,
        )

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
    def fillData(cls, browser, parsedContents: ParsedContents, isNewGame: bool):
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

        descriptionTextArea.send_keys(
            cls.getDescriptionHtml(parsedContents=parsedContents)
        )
        # TODO use isNewGame to provide zip. But idk

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
    def gameExists(cls, browser, parsedContents: ParsedContents) -> bool:
        browser.get(TemplateEvaluator.constructItchLink(parsedContents=parsedContents))
        try:
            editGameElement: WebElement = browser.find_element(
                By.CSS_SELECTOR, 'a[href^="https://itch.io/game/edit/"]'
            )
            editGameElement.click()
            return True

        except NoSuchElementException:
            try:
                browser.find_element(By.CSS_SELECTOR, ".not_found_game_page")
            except NoSuchElementException:
                raise Exception(
                    "Unknown situation. Game does not seem to exist but we do not seem to be on the 404 page either"
                )

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
