from setuptools import setup, find_packages

setup(
      name="CoinboxMod-currency",
      version="0.1",
      packages=find_packages(),
      
      zip_safe=True,
      
      namespace_packages=['cbpos', 'cbpos.mod'],
      include_package_data=True,

      install_requires=['sqlalchemy>=0.7','PyDispatcher>=2.0.3','ProxyTypes>=0.9','PySide>=1.1.2'],
      
      author='Coinbox POS Team',
      author_email='coinboxpos@googlegroups.com',
      description='Coinbox POS core package',
      license='GPLv3',
      url='http://coinboxpos.org/'
)
