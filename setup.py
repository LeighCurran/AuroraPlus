from distutils.core import setup
setup(
  name = 'AuroraPlus',
  packages = ['AuroraPlus'],
  version = '0.0.1',
  license='MIT',
  description = 'Python library to access the Aurora+ API: https://api.auroraenergy.com.au/api',
  author = 'Leigh Curran',
  author_email = 'AuroraPlusPy@outlook.com',
  url = 'https://github.com/leighcurran/AuroraPlus',
  keywords = ['Aurora+', 'AuroraPlus', 'Aurora', 'Tasmania', 'API'],
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.9',
  ],
)