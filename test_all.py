"""S.O.L.I.D Design.

Comprehensive test of the modules.

Python 3.4 or later is required.

Note that this must be in the parent folder of the
ch01, ch02, ch03, ch04, ch05, ch06, and ch07 folders.

To run any module individually, be sure that
the ``PYTHONPATH`` environment variable points to this parent folder.

"""

import unittest
import doctest

import ch01.ch_01_02

import ch02.ch_02_isp
import ch02.ch_02_01
import ch02.ch_02_02
import ch02.ch_02_03
import ch02.ch_02_04

import ch03.ch_03_lsp
import ch03.ch_03_01
import ch03.ch_03_02
import ch03.ch_03_03
import ch03.ch_03_04
import ch03.ch_03_05

import ch04.ch_04_ocp
import ch04.ch_04_01
import ch04.ch_04_03
import ch04.ch_04_04

import ch05.ch_05_dip
import ch05.ch_05_01
import ch05.ch_05_02
import ch05.ch_05_03

import ch06.ch_06_srp
import ch06.ch_06_01
import ch06.ch_06_02

import ch07.ch_07_02

modules = (ch01.ch_01_02,
           ch02.ch_02_isp, ch02.ch_02_01, ch02.ch_02_02, ch02.ch_02_03, ch02.ch_02_04,
           ch03.ch_03_lsp, ch03.ch_03_01, ch03.ch_03_02, ch03.ch_03_03, ch03.ch_03_04, ch03.ch_03_05,
           ch04.ch_04_ocp, ch04.ch_04_01, ch04.ch_04_03, ch04.ch_04_04,
           ch05.ch_05_dip, ch05.ch_05_01, ch05.ch_05_02, ch05.ch_05_03,
           ch06.ch_06_srp, ch06.ch_06_01, ch06.ch_06_02,
           ch07.ch_07_02,
          )

def suite():
    """Build a suite from doctest and unittest in each module.
    """
    doctest_suite = unittest.TestSuite(
        [doctest.DocTestSuite(m) for m in modules],
    )
    unittest_suite = unittest.TestSuite(
        [unittest.defaultTestLoader.loadTestsFromModule(m) for m in modules],
    )
    return unittest.TestSuite([doctest_suite, unittest_suite])

if __name__ == "__main__":
    runner= unittest.TextTestRunner()
    runner.run(suite())
