# BibleHelp translator

This script takes BibleHelp booklets in English and referring to KJV bible quotes and translates them into a given target language.

## Prerequisites:

- python3 (tested with 3.10.6)

You need a DeepL auth key. Sign up for a "DeepL API Free" account [here](deepl.com), then go to "Account" and scroll down and copy the authentication key.
Next, export that as an environment variable, for example by adding this to your `~/.bashrc` and then starting a new terminal:

```
export DEEPL_AUTH_KEY='put-your-key-here-not-this-text:fx'
```

Since it should stay confidential, remember not to share that bashrc file with others if you do that. Alternatively, you can put the key at the front of your commandline whenever you run the script, e.g. `DEEPL_AUTH_KEY='asdfljasdf' ./biblehelp_translator.py ...etc`.

First use wget to download 50 MB of booklets:

```
wget -r https://biblehelpsinc.org/
```

## Usage:

```
./biblehelp_translator.py biblehelpsinc.org/publication/a-broken-and-contrite-heart/index.html --language=it
```

That should give you some files in output/it/ - an html that renders something if you open it in the browser, and a pdf.
