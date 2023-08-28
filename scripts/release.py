#!/usr/bin/env python3
from __future__ import annotations

import codecs
import pathlib
import re
import subprocess

from datetime import datetime
from functools import total_ordering

import attr
import click


_MAIN_BRANCH = "main"
_HERE = pathlib.Path(__file__).parent
_ROOT = _HERE.parent
_PACKAGE_ROOT = _ROOT / "src" / "dependabot-dep-poc"
_VERSION_FILE = _PACKAGE_ROOT / "__init__.py"


@total_ordering
@attr.s(eq=False, order=False, slots=True, frozen=True)
class VersionInfo:
    """
    CalVer format: ``YYYY.M.MICRO``

    See https://www.python.org/dev/peps/pep-0440/ for release levels.
    """

    year: int = attr.ib()
    month: int = attr.ib()
    micro: int = attr.ib()
    releaselevel: str = attr.ib()

    @classmethod
    def _from_version_string(cls, s: str, current_branch=None) -> VersionInfo:
        """
        Parse *s* and return a _VersionInfo.
        """
        v = s.split(".")
        if len(v) == 3:
            release_level = "final"
            v.append(release_level)

        return cls(year=int(v[0]), month=int(v[1]), micro=int(v[2]), releaselevel=v[3])

    @classmethod
    def increment_micro(cls, version: VersionInfo) -> VersionInfo:
        return cls(
            year=version.year,
            month=version.month,
            micro=version.micro + 1,
            releaselevel=version.releaselevel,
        )

    def _ensure_tuple(self, other: VersionInfo) -> tuple:
        """
        Ensure *other* is a tuple of a valid length.

        Returns a possibly transformed *other* and ourselves as a tuple of
        the same length as *other*.
        """

        if self.__class__ is other.__class__:
            other = attr.astuple(other)

        if not isinstance(other, tuple):
            raise NotImplementedError

        if not (1 <= len(other) <= 4):
            raise NotImplementedError

        return attr.astuple(self)[: len(other)], other

    def __eq__(self, other: VersionInfo) -> bool:
        try:
            us, them = self._ensure_tuple(other)
        except NotImplementedError:
            return NotImplemented

        return us == them

    def __lt__(self, other: VersionInfo) -> bool:
        try:
            us, them = self._ensure_tuple(other)
        except NotImplementedError:
            return NotImplemented
        return us < them

    def __str__(self):
        ver_str = f"{self.year}.{self.month}.{self.micro}"
        if self.releaselevel != "final":
            ver_str = f"{ver_str}.{self.releaselevel}"
        return ver_str


def get_current_version() -> VersionInfo:
    with codecs.open(_VERSION_FILE, "rb", "utf-8") as f:
        ver_file = f.read()
        ver_str = re.search("__version__ = ['\"]([^'\"]+)['\"]", ver_file).group(1)
        return VersionInfo._from_version_string(ver_str)


def get_next_version(current_version: VersionInfo, current_branch: str) -> VersionInfo:
    now = datetime.now()
    next_version = VersionInfo._from_version_string(
        now.strftime("%Y.%m.1"), current_branch
    )
    while current_version >= next_version:
        next_version = VersionInfo.increment_micro(next_version)
    return next_version


def rewrite_version(current_version: VersionInfo, next_version: VersionInfo):
    """
    Rewrites the configured version file for the new version.
    """
    contents = _VERSION_FILE.read_text()
    contents = contents.replace(
        f'__version__ = "{current_version}"', f'__version__ = "{next_version}"'
    )
    _VERSION_FILE.write_text(contents)


@click.command()
@click.option(
    "--version",
    required=False,
    help="The next version number to use.",
)
@click.option(
    "--confirm/--no-confirm",
    is_flag=True,
    default=True,
    help="Ask for confirmation before acting.",
)
def make_release(version: str | None = None, confirm: bool = True):
    """
    Updates the current version and performs the required ``git`` commands for
    generating the release.

    This command will commit a new change to the source version and push it to
    the VCS origin, along with an annotated tag.
    """
    current_branch = subprocess.check_output(
        ("git", "branch", "--show-current"), encoding="utf-8"
    )
    current_branch = current_branch.strip()
    if current_branch not in [_MAIN_BRANCH]:
        click.secho(
            f"Releases can only be made from the {_MAIN_BRANCH} branches",
            fg="red",
        )
        return False

    try:
        # Git pull with rebase to make sure the release has the latest code from origin
        output = subprocess.check_output(
            ["git", "pull", "origin", current_branch, "--rebase"],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        click.secho(output)
    except subprocess.CalledProcessError as e:
        error_output = e.output
        if "cannot pull with rebase: You have unstaged changes" in error_output:
            click.secho("Error: You have unstaged changes. Please commit or stash them")
        else:
            # Handle other errors
            click.secho("An error occurred:", e)

        return False

    current_version = get_current_version()
    if version is None:
        version = get_next_version(current_version, current_branch)

    if confirm:
        prompt = f"Version to replace {current_version} with"
        chosen_version = click.prompt(prompt, default=str(version))
        if chosen_version:
            try:
                version = VersionInfo._from_version_string(chosen_version)
            except ValueError:
                click.secho("Invalid version format", fg="red")
                return False

        proceed = click.confirm("Ready to commit changes and push?")
        if not proceed:
            click.echo("Doing nothing")
            return True

    # Write new version to _VERSION_FILE
    rewrite_version(current_version, version)
    # Commit changes
    click.secho("Staging changes", fg="cyan")
    subprocess.run(("git", "add", str(_VERSION_FILE)))
    click.secho("Commiting changes", fg="cyan")
    subprocess.run(("git", "commit", "-m" "Bumped version number"))
    # Create tag
    click.secho("Tagging changes", fg="cyan")
    subprocess.run(("git", "tag", "-a", f"{version}", "-m", f"Release {version}"))
    # Push all
    click.secho("Pushing changes", fg="cyan")
    subprocess.run(("git", "push"))
    subprocess.run(("git", "push", "origin", f"{version}"))
    click.secho("Done", fg="cyan")


if __name__ == "__main__":
    make_release()
