# Does the submission.html
from src.ParsedContents import ParsedContents, CartType
from src.CompilationTarget import CompilationTarget
from pathlib import Path
from src.TemplateEvaluator import TemplateEvaluator, TemplateFileEnum
from selenium.webdriver.common.keys import Keys

# import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    UnexpectedAlertPresentException,
    NoSuchWindowException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from decouple import config
import time
import subprocess


class ItchGameCompilationTarget(CompilationTarget):
    @classmethod
    def uploadToItch(cls, parsedContents: ParsedContents, exportFolder: Path):
        # TODO handle windows
        result = subprocess.run(["open", str(exportFolder)])
        if result.returncode != 0:
            raise Exception("Error - unable to open file location")

        with open(
            '/Users/nathandunn/Projects/p8export3/p8export-fresh/template/template-retuls.temp'
        , 'w') as output:
            output.write(cls.getItchDescription(parsedContents))

        # selenium.
        browser: Chrome
        with Chrome(executable_path=config("CHROMEEXE")) as browser:
            cls.login(browser)
            isNewGame: bool = False
            if not cls.gameExists(browser, parsedContents):
                browser.get("https://itch.io/game/new")
                isNewGame = True

            cls.fillData(browser, parsedContents, isNewGame)
            # print('ok whenever you are ready')
            input("press enter after you close the browser")
            # while True:
            #     try:
            #         print('selecting body')
            #         x = browser.find_element(By.CSS_SELECTOR, 'body')
            #         y = x
            #     except NoSuchWindowException:
            #         break
            #     except:
            #         pass
            #     time.sleep(1)
            # print('detected browser close')

    @classmethod
    def getItchDescription(cls, parsedContents: ParsedContents) -> str:
        template: TemplateFileEnum = TemplateEvaluator.getItchTemplate(
            cartType=parsedContents.metadata.stronglyTypedCartType
        )
        return TemplateEvaluator.evaluateTemplateToString(
            parsedContents=parsedContents,
            template=template,
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
        slug: WebElement = cls.pollForSelector(
            browser=browser, selector='[name="game[slug]"]'
        )
        # slug.clear()
        slug.send_keys(Keys.CONTROL + "a")
        slug.send_keys(Keys.DELETE)
        slug.send_keys(parsedContents.metadata.correctedGameSlug)

        title: WebElement = cls.pollForSelector(
            browser=browser, selector='[name="game[title]"]'
        )
        title.clear()
        title.send_keys(parsedContents.metadata.game_name)

        tagline: WebElement = cls.pollForSelector(
            browser=browser, selector='[name="game[short_text]"]'
        )
        tagline.clear()
        tagline.send_keys(parsedContents.metadata.tagline)

        noPayments: WebElement = cls.pollForSelector(
            browser=browser, selector=".payment_mode_disable_payments"
        )
        noPayments.click()

        # TODO make these better
        try:
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
        except:
            pass

        descriptionHtmlButton: WebElement = cls.pollForSelector(
            browser=browser, selector='.redactor-toolbar a[aria-label="HTML"]'
        )
        descriptionHtmlButton.click()
        descriptionTextArea: WebElement = cls.pollForSelector(
            browser=browser, selector=".redactor-box textarea.open"
        )
        descriptionTextArea.clear()
        descriptionTextArea.send_keys(
            cls.getItchDescription(parsedContents=parsedContents)
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
