from setuptools import setup

setup(
    name='Terminal_bot',
    version='1.0.0',
    description='Terminal bot App for office managers',
    url='https://github.com/Krom4rd/Terminal_bot',
    author='Code Warriors',
    author_email='Krom4rd@gmail.com, vavazen@gmail.com, ',
    license='MIT',
    packages=['Terminal_bot'],
    install_requires=[''],    
    entry_points={'console_scripts': ['Terminal_bot = Terminal_bot.main:main']
                  })

