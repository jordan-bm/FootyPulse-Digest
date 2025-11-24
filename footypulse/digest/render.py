import os
from jinja2 import Environment, FileSystemLoader

def render_digest(players, output_path="digest_output.html"):
    # Render the daily digest HTML using Jinja2
    # players: DataFrame or list of dicts
    
    # DataFrame -> list of dicts
    if hasattr(players, "to_dict"):
        players = players.to_dict(orient="records")

    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    template = env.get_template("template.html")

    html = template.render(players=players)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path
