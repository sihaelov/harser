
# Harser

[![Build Status](https://travis-ci.org/sihaelov/harser.svg?branch=master)](https://travis-ci.org/sihaelov/harser) [![Coverage Status](https://img.shields.io/codecov/c/github/sihaelov/harser.svg)](https://codecov.io/gh/sihaelov/harser) [![Wheel Status](https://img.shields.io/badge/wheel-yes-brightgreen.svg)](https://pypi.python.org/pypi/harser) ![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg) [![PyPI Version](https://img.shields.io/pypi/v/harser.svg)](https://pypi.python.org/pypi/harser)


Harser is a library for easy extracting data from HTML and building XPath.

## Installation

```python
pip install harser
```
## Examples

```python
>>> from harser import Harser

>>> HTML = '''
    <html><body>
    <div class="header" id="id-header">
        <li class="nav-item" data-nav="first-item" href="/nav1">First item</li>
        <li class="nav-item" data-nav="second-item" href="/nav2">Second item</li>
        <li class="nav-item" data-nav="third-item" href="/nav3">Third item</li>
    </div>
    <div>First layer
        <h3>Lorem Ipsum</h3>
        <span>Dolor sit amet</span>
    </div>
    <div>Second layer</div>
    <div>Third layer
        <span class="text">first block</span>
        <span class="text">second block</span>
        <span>third block</span>
    </div>
    <span>fourth layer</span>
    <img />
    <div class="footer" id="id-foobar" foobar="ab bc cde">
        <h3 some-attr="hey">
            <span id="foobar-span">foo ter</span>
        </h3>
    </div>
    </body></html>
'''

>>> harser = Harser(HTML)

>>> harser.find('div', class_='header').children(class_='nav-item').find('text').extract()
# Or just
# harser.find(class_='nav-item').find('text').extract()
['First item', 'Second item', 'Third item']

>>> harser.find(class_='nav-item').get_attr('href').extract()
['/nav1', '/nav2', '/nav3']

# It is equally
>>> harser.find('div', class_='header', id='id-header')
>>> harser.find('div', attrs={'class': 'header', 'id': 'id-header'})

>>> harser.find(id__contains='bar').get_attr('class').extract()
['footer']

>>> harser.find(href__not_contains='2').find('text').extract()
['First item', 'Third item']

>>> harser.find(attrs={'data-nav__contains': 'second'}).next_siblings().find('text').extract()
['Third item']

>>> harser.find('li').parent().next_siblings(filters={'text__contains': 'Second'}).clean_extract()
['<div>Second layer</div>']

>>> harser.find('h3', filters={'span.@id__starts_with': 'foo'}).get_attr('some-attr').extract()
['hey']

>>> harser.find('div').children('h3').xpath
'//descendant::div/h3'

```

## Support the project

Please contact [Michael Sinov](mailto:sihaelov@gmail.com?subject=Harser) if you want to support the Harser project.
