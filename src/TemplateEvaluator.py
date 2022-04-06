from ParsedContents import Metadata, ControlEnum, ParsedContents

# from File


class TemplateEvaluator:

    # @classmethod
    # def evaluateTemplateToString(cls, parsedContents: ParsedContents, ):
    #
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
            "$charCount$", parsedContents.sourceCodeP8sciiCharCount
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
        return {ControlEnum.ARROW: "Arrow Keys", ControlEnum.X: "X"}[controlEnum]
