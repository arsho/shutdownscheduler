# -*- coding: utf-8 -*-
import unittest
import os
import sys
import tkinter as tk
import platform
BASEDIR = os.path.abspath(os.path.join(
                          os.path.dirname(os.path.abspath(__file__)),
                          ".."))
sys.path.insert(0, BASEDIR)
import main

class TestShutdownScheduler(unittest.TestCase):
    pass
if __name__ == "__main__":
    unittest.main()
