import unittest

from harser import Harser

HTML_ROOT = '''
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
    <img src="image.png" />
    <div class="footer" id="id-foobar" foobar="ab bc cde">
        <h3 some-attr="hey">
            <span id="foobar-span">foo ter</span>
        </h3>
    </div>
</body></html>
'''


class TestHarser(unittest.TestCase):

    def setUp(self):
        self.harser = Harser(HTML_ROOT)

    def test_get_attributes(self):
        self.assertEqual(Harser(HTML_ROOT).find('li', class_='nav-item')
                         .get_attr('href').extract(), ['/nav1', '/nav2', '/nav3'])
        self.assertEqual(Harser(HTML_ROOT).find('img').get_attr('href')
                         .extract(), [])
        self.assertEqual(Harser(HTML_ROOT).find(id='id-header')
                         .get_attr('class').extract(), ['header'])
        self.assertEqual(Harser(HTML_ROOT).find(class_='footer')
                         .get_attr('foobar').extract(), ['ab bc cde'])

    def test_extracts(self):
        self.assertEqual(Harser(HTML_ROOT).find('li').get_attr('href')
                         .extract_first(), '/nav1')
        self.assertEqual(Harser(HTML_ROOT).find('li').extract_first().strip(),'<li class="nav-item" data-nav="first-item" href="/nav1">First item</li>')
        self.assertEqual(Harser(HTML_ROOT).find('li').get_attr('href')
                         .extract_first(), '/nav1')

    def test_tags(self):
        self.assertEqual(Harser(HTML_ROOT).find(attrs={'some-attr': 'hey'})
                         .children().find('text').extract_first(), 'foo ter')

        self.assertEqual(Harser(HTML_ROOT).find('img', src__contains='png')
                         .get_attr('src').extract_first(), 'image.png')

        self.assertEqual(Harser(HTML_ROOT).find(id='foobar-span')
                         .parents('div').get_attr('foobar').extract_first(),
                         'ab bc cde')

        self.assertEqual(Harser(HTML_ROOT).find(id='foobar-span').parent()
                         .get_attr('some-attr').extract_first(), 'hey')

        self.assertEqual(Harser(HTML_ROOT).find('li').parent()
                         .next_siblings(filters={'text__contains': 'Second'})
                         .clean_extract(), ['<div>Second layer</div>'])

        self.assertEqual(Harser(HTML_ROOT).find('li',
                         filters={'text__not_contains': 'First',
                                  'text__not_starts_with': 'Second'})
                         .previous_siblings().get_attr('data-nav')
                         .extract(), ['first-item', 'second-item'])

        self.assertEqual(Harser(HTML_ROOT).find('li', class_='nav-item',
                         attrs={'data-nav': 'second-item'}).siblings()
                         .find('text').extract(), ['First item', 'Second item', 'Third item'])

        self.assertEqual(Harser(HTML_ROOT).find('span',
                         filters={'text__contains': 'third block'})
                         .siblings('span', class_="text").find('text')
                         .extract(), ['first block', 'second block'])

    def test_xpaths(self):
        self.assertEqual(Harser(HTML_ROOT).find('img').xpath, '//descendant::img')
        self.assertEqual(Harser(HTML_ROOT).find('img')
                         .add_xpath('[contains(@src, "png")]').xpath,
                         '//descendant::img[contains(@src, "png")]')
        self.assertEqual(Harser(HTML_ROOT).find('img')
                         .add_xpath('[contains(@src, "png")]').get_attr('src')
                         .extract_first(), 'image.png')

        self.assertEqual(Harser(HTML_ROOT).find(class_=53).xpath,
                         "//descendant::*[@class='53']")
