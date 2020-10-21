from setuptools import setup

setup(name='elvis',
      version='0.2',
      description='Panel based on golden-layout.',
      url='https://github.com/LeonvanKouwen/elvis',
      author='Leon van Kouwen',
      author_email='lvankouwen@gmail.com',
      license='MIT',
      packages=['elvis'],
      include_package_data=True,
      zip_safe=False, 
      install_requires=['panel', 'holoviews', 'plotly'])
