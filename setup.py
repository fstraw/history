try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description': 'History Tools',
	'author': 'Brandon Batt',
	'url': 'www.lowestfrequency.com',
	'download_url': 'www.lowestfrequency.com',
	'author_email': 'fstraw@lowestfrequency.com',
	'version': '0.5',
	'install_requires': ['nose', 'docx'],
	'packages': ['histtools'],
	'scripts': [],
	'name': 'historytools'
}

setup(**config)