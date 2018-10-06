import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="puzzle-massive-divulger",
    version="0.0.1",
    author='Jake Hickenlooper',
    author_email='jake@weboftomorrow.com',
    description="Puzzle Massive divulger app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'puzzle-massive-divulger = divulger.script:main'
        ]
    },
)
