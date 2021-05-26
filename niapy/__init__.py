# encoding=utf8

"""Python micro framework for building nature-inspired algorithms."""

from niapy import util, algorithms, benchmarks, task
from niapy.runner import Runner

__all__ = ["algorithms", "benchmarks", "util", "task", "Runner"]
__project__ = "NiaPy"
__version__ = "2.0.0rc16"

VERSION = "{0} v{1}".format(__project__, __version__)
