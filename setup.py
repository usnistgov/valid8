from setuptools import setup, find_packages

setup(
    packages=find_packages(exclude=["tests", "docs"]),
    entry_points="""
          [console_scripts]
          rbv=rbv.cli:main
      """,
)
