"""Setup tools."""
from setuptools import setup, find_packages

print(find_packages("src"))

setup(name="ldr",
      version="0.0.1",
      description="Qualcomm Dragonboard 410c Temperature Sensor",
      author="Hirley Dayan<hirleydayan@gmail.com>",

      # See: http://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages
      packages=find_packages("src"),
      package_dir={"": "src"},

      # See: http://setuptools.readthedocs.io/en/latest/setuptools.html#namespace-packages
      namespace_packages=["qcom_db_410c"],

      scripts=[],
      install_requires=["libsoc_zero"]
      )
