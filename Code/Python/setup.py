import setuptools

setuptools.setup(
      name='onoma',
      version='2023.12.3.1',
      description='Onoma database manager',
      url='',
      author='Francesca Yffelti',
      author_email='francesca@pikkatech.eu',
      license='MIT',
      packages=['onoma'],
      package_data={'.': ['person_name.py', 'onoma_database.py']}, 

      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.9',
      ],
  )
