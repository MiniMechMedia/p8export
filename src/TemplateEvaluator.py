from src.ParsedContents import Metadata, ControlEnum, ParsedContents, CartType

# from File
from src.FileRegistry import TemplateFileEnum
from pathlib import Path
from markdown import markdown
from enum import Enum, auto
import jinja2
import string


class RenderType(Enum):
    # just a basic string replacement
    BASIC = auto()
    HTML = auto()


filters = {}


def registerFilter(func):
    filters[func.__name__] = func


@registerFilter
def htmlSafeSource(content):
    ret = []
    for c in content:
        if c in string.printable:
            ret.append(c)
        else:
            ret.append(f"&#{ord(c)};")

    return "".join(ret)


class TemplateEvaluator:
    @classmethod
    def getRenderTypeFromTemplate(cls, template: TemplateFileEnum) -> RenderType:
        if str(template.value).endswith(".html.md"):
            return RenderType.HTML
        return RenderType.BASIC

    @classmethod
    def getItchTemplate(cls, cartType: CartType):
        return (
            TemplateFileEnum.TWEET_ITCH_DESCRIPTION_TEMPLATE
            if cartType == CartType.TWEET
            else TemplateFileEnum.GAME_ITCH_DESCRIPTION_TEMPLATE
        )

    @classmethod
    def getReadmeTemplate(cls, cartType: CartType):
        return (
            TemplateFileEnum.TWEET_GITHUB_README_TEMPLATE
            if cartType == CartType.TWEET
            else TemplateFileEnum.GAME_GITHUB_README_TEMPLATE
        )

    @classmethod
    def evaluateTemplateToString(
        cls, parsedContents: ParsedContents, template: TemplateFileEnum
    ) -> str:
        strTemplate: str = template.readText()
        return cls.evaluateStringTemplateToString(
            parsedContents=parsedContents,
            strTemplate=strTemplate,
            renderType=cls.getRenderTypeFromTemplate(template=template),
        )

    @classmethod
    def evaluateStringTemplateToString(
        cls, parsedContents: ParsedContents, strTemplate: str, renderType: RenderType
    ) -> str:
        root = (Path(__file__) / ".." / "..").resolve() / "template"
        # print('checkhere',root)
        templateFileName = "asdfasdfasdf.temp"
        temporaryTemplateFile = root / templateFileName
        with open(temporaryTemplateFile, "w") as file:
            file.write(strTemplate)

        templateLoader = jinja2.FileSystemLoader(searchpath=root.resolve())
        templateEnv = jinja2.Environment(loader=templateLoader)
        # templateEnv.filters['htmlSafeSource'] = htmlSafeSource
        for key, val in filters.items():
            templateEnv.filters[key] = val
        jinjaTemplate = templateEnv.get_template(templateFileName)

        ret: str = jinjaTemplate.render(
            cls.constructEvaluationDictionary(parsedContents=parsedContents)
        )
        """
                templateLoader = jinja2.FileSystemLoader(searchpath=root.resolve())
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = str(template.filepath)
        jinjaTemplate = templateEnv.get_template(TEMPLATE_FILE)
        # templateVars = {"title": "Test Example",
        #                 "description": "A simple inquiry of function."}
        # return template.render(cls.constructEvaluationDictionary(parsedContents=parsedContents))
        return jinjaTemplate.render({"title":'blah'})
        """

        # ret: str = strTemplate.format(
        #     **cls.constructEvaluationDictionary(parsedContents=parsedContents)
        # )

        # Not sure what the right way is. But let's hack it.
        ret = ret.replace("&#9617;", "░")

        if renderType == RenderType.HTML:
            ret = markdown(ret)

        return ret

    @classmethod
    def evaluateTemplateToFile(
        cls,
        parsedContents: ParsedContents,
        template: TemplateFileEnum,
        outputFile: Path,
    ) -> None:
        with open(outputFile, "w") as file:
            file.write(
                cls.evaluateStringTemplateToString(
                    parsedContents=parsedContents,
                    strTemplate=template.readText(),
                    renderType=cls.getRenderTypeFromTemplate(template=template),
                )
            )

    @classmethod
    def constructEvaluationDictionary(
        cls, parsedContents: ParsedContents
    ) -> dict[str, str]:
        # print('here is the dict')
        # print(parsedContents.metadata.acknowledgements)
        return {
            "acknowledgements": parsedContents.metadata.acknowledgements,
            "description": parsedContents.metadata.description,
            "controls": cls.constructControlDescription(
                metadata=parsedContents.metadata
            ),
            "hints": parsedContents.metadata.hints,
            "jam_info": cls.constructJamInfo(metadata=parsedContents.metadata),
            "about_extra": parsedContents.metadata.about_extra,
            "source_code_link": cls.constructSourceCodeLink(
                parsedContents=parsedContents
            ),
            "code_explainer_link": cls.constructExplainerCodeLink(
                parsedContents=parsedContents
            ),
            "char_count": parsedContents.sourceCodeP8sciiCharCount,
            "minified_code": parsedContents.minifiedSourceCode,
            "clarified_code": parsedContents.clarifiedSourceCode,
            "source_code": parsedContents.sourceCode,
            "game_name": parsedContents.metadata.game_name,
            "itch_link": cls.constructItchLink(parsedContents=parsedContents),
            "alt_text": parsedContents.metadata.img_alt,
            "tag_line": parsedContents.metadata.tagline,
            "cover_path": parsedContents.coverPath,
            "cover_path_abs": parsedContents.coverPathAbs,
            "folder_relative_path": parsedContents.folderRelativePath,
            # TODO deprecate!
            "pico_url": parsedContents.pico8EduUrlMinified,
            "pico_url_minified": parsedContents.pico8EduUrlMinified,
            "pico_url_clarified": parsedContents.pico8EduUrlClarified,
            "number_players": parsedContents.metadata.numberPlayersDesc
            # 'itch_link': cls.constructItchLink(parsedContents=parsedContents)
        }

    # @classmethod
    # def constructDescription(cls, parsedContents: ParsedContents):
    #     template: str = parsedContents.metadata.description
    #     template = template.replace(
    #         "$charCount$", str(parsedContents.sourceCodeP8sciiCharCount)
    #     )
    #     template = template.replace(
    #         "$sourceCode$", f"<pre><code>{parsedContents.sourceCode}</code></pre>"
    #     )
    #     return template

    # TODO should maybe provide target like XML, HTML, MD, TXT
    @classmethod
    def constructControlDescription(cls, metadata: Metadata) -> str:
        ret: str = ""
        for control in metadata.controls:
            controlInputs: str = " / ".join(
                cls.controlToDescription(inp) for inp in control.inputs
            )
            ret += f"* {controlInputs} - {control.desc}\n"

        return ret.removesuffix("\n")

    @classmethod
    def controlToDescription(cls, controlEnum: ControlEnum):
        return {
            ControlEnum.ARROW_KEYS: "Arrow Keys",
            ControlEnum.LEFT_ARROW_KEY: "Left Arrow Key",
            ControlEnum.RIGHT_ARROW_KEY: "Right Arrow Key",
            ControlEnum.UP_ARROW_KEY: "Up Arrow Key",
            ControlEnum.DOWN_ARROW_KEY: "Down Arrow Key",
            ControlEnum.ESDF: "ESDF",
            ControlEnum.X: "X",
            ControlEnum.Z: "Z",
            ControlEnum.P: "P",
            ControlEnum.S: "S",
            ControlEnum.E: "E",
            ControlEnum.D: "D",
            ControlEnum.F: "F",
            ControlEnum.A: "A",
            ControlEnum.Q: "Q",
            ControlEnum.TAB: "Tab",
            ControlEnum.MOUSE: "Mouse",
            ControlEnum.LEFT_CLICK: "Left Click",
            ControlEnum.RIGHT_CLICK: "Right Click",
        }[controlEnum]

    @classmethod
    def constructJamInfo(cls, metadata: Metadata) -> str:
        ret: str = ""
        jam: Metadata.JamInfo
        isFirst = True
        for jam in metadata.jam_info:
            if not isFirst:
                ret += "\n"
            verb = "Created for" if isFirst else "Also submitted to"
            jamName = (
                jam.jam_name
                if jam.jam_number is None
                else f"{jam.jam_name} {jam.jam_number}"
            )
            formattedJamInfo = (
                jamName
                if not jam.correctedJamUrl
                else f"[{jamName}]({jam.correctedJamUrl})"
            )
            ret += f"{verb} {formattedJamInfo}  \n"

            if jam.jam_theme:
                ret += f"Theme: {jam.jam_theme}  \n"

            if jam.jam_name == "TriJam":
                ret += f"Development Time: {metadata.develop_time}  \n"
            elif jam.jam_name == "MiniJam":
                ret += f"Limitation: {jam.minijam_limitation}  \n"

            if jam.jam_extra:
                ret += jam.jam_extra

            isFirst = False

        return ret

    @classmethod
    def constructSourceCodeLink(cls, parsedContents: ParsedContents) -> str:
        baseUrl: str = parsedContents.config.sourceControlRootUrl
        if not baseUrl.endswith("/"):
            baseUrl += "/"

        return baseUrl + parsedContents.metadata.correctedGameSlug

    @classmethod
    def constructExplainerCodeLink(cls, parsedContents: ParsedContents) -> str:
        return f'{cls.constructSourceCodeLink(parsedContents)}#explanation'

    @classmethod
    def constructItchLink(cls, parsedContents):
        return f"https://{parsedContents.config.itchAuthor}.itch.io/{parsedContents.metadata.correctedGameSlug}"
