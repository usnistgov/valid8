from setuptools import setup, find_packages

setup(
    packages=find_packages(exclude=["tests", "docs"]),
    entry_points="""
          [console_scripts]
          valid8=valid8.cli:main
          hvalid8=valid8.cli:main
      """,
)
