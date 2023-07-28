#!/usr/bin/env python3
""" Turns bible help in html into html page and a pdf after optionally translating from English"""

# Note: you should first do wget -r https://biblehelpsinc.org/ to get the booklets in html form

import argparse
import glob
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import deepl
from bs4 import BeautifulSoup, Comment, NavigableString

parser = argparse.ArgumentParser(
    description="Turn bible help into optionally translated html page and pdf"
)

parser.add_argument(
    "filename",
    metavar="filename",
    type=str,
    help="input html page from https://biblehelpsinc.org/publications/publication-list/",
)
parser.add_argument(
    "--prefix", type=str, default="html/html_prefix.html", help="prefix html file"
)
parser.add_argument(
    "--postfix", type=str, default="html/html_postfix.html", help="postfix html file"
)
parser.add_argument(
    "--language", type=str, default="nl", help="language code for DeepL"
)

translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])

args = parser.parse_args()

# for example: biblehelpsinc.org/publication/a-broken-and-contrite-heart/index.html
source_html_file = args.filename

lang = args.language
output_dir = Path(f"./output/{lang}/")
output_dir.mkdir(parents=True, exist_ok=True)
booklet_title = source_html_file[30:][:-11]

output_pdf = (output_dir / booklet_title).with_suffix(".pdf")
output_html = output_pdf.with_suffix(".html")

tmp_output_html = "output.html"
tmp_output_pdf = "output.pdf"

strings_translated = 0


# leave_untranslated = ["PO Box 391", "Hanover, PA 17331"]


def translate(text_element):
    global strings_translated
    if isinstance(text_element, Comment):
        return
    # if text_element.string in leave_untranslated:
    #     return
    if len(text_element) > 0 and not str.isspace(text_element):
        text = str(translator.translate_text(text_element, target_lang=lang))
        # text = "String: " + str(text_element)
        text_element.string.replace_with(text)
        strings_translated += 1


# ensure footer exists for given language
footer_file_name = f"./html/footers/{lang}.html"
footer_content = ""
if os.path.isfile(footer_file_name):
    print(f"Found existing footer for {lang}.")
    with open(footer_file_name, "r") as footer_file:
        footer_content = footer_file.read()
else:
    print(f"Translating footer for {lang}")
    with open("./html/footers/en.html", "r") as footer_file:
        english_footer_text = footer_file.read()
    footer = BeautifulSoup(english_footer_text, "html.parser")
    for text_element in footer.findAll(text=True):
        text_element = translate(text_element)
    with open(footer_file_name, "w") as footer_file:
        footer_content = footer.prettify()
        footer_file.write(footer.prettify())


with open(source_html_file, "r") as input_html_file:
    content = input_html_file.read()
    # select just the <article> element
    article = BeautifulSoup(content, "html.parser").article
    article.footer.decompose()
    for text_element in article.findAll(text=True):
        translate(text_element)
    content = article.prettify()

with open(args.prefix, "r") as html_preamble:
    html_text = html_preamble.read() + content + footer_content

with open(args.postfix, "r") as html_postfix:
    html_text += html_postfix.read()

with open(tmp_output_html, "w") as html_file:
    html_file.write(html_text)

dirs_to_copy = ["images", "css"]
for dir_to_copy in dirs_to_copy:
    dst_dir = os.path.join(tempfile.gettempdir(), dir_to_copy)
    Path(dst_dir).mkdir(parents=True, exist_ok=True)
    for image in glob.iglob(os.path.join(dir_to_copy, "*")):
        shutil.copy(image, dst_dir)

subprocess.run(
    ["wkhtmltopdf", "--enable-local-file-access", tmp_output_html, tmp_output_pdf]
)

# move tmp to final destinations
os.rename(tmp_output_html, output_html)
os.rename(tmp_output_pdf, output_pdf)

print(f"Translated {strings_translated} strings")
