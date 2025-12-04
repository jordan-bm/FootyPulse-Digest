import os
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def render_digest(players, save_file=False, output_file="digest_output.html"):
    template = env.get_template("digest.html")
    html = template.render(players=players)

    # Only save file if requested
    if save_file:
        output_path = os.path.join(TEMPLATE_DIR, output_file)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

    return html
