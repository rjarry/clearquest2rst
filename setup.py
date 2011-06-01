# docutils-extensions's setup.py
from distutils.core import setup
setup(
    name = "clearquest2rst",
    version = "0.2.0",
    license = "MIT",
    requires = ["docutils (>=0.7)", "docutilsextensions (>=0.1.0)"],

    description = "A docutils for converting ClearQuest requests to RST tables.",
    long_description = open('README.rst').read(),
    author = "Robin Jarry",
    author_email = "robin.jarry@ablogix.fr",
    url = "http://github.com/robin-jarry/clearquest2rst",
    download_url = "http://github.com/robin-jarry/clearquest2rst",
    keywords = ["docutils", "rst", "reStructuredText", "clearquest"],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: Beta",
        "Environment :: Windows",
        'Intended Audience :: End Users/Desktop',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Document Generation",
    ],
    packages = ["docutilsextensions"],
    package_dir = {'': 'src'}
)

