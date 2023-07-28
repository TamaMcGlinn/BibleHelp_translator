#!/usr/bin/env python3
""" Translates bible help Scribus SLA from English"""

import argparse
import glob
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import deepl
from bs4 import BeautifulSoup, Comment, NavigableString

booknames = [
    "ACTS",
    "AMOS",
    "COLOSSIANS",
    "DANIEL",
    "DEUTERONOMY",
    "ECCLESIASTES",
    "EPHESIANS",
    "ESTHER",
    "EXODUS",
    "EZEKIEL",
    "EZRA",
    "GALATIANS",
    "GENESIS",
    "HABAKKUK",
    "HAGGAI",
    "HEBREWS",
    "HOSEA",
    "I CHRONICLES",
    "I CORINTHIANS",
    "II CHRONICLES",
    "II CORINTHIANS",
    "III JOHN",
    "II JOHN",
    "II KINGS",
    "II PETER",
    "II SAMUEL",
    "II THESSALONIANS",
    "II TIMOTHY",
    "I JOHN",
    "I KINGS",
    "I PETER",
    "ISAIAH",
    "I SAMUEL",
    "I THESSALONIANS",
    "I TIMOTHY",
    "JAMES",
    "JEREMIAH",
    "JOB",
    "JOEL",
    "JOHN",
    "JONAH",
    "JOSHUA",
    "JUDE",
    "JUDGES",
    "LAMENTATIONS",
    "LEVITICUS",
    "LUKE",
    "MALACHI",
    "MARK",
    "MATTHEW",
    "MICAH",
    "NAHUM",
    "NEHEMIAH",
    "NUMBERS",
    "OBADIAH",
    "PHILEMON",
    "PHILIPPIANS",
    "PROVERBS",
    "PSALMS",
    "REVELATION",
    "ROMANS",
    "RUTH",
    "SONG OF SOLOMON",
    "TITUS",
    "ZECHARIAH",
    "ZEPHANIAH",
]

parser = argparse.ArgumentParser(
    description="Turn bible help into optionally translated html page and pdf"
)

parser.add_argument(
    "filename",
    metavar="filename",
    type=str,
    help="input sla file",
)
parser.add_argument(
    "--language", type=str, default="nl", help="language code for DeepL"
)

translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])

args = parser.parse_args()

with open(args.filename, "r") as sla_file:
    source_sla = BeautifulSoup(sla_file.read(), "xml")

lang = args.language
output_dir = Path(f"./output/{lang}/")
output_dir.mkdir(parents=True, exist_ok=True)
booklet_title = "431"  # TODO

output_pdf_file = (output_dir / booklet_title).with_suffix(".pdf")
output_sla_file = output_pdf_file.with_suffix(".sla")

strings_translated = 0
last_bible_quote_element = None


def translate(text_element):
    global strings_translated
    text = text_element["CH"]
    if len(text) == 0 or str.isspace(text):
        return
    # text = str(translator.translate_text(text, target_lang=lang))
    text = "String: " + str(text)
    quote = re.findall(r'[“"”].*[“"”]', text)
    if quote:
        print(quote)
    text_element["CH"] = text
    strings_translated += 1


for text_element in source_sla.findAll("ITEXT"):
    translate(text_element)
output_sla = source_sla.prettify()

with open(output_sla_file, "w") as xml_file:
    xml_file.write(output_sla)

print(f"Translated {strings_translated} strings")
