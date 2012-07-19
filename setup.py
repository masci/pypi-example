from setuptools import setup

setup(name='PyPi Example',
      version='1.0',
      description='Private PyPi on OpenShift',
      author='Massimiliano Pippi',
      author_email='mpippi@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['Django>=1.3', 'djangopypi', 'django-sendfile'],
     )
