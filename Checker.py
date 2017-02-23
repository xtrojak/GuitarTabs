from pyparsing import Word, Literal, nums, White, Forward, LineEnd

string = Word( nums ).setResultsName("string")
position = Word( nums ).setResultsName("position")
slash = Literal("/")
tone = (string + slash + position).setResultsName("tone")
dot = Literal(".")
space = White(" ")
tones = Forward().setResultsName("tones")
tones_recursion = ( tone + dot + tones ) | tone
tones << tones_recursion
selection = Forward().setResultsName("selection")
selection_recursion = (tones + space + selection) | tones
selection << selection_recursion
newline = LineEnd()
line = Forward().setResultsName("line")
line_recursion = (selection + newline + line) | selection
line << line_recursion
tabs = Forward().setResultsName("tabs")
tabs_recursion = (line + newline + newline + tabs) | line
tabs << tabs_recursion

file = open('example.txt', "r").read()
results = tabs.parseString(file)