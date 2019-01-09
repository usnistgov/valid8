from setuptools import setup, find_packages

setup(
    name="rbv",
    version="0.0.1",
    packages=find_packages(),
    entry_points="""
          [console_scripts]
          rbv=rbv.cli:main
      """,
)
