__author__ = 'kevin'

import unittest
import os

from attacksurfacemeter import CallGraph
from loaders import CflowLoader
from formatters import XmlFormatter

from tests.test_txt_formatter import TxtFormatterTestCase


class XmlFormatterTestCase(TxtFormatterTestCase):

    def setUp(self):
        self.formatter = XmlFormatter(
            CallGraph(
                CflowLoader(
                    os.path.join(os.path.dirname(os.path.realpath(__file__)), "helloworld"))))

        self.formatter_output_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "helloworld/formatter.output.xml")

        self.formatter_summary_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "helloworld/formatter.summary.xml")

if __name__ == '__main__':
    unittest.main()