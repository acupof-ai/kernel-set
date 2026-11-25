"""Include the repository's generated provider catalog in Python packages."""

from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist


_PROJECT_DIR = Path(__file__).resolve().parent
_SOURCE_CATALOG = _PROJECT_DIR.parents[1] / "providers" / "optimal.json"
_PACKAGE_CATALOG = Path("kernel_set/backends/optimal.json")


def _copy_catalog(command, output_dir):
    # A wheel built from an sdist already has the catalog as package data.
    if not (_PROJECT_DIR / _PACKAGE_CATALOG).is_file():
        command.copy_file(str(_SOURCE_CATALOG), str(Path(output_dir) / _PACKAGE_CATALOG))


class BuildPy(build_py):
    def run(self):
        super().run()
        if not self.editable_mode:
            _copy_catalog(self, self.build_lib)


class Sdist(sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)
        _copy_catalog(self, base_dir)


setup(cmdclass={"build_py": BuildPy, "sdist": Sdist})
