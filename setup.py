from setuptools import setup, find_packages
import os

version = "0.1"

setup(name='Sidekick',
      version=version,
      description="",
      long_description=open("README.rst").read() + "\n" + open("HISTORY.rst").read(),
      author="John Carr",
      author_email="john.carr@isotoma.com",
      license="Apache Software License",
      classifiers = [
          "Intended Audience :: System Administrators",
          "Operating System :: POSIX",
          "License :: OSI Approved :: Apache Software License",
      ],
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'yaybu',
          'apache-libcloud >= 0.5.0',
      ],
      extras_require = {
          'test': ['testtools', 'discover', 'mock'],
          },
      entry_points = """
      [console_scripts]
      sidekick = sidekick.main:main
      """
      )
