from typing import List

import deepl
from pathlib import Path
from functools import reduce
import re
import os

with Path("./API_KEY").open("r") as key_h:
    auth_key = key_h.read().strip()

white_space_re = re.compile(r'\s')
translator = deepl.Translator(auth_key)


def reduce_paragraphs(paras: List[str], lines):
    if len(lines) == 0:
        return paras
    if white_space_re.fullmatch(lines[0]):
        paras.append("")
    else:
        paras[-1] += lines[0].strip("\n")
    lines = lines[1:]

    return reduce_paragraphs(paras, lines)


def translate_paragraph(str_in: str) -> str:
    result = translator.translate_text(str_in,
                                     source_lang=deepl.Language.ENGLISH,
                                     target_lang=deepl.Language.GERMAN,
                                     preserve_formatting=True)
    if isinstance(result, deepl.TextResult):
        return result.text
    return result[0].text


if __name__ == '__main__':
    with Path("data/input.md").open("r") as input_handle:
        with Path("data/output.md").open("w") as output_handle:
            input_lines = input_handle.readlines()
            input_ps = reduce_paragraphs([""], input_lines)
            for p in input_ps:
                output_handle.write(f"{translate_paragraph(p)}\n\n")


