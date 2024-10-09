from setuptools import setup

setup(
   name='SUAPSslotRegister',
   version='1.0',
   description='just a script using the SUAPS API to register to a slot',
   author='sparkiz3',
   packages=['SUAPSslotRegister'],  #same as name
   install_requires=['requests'], #external packages as dependencies
)