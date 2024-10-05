from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'pybible-api'
Library for bible data'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="pybible-api", 
        version=VERSION,
        author="Jordo993",
        author_email="jordan.m.young0@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["regex","requests","beautifulsoup4"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'bible'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",

        ]
)
