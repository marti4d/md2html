import subprocess
import argparse
import os.path

# Configuration

DESCRIPTION = "Converts a CommonMark document into standalone styled HTML"
CMARK_UF_EXE_NAME = "{script_dir}\\cmark.exe"
DEFAULT_UF_TEMPLATE_PATH = "{script_dir}\\md2html.html"
DEFAULT_UF_CSS_PATH = "{script_dir}\\md2html.css"

# Start of script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def fmt_path(path):
    return path.format(script_dir=SCRIPT_DIR)


def render_markdown_as_html(title, markdown, uf_template_path, uf_css_path):
    template_path = fmt_path(uf_template_path)
    css_path = fmt_path(uf_css_path)

    with open(template_path, "rb") as template_file:
        template_html = template_file.read()

    with open(css_path, "rb") as css_file:
        css = css_file.read()

    return template_html.format(title=title, css=css, markdown=markdown)


def generate_markdown_from_file(uf_file_path):
    cmark_exe_name = fmt_path(CMARK_UF_EXE_NAME)
    file_path = fmt_path(uf_file_path)

    if not os.path.isfile(cmark_exe_name):
        raise Exception("Unable to find cmark executable '{}'".format(
                        cmark_exe_name))

    if not os.path.isfile(file_path):
        raise Exception("File not found '{}'".format(file_path))

    markdown = subprocess.check_output([
        cmark_exe_name,
        file_path
        ])

    return markdown


def parse_args(argv):
    parser = argparse.ArgumentParser(prog=argv[0], description=DESCRIPTION)
    parser.add_argument("title", help="The title for the HTML page")
    parser.add_argument("uf_md_path", metavar="input_path",
                        help="Path of input CommonMark file")
    parser.add_argument("-o", dest="uf_html_path", metavar="output_path",
                        help="Path to output HTML file")
    parser.add_argument("-t", dest="uf_template_path", metavar="template_path",
                        help="Path of HTML template",
                        default=DEFAULT_UF_TEMPLATE_PATH)
    parser.add_argument("-s", dest="uf_style_path", metavar="style_path",
                        help="Path of cascading style sheet",
                        default=DEFAULT_UF_CSS_PATH)

    args = parser.parse_args(argv[1:])

    return args


def main(argv):
    args = parse_args(argv)

    markdown = generate_markdown_from_file(args.uf_md_path)

    output_html = render_markdown_as_html(args.title, markdown,
                                          args.uf_template_path,
                                          args.uf_style_path)

    if args.uf_html_path:
        html_path = fmt_path(args.uf_html_path)
        with open(html_path, "wb") as f:
            f.write(output_html)

    else:
        print output_html


if __name__ == "__main__":
    import sys
    main(sys.argv)
