import subprocess
import sys
from pathlib import Path
from typing import Union


def exec_cmd(cmd: str, working_dir_path: Union[str, Path] = None):
    is_windows_os = sys.platform.startswith('win')
    exec_via_shell = is_windows_os

    subprocess.run(
        cmd.split(),
        shell=exec_via_shell,
        stdout=subprocess.PIPE,
        text=True,
        check=True,
        cwd=working_dir_path
    )


if __name__ == '__main__':
    for model, csv_file in [
        ('usersystem.User', 'data/users.csv'),
        ('reviews.Category', 'data/category.csv'),
        ('reviews.Genre', 'data/genre.csv'),
        ('reviews.Title', 'data/titles.csv'),
        ('reviews.GenreTitles', 'data/genre_title.csv'),
        ('reviews.Review', 'data/review.csv'),
        ('reviews.Comment', 'data/comments.csv')
    ]:
        cmd = f'python manage.py importcsv --model={model} {csv_file}'
        exec_cmd(cmd)
