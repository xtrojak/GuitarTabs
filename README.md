# SimpleTabs
The tool translates tabs in syntax described below to a picture.

Tabs are displayed in a grid with fixed width. 

<div align="center">
  <img src="https://raw.githubusercontent.com/xtrojak/GuitarTabs/master/app/static/pics/front.png"><br><br>
</div>

```python
0/5.2/3 - 3/2.0/6 - 0/3.0/5 - 2/3.1/6 #! Intro start
2/3.0/6 0/3 5/3 9/3.8/6 7/3 5/3.5/6 4/3 2/3.1/6
0/5.2/3 - 3/2.0/6 - 0/3.0/5 - 2/3.1/6 #? Intro end
2/3.0/6 0/3 5/3 9/3.8/6 7/3.7/6 10/3.10/6 7/3.7/6 5/3.5/6
```

### Tabs syntax

A line is divided into 4 selections, each of them containing up to 8 positions.

* tone - `s/p` (two integers)
	* `s` - number of string (ranging 1 to 6)
	* `b` - number of guitar bar (ranging 1 to 20)
* multiple tones on a position - `tone.tone. ... .tone`
* next position in a selection - `space`
	* up to 10 tones in a selection
	* skip position using `-`
* add comment above current selection - `#`
	* if comment starts with character `!`, it will start drawing a line above selections
	* until there is a comment starting with `?`
* next selection - newline
	* up to 4 selections
* next line - 2x newline

More formally (in EBNF notation):

```
start: line*
selection: line+ ("\n")?
selection: position+ COMMENT? ("\n")? | COMMENT ("\n")?
position: tone ("." tone)* | "-"
tone : string "/" bar
string : INTEGER
bar : INTEGER    
COMMENT: "#" ("!" | "?")? /[^\n]/*
```
