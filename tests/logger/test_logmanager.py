import unittest
import sys

import atrox3d.logger.logmanager as lm
import logging
# from pathlib import Path

class TestLogmanager(unittest.TestCase):

    def setUp(self):
        ''' import (cached) module into global '''
        global lm
        import atrox3d.logger.logmanager as lm
    
    def tearDown(self) -> None:
        ''' remove current module, delete module var '''
        global lm
        del sys.modules['atrox3d.logger.logmanager']
        del lm

    def test_logging_is_not_configured(self):
        self.assertEqual(False, lm.is_logging_configured())

    def test_logging_is_configured(self):
        lm.setup_logging()
        self.assertEqual(True, lm.is_logging_configured())

    def test_LoggingNotConfiguredexception(self):
        with self.assertRaises(lm.LoggingNotConfiguredException):
            lm.get_logger(__name__)
    
    def test_logging_configuration_status(self):
        self.assertFalse(lm.is_logging_configured())
        lm.setup_logging()
        self.assertTrue(lm.is_logging_configured())

    def test_get_logger(self):
        self.assertFalse(lm.is_logging_configured())
        lm.setup_logging('INFO')
        self.assertTrue(lm.is_logging_configured())
        logger_info = lm.get_logger('info')
        self.assertEqual('INFO', logging.getLevelName(logger_info.getEffectiveLevel()))
        logger_debug = lm.get_logger('debug', level='DEBUG')
        self.assertEqual('DEBUG', logging.getLevelName(logger_debug.getEffectiveLevel()))

    def test_set_logger_level_for_imported_modules(self):
        print('import atrox3d.simplegit.git...')
        import atrox3d.simplegit.git
        print(f'{atrox3d.simplegit.git.logger = }')
        print(f'set level of loggers in imported modules to INFO... ')
        lm.set_logger_level_for_imported_modules('INFO', __name__)
        print(f'{atrox3d.simplegit.git.logger = }')
