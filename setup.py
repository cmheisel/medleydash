from setuptools import setup, find_packages

setup(
    name="medleydash",
    version=__import__("medleydash").__version__,
    author="Chris Heisel",
    author_email="chris@heisel.org",
    description=("A dashboard app for my team"),
    long_description=open("README.rst").read(),
    url="https://github.com/cmheisel/medleydash",
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
    ]
)
