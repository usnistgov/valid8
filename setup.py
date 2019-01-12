from setuptools import setup, find_packages

setup(
    name="rbv",
    packages=find_packages(),
    entry_points="""
          [console_scripts]
          rbv=rbv.cli:main
      """,
)
