# GuitarTabs
The tool translates tabs in syntax described below to a picture.

Usage: `python GuitarTabs.py`

### Tabs syntax

Tabs are displayed in a grid with fixed width. 

A line is devided into 4 selections, each of them containing up to 8 tones.

* tone - s/p (two integers)
	* s - number of string
	* b - position on the string
* multiple tones on a position - tone.tone. ... .tone
* next position in a selection - space
	* up to 8 tones in a selection
* next selection - newline
	* up to 4 selections
* next line - 2x newline

More formally:

```
string := integer [1, 6]
position := integer [1, 20]
tone := string/position
tones := tone.tones | tone
selection := tones selection | tones
line := selection \n line | selection
lines := line \n\n lines | line
```

> Dependencies can be installed:

> * sudo apt-get install librsvg2-bin imagemagick python-poppler-qt4
> * pip install svgwrite
