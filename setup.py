from setuptools import setup, find_packages

setup(
    name="mentormatch",
    description='J&J Cross-Sector Mentoring Program utility that matches mentors with mentees.',
    version="0.1.7",
    author='Jonathan Chukinas',
    author_email='chukinas@gmail.com',
    url='https://github.com/jonathanchukinas/mentormatch',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["Click", "openpyxl"],
    entry_points="""
        [console_scripts]
        mentormatch=mentormatch.cli:mentormatch_cli
    """,
)
