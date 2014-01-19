from setuptools import setup, find_packages

setup(
      name="Coinbox-mod-currency",
      version="0.2",
      packages=find_packages(),
      
      zip_safe=True,
      
      namespace_packages=['cbmod'],
      include_package_data=True,

      install_requires=[
            'sqlalchemy>=0.7, <1.0',
            'PyDispatcher>=2.0.3, <3.0',
            'ProxyTypes>=0.9, <1.0',
            'Babel>=1.3, <2.0',
            'PySide>=1.0,<2.0'
      ],
      
      author='Coinbox POS Team',
      author_email='coinboxpos@googlegroups.com',
      description='Coinbox POS currency module',
      license='MIT',
      url='http://coinboxpos.org/'
)
