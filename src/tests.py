"""
Test runner.

Run tests with:
```bash
cd src
python -m unittest tests.py
```

Run specific test with:
```bash
cd src
python -m unittest tests.TestGridGraph
```

"""

import unittest
from hpgg.grid_graphs.tile_grid_graphs import TestGridGraph

if __name__ == "__main__":
    unittest.main()