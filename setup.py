import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mentormatch",
    description='J&J Cross-Sector Mentoring Program utility that matches mentors with mentees.',
    long_description=long_description,
    version="0.1.8",
    author='Jonathan Chukinas',
    author_email='chukinas@gmail.com',
    url='https://github.com/jonathanchukinas/mentormatch',
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["Click", "openpyxl"],
    entry_points="""
        [console_scripts]
        mentormatch=mentormatch.cli:mentormatch_cli
    """,
)

# PyPA tutorial: https://packaging.python.org/tutorials/packaging-projects/
# To distribute the next version:
#   Build the sdist and wheel:
#       python setup.py sdist bdist_wheel
#   Upload to PyPI:
#       twine upload dist/*
