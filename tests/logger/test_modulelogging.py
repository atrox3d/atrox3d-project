import unittest
import sys

import atrox3d.logger.modulelogging as ml
import logging
# from pathlib import Path


class TestModuleLogging(unittest.TestCase):

    def test_set_logger_level_for_imported_modules(self):
        print('import atrox3d.simplegit.git...')
        import atrox3d.simplegit.git
        print(f'{atrox3d.simplegit.git.logger = }')
        print(f'set level of loggers in imported modules to INFO... ')
        ml.set_logger_level_for_imported_modules('INFO', __name__)
        print(f'{atrox3d.simplegit.git.logger = }')
