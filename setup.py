"""
Surge command line client
"""
from setuptools import find_packages, setup

dependencies = ['click', 'python-vagrant']

setup(
    name='surge',
    version='0.1.0',
    url='https://github.com/CiscoSystems/surge',
    license='BSD',
    author='Marc Solanas Tarre',
    author_email='msolanas@cisco.com',
    description='Surge command line client',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'surge = surge.cli:cli',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
