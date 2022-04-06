from src.ParsedContents import Metadata, ControlEnum, ParsedContents

# from File
from src.FileRegistry import TemplateFileEnum
from pathlib import Path


class TemplateEvaluator:
    # @classmethod
    # def evaluateTemplateToString(
    #     cls, parsedContents: ParsedContents, template: TemplateFileEnum
    # ) -> str:
    #     strTemplate: str = template.readText()
    #     return cls.evaluateStringTemplateToString(
    #         parsedContents=parsedContents, strTemplate=strTemplate
    #     )

    @classmethod
    def evaluateStringTemplateToString(
        cls, parsedContents: ParsedContents, strTemplate: str
    ) -> str:
        return strTemplate.format(
            **cls.constructEvaluationDictionary(parsedContents=parsedContents)
        )

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
                    parsedContents=parsedContents, strTemplate=template.readText()
                )
            )

    @classmethod
    def constructEvaluationDictionary(
        cls, parsedContents: ParsedContents
    ) -> dict[str, str]:
        return {
            "description": cls.constructDescription(parsedContents=parsedContents),
            "controls": cls.constructControlDescription(
                metadata=parsedContents.metadata
            ),
        }

    @classmethod
    def constructDescription(cls, parsedContents: ParsedContents):
        template: str = parsedContents.metadata.description
        template = template.replace(
            "$charCount$", str(parsedContents.sourceCodeP8sciiCharCount)
        )
        template = template.replace(
            "$sourceCode$", f"<pre><code>{parsedContents.sourceCode}</code></pre>"
        )
        return template

    # TODO should maybe provide target like XML, HTML, MD, TXT
    @classmethod
    def constructControlDescription(cls, metadata: Metadata) -> str:
        return "\n".join(
            f"{cls.controlToDescription(control.key)} - {control.desc}"
            for control in metadata.controls
        )

    @classmethod
    def controlToDescription(cls, controlEnum: ControlEnum):
        return {ControlEnum.ARROW_KEYS: "Arrow Keys", ControlEnum.X: "X"}[controlEnum]
