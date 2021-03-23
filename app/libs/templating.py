import markdown


def create_info_template():
    with open('README.md', 'r') as file:
        html = markdown.markdown(file.read())
        return '<div class="info>{}</div>'.format(html)
