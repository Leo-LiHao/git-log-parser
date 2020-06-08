import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gitlogparser",
    version="0.1.5",
    author="Gabor Antal",
    author_email="antalgabor1993@gmail.com",
    description="Parser for 'git log' command",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaborantal/git-log-parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'gitlogparser=gitlogparser.main:main',
        ],
    },
)
