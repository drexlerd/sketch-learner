#!/usr/bin/env python3

import sys

from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from learner.src.util import runner

if __name__ == "__main__":
    runner.run()
