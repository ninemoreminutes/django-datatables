# Python
import os

# django-setuptest
import setuptest

class TestSuite(setuptest.SetupTestSuite):
    
    def resolve_packages(self):
        packages = super(TestSuite, self).resolve_packages()
        test_app = os.path.basename(os.path.dirname(__file__))
        if test_app not in packages:
            packages.append(test_app)
        return packages
