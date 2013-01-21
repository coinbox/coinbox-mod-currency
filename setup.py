from setuptools import setup, find_packages

setup(
      name="CoinboxMod",
      version="0.1",
      packages=find_packages(),
      
      zip_safe=True,
      
      namespace_packages=['cbpos', 'cbpos.mod'],
      include_package_data=True,
      
      author='Coinbox POS Team',
      author_email='coinboxpos@googlegroups.com',
      description='Coinbox POS core package',
      license='GPLv3',
      url='http://coinboxpos.org/'
)
