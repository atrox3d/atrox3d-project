import unittest
import sys

import atrox3d.logger.logmanager as lm
import logging
from pathlib import Path

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
        lm.get_logger(__name__)
