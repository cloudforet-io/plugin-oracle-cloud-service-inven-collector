import os
import unittest
import json

from pprint import pprint
from spaceone.core.unittest.result import print_data
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core import utils
from spaceone.core.transaction import Transaction
from spaceone.tester import TestCase, print_json


OCI_CREDENTIALS_PATH = os.environ.get('OCI_CRED', None)

if OCI_CREDENTIALS_PATH is None:
    print("""
        ##################################################
        # ERROR 
        #
        # Configure your GCP credential first for test
        # https://console.cloud.google.com/apis/credentials
        ##################################################
        example)
        export GOOGLE_APPLICATION_CREDENTIALS="<PATH>" 
    """)
    exit


def _get_credentials():
    with open(OCI_CREDENTIALS_PATH) as json_file:
        json_data = json.load(json_file)
        return json_data


class TestCollector(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.oci_credentials = _get_credentials()
        pprint(cls.oci_credentials)
        super().setUpClass()

    # def test_init(self):
    #     v_info = self.inventory.Collector.init({'options': {}})
    #     print_json(v_info)

    def test_verify(self):
        options = {
        }
        v_info = self.inventory.Collector.verify({'options': options, 'secret_data': self.oci_credentials})
        print_json(v_info)

    def test_collect(self):
         options = {}
         filter = {}
         resource_stream = self.inventory.Collector.collect({'options': options, 'secret_data': self.oci_credentials,
                                                             'filter': filter})
         # print(resource_stream)

         for res in resource_stream:
             print_json(res)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
