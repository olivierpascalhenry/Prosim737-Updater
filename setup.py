"""Prosim737 Updater

Prosim737 Updater is a tool dedicated to update Prosim737. It can install updated 
stored locally, or donwload and install updates from the official Prosim737 website. 
It can create backups of a full Prosim737 installation, and restore a backup. Its 
primary goal is to be used for Prosim737 beta testing. But it can be used to backup 
and manage updates of Prosim737.
"""


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

classifiers = """\
Development Status :: 5 - Production/Stable
Environment :: Win32 (MS Windows)
Environment :: X11 Applications :: Qt
Intended Audience :: Developers
Intended Audience :: End Users/Desktop
License :: OSI Approved :: GNU General Public License v3 (GPLv3)
Natural Language :: English
Operating System :: Microsoft :: Windows
Programming Language :: Python :: 3.5
Topic :: Games/Entertainment :: Simulation
Topic :: System :: Installation/Setup
Topic :: Utilities
"""

doclines = __doc__.split('\n')

setup(name='Prosim737 Updater',
      version='1.0.0',
      description=doclines[0],
      long_description='\n'.join(doclines[2:]),
      author='Olivier Henry',
      author_email='olivier.pascal.henry@gmail.com',
      maintainer='Olivier Henry',
      maintainer_email='olivier.pascal.henry@gmail.com',
      url='',
      download_url='',
      license='GNU General Public License v3',
      keywords=['Prosim737', 'simulator', 'update'],
      packages=['ui',
          'ui.build',
          'functions',
		  'documentation',
          'fonts',
          'icons'],
      package_data={
          'icons': ['*.svg', '*.png'],
	      'fonts': ['*.ttf'],
          'documentation': ['*.txt'],
          'ui.build': ['*.ui']},
      classifiers=filter(None, classifiers.split("\n")),
      requires=['PyQt5 (>=5.7)', 'beautifulsoup4 (>=4.5.3)', 'requests (>=2.13.0)', 'psutil (>=5.2.1)'],
      install_requires=['PyQt5 >= 5.7', 'beautifulsoup4 >= 4.5.3', 'requests >= 2.13.0', 'psutil >= 5.2.1'],
      )
