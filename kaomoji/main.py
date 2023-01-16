# Python parameters
import os
import shutil

import click

from kaomoji.utils import project_path

cli = click.Group()


@cli.command()
@click.option(
    "--link",
    "-l",
    is_flag=True,
    help="Copy emoticon folder to specified location",
)
def link(link):
    """Copy emoticon folder to specified location"""
    if link:
        home = os.path.expanduser("~")
        emoticons_path = f"{home}/.local/share/splatmoji/data/emoticons"
        source = f"{project_path()}/data/emoticons"
        if os.path.exists(emoticons_path):
            shutil.rmtree(emoticons_path)
        shutil.copytree(source, emoticons_path)
        print(f"Copied {source} to {emoticons_path}")
    else:
        print("use the flag --link or -l to copy emoticon folder")


if __name__ == "__main__":
    cli()
