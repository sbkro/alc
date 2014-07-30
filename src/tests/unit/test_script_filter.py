# -*- coding:utf-8 -*-

from mock import MagicMock, patch
from alc.script_filter import ScriptFilter
from nose.tools import raises


class TestAppendItem:
    '''
    Unit test for *ScriptFilter.append_item()*.
    '''

    m_node_item = MagicMock()
    m_node_title = MagicMock()

    @patch('xml.etree.ElementTree.SubElement',
           side_effect=[m_node_item, m_node_title])
    def test_default(self, m_SubElement):
        '''
        :type: normal
        :case: argument *title* is only specified.
        :expect: append *item* tag.
        '''
        sf = ScriptFilter()
        sf.append_item('sample')

        expect = [((sf.xml, 'item'),
                   {'uid': '0', 'valid': 'no', 'autocomplete': ''},),
                  ((self.m_node_item, 'title'),)]
        assert expect == m_SubElement.call_args_list
        assert self.m_node_title.text == 'sample'

    @patch('xml.etree.ElementTree.SubElement',
           side_effect=[m_node_item, m_node_title])
    def test_valid_is_true(self, m_SubElement):
        '''
        :type: normal
        :case: keyword argument *valid* is True.
        :expect: *valid* attribute is 'yes'.
        '''
        sf = ScriptFilter()
        sf.append_item('sample', valid=True)

        expect = [((sf.xml, 'item'),
                   {'uid': '0', 'valid': 'yes', 'autocomplete': ''},),
                  ((self.m_node_item, 'title'),)]
        assert expect == m_SubElement.call_args_list
        assert self.m_node_title.text == 'sample'

    @patch('xml.etree.ElementTree.SubElement',
           side_effect=[m_node_item, m_node_title])
    def test_autocomplete_is_specified(self, m_SubElement):
        '''
        :type: normal
        :case: keyword argument *autocomplete* is not None.
        :expect: *autocomplete* attribute is specified string.
        '''
        sf = ScriptFilter()
        sf.append_item('sample', autocomplete='comp_test')

        expect = [((sf.xml, 'item'),
                   {'uid': '0', 'valid': 'no', 'autocomplete': 'comp_test'},),
                  ((self.m_node_item, 'title'),)]
        assert expect == m_SubElement.call_args_list
        assert self.m_node_title.text == 'sample'

    @patch('xml.etree.ElementTree.SubElement',
           side_effect=[m_node_item, m_node_title])
    def test_uid_is_specified(self, m_SubElement):
        '''
        :type: normal
        :case: keyword argument *uid* is not None.
        :expect: *uid* attribute is specified string.
        '''
        sf = ScriptFilter()
        sf.append_item('sample', uid='uid_test')

        expect = [((sf.xml, 'item'),
                   {'uid': 'uid_test', 'valid': 'no', 'autocomplete': ''},),
                  ((self.m_node_item, 'title'),)]
        assert expect == m_SubElement.call_args_list
        assert self.m_node_title.text == 'sample'

    def test_title_is_invalid(self):
        '''
        :type: error
        :case: argument *title* is None or empty string.
        :expect: raise ValueError.
        '''
        @raises(ValueError)
        def execute(title):
            sf = ScriptFilter()
            sf.append_item(title)

        execute(None)
        execute('')


def test_xml():
    '''
    Unit test for *ScriptFilter.xml*.

    :type: normal
    :case: call this method.
    :expect: return *Script Filter XML* as DOM tree.
    '''
    sf = ScriptFilter()
    assert sf.xml == sf._node_items


@patch('xml.etree.ElementTree.tostring')
def test_xml_s(m_tostring):
    '''
    Unit test for *ScriptFilter.xml_s*.

    :type: normal
    :case: call this method.
    :expect: call *xml.etree.ElementTree.tostring*.
    '''
    sf = ScriptFilter()
    sf.xml_s

    m_tostring.assert_called_once_with(sf._node_items)
