import cairosvg

FILE_TYPES = {'PNG': cairosvg.svg2png, "PDF": cairosvg.svg2pdf, "SVG": cairosvg.svg2svg}
OUTPUT_MIMES = {'PNG': "image/png", "PDF": "application/pdf", "SVG": " image/svg+xml"}
SPACE = 50
POSITION = 60
SIZE_X = 950
