"""Setup tools."""
from setuptools import setup, find_packages

print(find_packages("src"))

setup(name="jishinsensa-device",
      version="0.0.1",
      description="Jishin Sensa Device Services",
      author="Hirley Dayan<hirleydayan@gmail.com>",

      # See: http://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages
      packages=find_packages("src"),
      package_dir={"": "src"},

      # See: http://setuptools.readthedocs.io/en/latest/setuptools.html#namespace-packages
      namespace_packages=["jishinsensa", "jishinsensa.services"],

      scripts=[],
      install_requires=[]
      )
