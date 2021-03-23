import markdown


def create_info_template():
    with open('README.md', 'r') as file:
        source = file.read()
        source = "\n".join(source.split("\n")[1:])
        html = markdown.markdown(source, extensions=['fenced_code'])
        return '<div class="modal-body">{}</div>'.format(html)
