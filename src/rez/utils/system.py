from contextlib import contextmanager
import subprocess
import sys


@contextmanager
def add_sys_paths(paths):
    """Add to sys.path, and revert on scope exit.
    """
    original_syspath = sys.path[:]
    sys.path.extend(paths)

    try:
        yield
    finally:
        sys.path = original_syspath


def popen(args, **kwargs):
    """Wrapper for `subprocess.Popen`.

    Avoids python bug described here: https://bugs.python.org/issue3905. This
    can arise when apps (maya) install a non-standard stdin handler.
    """
    try:
        file_no = sys.stdin.fileno()

    except AttributeError:
        # Maya uses a non standard stdin object which does not implement
        # fileno we can work around this using the private __stdin__ object
        # which remains unmolested
        file_no = sys.__stdin__.fileno()

    if "stdin" not in kwargs and file_no not in (0, 1, 2):
        kwargs["stdin"] = subprocess.PIPE

    return subprocess.Popen(args, **kwargs)
