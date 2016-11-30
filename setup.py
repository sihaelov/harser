from setuptools import setup

setup(
    name='harser',
    version='0.1',
    packages=['harser'],
    install_requires=['lxml', 'six'],
    include_package_data=True,
    license='MIT License',
    description='Easy way for HTML parsing and building XPath.',
    url='https://github.com/sihaelov/harser',
    author='Michael Sinov',
    author_email='sihaelov@gmail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
