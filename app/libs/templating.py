import markdown


INFO_TEMPLATE = """<div class="info>{}</div}"""


def create_info_template():
    with open('README.md', 'r') as file:
        html = markdown.markdown(file.read())

        output_file = open("app/templates/info.html", "w")
        output_file.write(html)
        output_file.close()
