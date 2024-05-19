import logging
import unittest

import atrox3d.logger.modulelogging as ml
from . import fakemodule

class TestModuleLogging(unittest.TestCase):

    def test_get_module_loggers(self):
        loggers = ml.get_module_loggers(fakemodule)
        self.assertEqual(1, len(loggers))
        self.assertIsInstance(loggers[0], logging.Logger)

    def test_set_module_loggers_level(self):
        ml.set_module_loggers_level(fakemodule, 'ERROR')
        for logger in ml.get_module_loggers(fakemodule):
            self.assertEqual(logging.getLevelName(logger.getEffectiveLevel()), 'ERROR')

    def test_set_logger_level_for_modules(self):
        ml.set_logger_level_for_modules('ERROR', fakemodule)
        for logger in ml.get_module_loggers(fakemodule):
            self.assertEqual(logging.getLevelName(logger.getEffectiveLevel()), 'ERROR')

    def test_set_logger_level_for_imported_modules(self):
        ml.set_logger_level_for_imported_modules('INFO', __name__)
        print(f'{fakemodule.logger = }')
