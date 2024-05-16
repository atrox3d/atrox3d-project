import unittest
import atrox3d.logging.logmanager as lm

class TestLogmanager(unittest.TestCase):

    def test_LoggingNotConfiguredexception(self):
        with self.assertRaises(lm.LoggingNotConfiguredException):
            lm.get_logger(__name__)