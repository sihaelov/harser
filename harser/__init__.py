from lxml.html import fromstring, tostring
import six


class Harser(object):
    SET_FILTERS = {
        'contains': 'contains',
        'starts_with': 'starts-with',
        'ends_with': 'ends-with'
    }

    def __init__(self, html_str='', xpath='/'):
        self.xpath = xpath
        self.html_str = html_str

    def _get_tree(self):
        tree = fromstring(self.html_str)
        return tree.xpath(self.xpath)

    def _extract_base(self, is_clean):
        tree_result = self._get_tree()
        result = []

        for el in tree_result:
            try:
                el_result = tostring(el, pretty_print=True, encoding='unicode')
                if is_clean:
                    el_result = el_result.strip()
                result.append(el_result)
            except TypeError:
                result.append(el)

        return result

    def extract(self):
        result = self._extract_base(is_clean=False)
        return result

    def clean_extract(self):
        result = self._extract_base(is_clean=True)
        return result

    def extract_first(self):
        tree_result = self._get_tree()

        if tree_result:
            try:
                result = tostring(tree_result[0], pretty_print=True, encoding='unicode')
            except TypeError:
                result = tree_result[0]
            return result

    def _parse(self, tag=None, element='*', filters=None, attrs=None, **kwargs):

        if element == 'text':
            element += '()'

        if tag:
            self.xpath += '/{tag}{element}'.format(tag=tag, element=element)
        else:
            self.xpath += '/{element}'.format(element=element)

        if kwargs and attrs:
            attrs.update(kwargs)
        elif kwargs:
            attrs = kwargs

        if filters or attrs:
            predicates = self._build_filtres(filters, attrs)
            self.xpath += predicates

        return Harser(html_str=self.html_str, xpath=self.xpath)

    def add_xpath(self, xpath):
        self.xpath += xpath
        return self

    def _build_filtres(self, filters, attrs):

        predicates = []
        if attrs:
            normalized_attrs = {}

            for key, value in attrs.items():
                normalized_attrs[key] = self._normalize_search_value(value)

            attrs = normalized_attrs

            if 'class_' in attrs:
                attrs['class'] = attrs.pop('class_')

            for attr_name, attr_text in attrs.items():
                predicates.append(self._build_predicates(attr_name, attr_text))

        if filters:
            for filter_name, filter_text in filters.items():
                filter_name = filter_name.replace('.', '/')

                filter_names = filter_name.split('/')
                filter_query = filter_names[len(filter_names)-1]
                attr_filter = self._build_condition(filter_query, filter_text)
                filter_result = filter_name.split('__')[0].replace('text', 'text()')

                if filter_result and attr_filter:
                    predicates.append(filter_result + attr_filter)

        return '[' + ' and '.join(predicates) + ']'

    def _normalize_search_value(self, value):
        # Leave it alone if it's a Unicode string, a callable, a
        # regular expression, a boolean, or None.
        if (isinstance(value, six.text_type) or callable(value) or hasattr(value, 'match')
            or isinstance(value, bool) or value is None):
            return value

        # If it's a bytestring, convert it to Unicode, treating it as UTF-8.
        if isinstance(value, six.binary_type):
            return value.decode("utf8")

        # Otherwise, convert it into a Unicode string.
        # The unicode(str()) thing is so this will do the same thing on Python 2
        # and Python 3.
        return six.text_type(str(value))

    def _build_predicates(self, attr, value):
        predicates = ''

        filter_list = attr.split('__')

        predicates += ("%s()" if attr == 'text' else "@%s") % filter_list[0]

        attr_filter = self._build_condition(attr, value)

        if attr_filter:
            predicates += attr_filter
        else:
            predicates += "='%s'" % value

        return predicates

    def _build_condition(self, attr, value):

        is_negative = False

        filter_list = attr.split('__')
        attr_filter = ''

        if len(filter_list) > 1:
            filter_str = filter_list[1]

            if 'not_' in filter_str:
                is_negative = True
                filter_str = filter_str.replace('not_', '')

            attr_filter = self.SET_FILTERS[filter_str]

        result_filter = None

        if attr_filter:

            result_filter_base = "{filter}(., '{value}')".format(filter=attr_filter,
                                                                 value=value)

            result_filter = ("[not(%s)]" if is_negative else "[%s]") % result_filter_base

        return result_filter

    def find(self, *args, **kwargs):
        return self._parse('descendant::', *args, **kwargs)

    def children(self, *args, **kwargs):
        return self._parse('', *args, **kwargs)

    def parents(self, *args, **kwargs):
        return self._parse('ancestor::', *args, **kwargs)

    def parent(self, *args, **kwargs):
        return self._parse('parent::', *args, **kwargs)

    def next_siblings(self, *args, **kwargs):
        return self._parse('following-sibling::', *args, **kwargs)

    def previous_siblings(self, *args, **kwargs):
        return self._parse('preceding-sibling::', *args, **kwargs)

    def siblings(self, element=None, *args, **kwargs):
        new_element = '../'
        if element:
            new_element += element
        else:
            new_element += '*'
        return self._parse(element=new_element, *args, **kwargs)

    def get_attr(self, element):
        return self._parse('@', element)
