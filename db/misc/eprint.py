from __future__ import print_function
import sys

def eprint(error, *args, **kwargs):
    print(f"({type(error).__name__})", *args, file=sys.stderr, **kwargs)