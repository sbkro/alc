# -*- coding:utf-8 -*-

import xml.etree.ElementTree as etree


class ScriptFilter:
    '''
    This is an utility class to manage *Script Filter XML* for Alfred.
    By using this class, you are able to manipulate the *Script Filter
    XML* without being conscious of the XML structure.

    .. seealso::
        About format of *Script Filter XML*, refer to sample workflows.
        How to add 'Script Filter XML Format' workflows is as follows.

        * open 'Aflred Preference.'
        * select 'Workflows' from toolbar.
        * select '+' button.
        * select 'Example' -> 'Script Filter XML format'

    .. warning::
        Not fully corresponds with the specifications of
        *Script Filter XML*.

        Support status is as follows. (Alfred version 2.3)

        +------+-------------+--------+
        |tag   |attribute    | status |
        +======+=============+========+
        |item  |uid          |o       |
        |      +-------------+--------+
        |      |arg          |x       |
        |      +-------------+--------+
        |      |valid        |o       |
        |      +-------------+--------+
        |      |autocomplete |o       |
        |      +-------------+--------+
        |      |type         |x       |
        +------+-------------+--------+
        |title               |o       |
        +--------------------+--------+
        |icon                |x       |
        +--------------------+--------+
        |subtitle            |x       |
        +--------------------+--------+
        |text                |x       |
        +--------------------+--------+

    **How to use** ::

        sf = ScriptFilter()
        sf.append_item('Safari')
        sf.append_item('Google Chrome')
        sf.append_item('Firefox', uid='fx-uid', autocomplete='fx', valid=True)
        print sf.xml_s
        # <items>
        #   <item autocomplete="" uid="0" valid="no">
        #     <title>Safari</title>
        #   </item>
        #   <item autocomplete="" uid="1" valid="no">
        #     <title>Google Chrome</title>
        #   </item>
        #   <item autocomplete="fx" uid="fx-uid" valid="yes">
        #     <title>Firefox</title>
        #   </item>
        # </items>

    '''

    def __init__(self):
        self._node_items = etree.Element('items')

    def append_item(self, title, uid=None, valid=False, autocomplete=''):
        '''
        Append an item at *Script Filter XML*.

        :param str title:
            **Required.**
        :param str uid:
            UID of item. Corresponds to the *uid* attribute in *item* tag.
            Default is item length.
        :param bool valid:
            Corresponds to the *valid* attribute in *item* tag.
            Default is 'no'.
        :param str autocomplete:
            Corresponds to the *autocomplete* attribute in *item* tag.
        :todo:
            Not fully corresponds with the specifications of
            *Script Filter XML*.
        :raises ValueError:
            If *title* is None or empty string.
    '''
        if title is None or title is '':
            raise ValueError('Argument \'title\' is requred.')

        attr_uid = uid if uid else str(len(self._node_items))
        attr_valid = 'yes' if valid else 'no'

        node_item = etree.SubElement(self._node_items, 'item',
                                     uid=attr_uid,
                                     valid=attr_valid,
                                     autocomplete=autocomplete)

        node_title = etree.SubElement(node_item, 'title')
        node_title.text = title

    @property
    def xml(self):
        '''
        Return script filter xml as DOM elements.

        :rtype: xml.etree.Element
        :return: DOM element of script filter xml.
        '''
        return self._node_items

    @property
    def xml_s(self):
        '''
        Return script filter xml as string.

        :rtype: str
        :return: String of script filter xml.
        '''
        return etree.tostring(self._node_items)
