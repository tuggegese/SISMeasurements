import os
from setuptools import setup

setup(
      name="SISEval",
      description="Sediment impact Sensors evaluation tool",
      author="S. Gegenleithner",
      licence='MIT',
      python_requires=">3.6",
      install_requires=[
              "numpy",
              "scipy",
              "pi-ina219",
              "PyWavelets",
              "statsmodels",
              "pytz",
              "tinydb"]
      )