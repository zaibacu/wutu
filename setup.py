from setuptools import setup
from pip.req import parse_requirements
import os

install_reqs = list(parse_requirements("requirements", session = {}))
def version():
    return __import__("wutu").get_version()

setup(  name="wutu",
        version=version(),
        description="A minimalistic python-angular framework",
        author="Šarūnas Navickas",
        author_email="zaibacu@gmail.com",
        license="MIT",
        packages=["wutu"],
        install_requires=[str(ir.req) for ir in install_reqs],
        test_suite="nose.collector",
        tests_require=['nose']
    )
