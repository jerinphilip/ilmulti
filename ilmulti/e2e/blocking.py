from ..meta import ConfigBuildable
from ..utils.language_utils import detect_lang, inject_token


class BlockingTranslator(ConfigBuildable):
    """
    A blocking translator.
    """

    def __init__(self, translator, splitter, tokenizer):
        self.splitter = splitter
        self.tokenizer = tokenizer
        self.translator = translator

    def __call__(self, source, tgt_lang, src_lang=None, detokenize=True):
        """
        Uses splitter -> tokenizer -> translator and lays out the
        interaction.
        """
        if src_lang is None:
            _, src_lang = detect_lang(source)[0]

        lines = self.splitter(source, lang=src_lang)
        tokenized = self.tokenizer.map(lines, lang=src_lang)
        with_target_token = inject_token(tokenized, tgt_lang=tgt_lang)
        export = self.translator(with_target_token)
        export = self._handle_empty_lines_noise(export)
        if detokenize:
            export = self._detokenize(export)
        return export

    def _handle_empty_lines_noise(self, exports):
        _exports = []
        for entry in exports:
            if not entry["src"].strip():
                entry["tgt"] = ""
            _exports.append(entry)
        return _exports

    def _detokenize(self, export):
        _exports = []
        for entry in export:
            for key in ["src", "tgt"]:
                entry[key] = self.tokenizer.inv(entry[key])
            entry["src"] = entry["src"][9:]
            _exports.append(entry)
        return _exports

    @classmethod
    def fromConfig(cls, config):
        from ..registry import build

        built = {}
        for key in config:
            built[key] = build(key, config[key])
        return cls(**built)
