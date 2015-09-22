from setuptools import setup
from pip.req import parse_requirements
import sys, os
sys.path.append("wutu/")
sys.path.append("wutu/compiler/")

install_reqs = list(parse_requirements("requirements.txt", session={}))


def version():
    import version
    return version.get_version()


setup(name="wutu",
        version=version(),
        description="A minimalistic python-angular framework",
        author="Šarūnas Navickas",
        author_email="zaibacu@gmail.com",
        license="MIT",
        packages=["wutu", "wutu.compiler"],
        install_requires=[str(ir.req) for ir in install_reqs],
        test_suite="nose.collector",
        tests_require=["nose"])
