# GuitarTabs
The tool translates tabs in syntax described below to a picture.

Usage: `python GuitarTabs.py`

Tabs are displayed in a grid with fixed width. 

<div align="center">
  <img src="https://raw.githubusercontent.com/mathooo/GuitarTabs/master/pics/front.png"><br><br>
</div>

```python
0/5.2/3 - 3/2.0/6 - 0/3.0/5 - 2/3.1/6 #! Intro start
2/3.0/6 0/3 5/3 9/3.8/6 7/3 5/3.5/6 4/3 2/3.1/6
0/5.2/3 - 3/2.0/6 - 0/3.0/5 - 2/3.1/6 #? Intro end
2/3.0/6 0/3 5/3 9/3.8/6 7/3.7/6 10/3.10/6 7/3.7/6 5/3.5/6
```

### Tabs syntax

A line is devided into 4 selections, each of them containing up to 8 positions.

* tone - `s/p` (two integers)
	* `s` - number of string
	* `b` - number of bar
* multiple tones on a position - `tone.tone. ... .tone`
* next position in a selection - `space`
	* up to 8 tones in a selection
	* skip position using `-`
* add comment above current selection - `#`
	* if comment starts with character `!`, it will start drawing a line above selections
	* untill tere is a comment starting with `?`
* next selection - newline
	* up to 4 selections
* next line - 2x newline

More formally:

```
string := integer [1, 6]
bar := integer [1, 20]
tone := string/bar
position := tone.position | tone
selection := position selection | position | - selection | -
line := selection \n line | selection
lines := line \n\n lines | line
```

> Dependencies:
> python (2.7.x), librsvg2-bin, imagemagick, python-poppler-qt4, python-svgwrite

> If you are using a Ubuntu-like distribution, they can be installed:
> * sudo apt-get install python2.7 librsvg2-bin imagemagick python-poppler-qt4
> * pip install svgwrite
