from unittest2 import TestCase
from aux.system import get_system

class SystemTest(TestCase):

    def test_get_system_type(self):
        system = get_system(systemtype='SSPService')

        print system
