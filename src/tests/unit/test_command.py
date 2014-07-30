# -*- coding:utf-8 -*-

import calendar

from datetime import datetime
from mock import patch
from alc.command import CalendarCommand, ArgumentParserError
from freezegun import freeze_time


class Test__Init__():
    '''
    Unit test for *CalendarCommand.__init__()*.
    '''
    def execute(self, config, expect):
        '''
        This is a utility method.
        Verify that *config* and *expect* the same.

        :param dict config: config
        :param dict expect: expect
        '''
        cmd = CalendarCommand(config)

        assert cmd._firstweekday == expect['firstweekday']
        assert str(cmd._datetime) == expect['datetime']
        assert cmd._datetime_format == expect['datetime_format']

    @freeze_time('2014-07-26 12:00:00')
    def test_config_is_empty(self):
        '''
        :type: normal
        :case: *config* is empty.
        :expect: instance variables are used default value.
        '''
        config = {}
        expect = {
            'firstweekday': calendar.MONDAY,
            'datetime': '2014-07-26 12:00:00',
            'datetime_format': '%Y/%m/%d (%a)\t%H:%M:%S'
        }

        self.execute(config, expect)

    @freeze_time('2014-07-26 12:00:00')
    def test_first_week_day_is_specified(self):
        '''
        :type: normal
        :case: *first_week_day* is specified.
        :expect: *_firstweekday* is set in instance variable.
        '''
        config = {
            'first_week_day': calendar.SUNDAY
        }
        expect = {
            'firstweekday': calendar.SUNDAY,
            'datetime': '2014-07-26 12:00:00',
            'datetime_format': '%Y/%m/%d (%a)\t%H:%M:%S'
        }

        self.execute(config, expect)

    @freeze_time('2014-07-26 12:00:00')
    def test_query_is_empty(self):
        '''
        :type: normal
        :case: *query* is empty.
        :expect: *default_datetime_format* is set in instance variable.
        '''
        config = {
            'query': '',
            'default_datetime_format': '%Y/%m/%d'
        }
        expect = {
            'firstweekday': calendar.MONDAY,
            'datetime': '2014-07-26 12:00:00',
            'datetime_format': '%Y/%m/%d'
        }

        self.execute(config, expect)

    @freeze_time('2014-07-26 12:00:00')
    def test_query_is_month(self):
        '''
        :type: normal
        :case: month is set in *query*.
        :expect: *specified_datetime_format* is set in instance variable.
        '''
        config = {
            'query': '08',
            'specified_datetime_format': '%Y/%m/%d'
        }
        expect = {
            'firstweekday': calendar.MONDAY,
            'datetime': '2014-08-01 00:00:00',
            'datetime_format': '%Y/%m/%d'
        }

        self.execute(config, expect)

    @freeze_time('2014-07-26 12:00:00')
    def test_query_is_month_and_year(self):
        '''
        :type: normal
        :case: month and year are set in *query*.
        :expect: *specified_datetime_format* is set in instance variable.
        '''
        config = {
            'query': '08 2013',
            'specified_datetime_format': '%Y/%m/%d'
        }
        expect = {
            'firstweekday': calendar.MONDAY,
            'datetime': '2013-08-01 00:00:00',
            'datetime_format': '%Y/%m/%d'
        }

        self.execute(config, expect)

    @freeze_time('2014-07-26 12:00:00')
    def test_query_is_space_only(self):
        '''
        :type: normal
        :case: space is set in *query*.
        :expect: *default_datetime_format* is set in instance variable.
        '''
        config = {
            'query': '   ',
            'default_datetime_format': '%Y/%m/%d'
        }
        expect = {
            'firstweekday': calendar.MONDAY,
            'datetime': '2014-07-26 12:00:00',
            'datetime_format': '%Y/%m/%d'
        }

        self.execute(config, expect)


class Test_ParseQuery():
    '''
    Unit test for *CalendarCommand._parse_query()*.
    '''

    @patch('alc.command.CalendarCommand.__init__', return_value=None)
    def execute(self, query, expect, m__init__):
        '''
        This is a utility method. Varify that result and *expect* the same.

        :param dict query: argument of this method.
        :param dict expect: expect
        '''
        cmd = CalendarCommand({})
        actual = cmd._parse_query(query)
        print actual
        assert expect == actual

    @patch('alc.command.ThrowingArgumentParser.error',
           side_effect=[ArgumentParserError('error_message')])
    @patch('alc.command.CalendarCommand.__init__', return_value=None)
    def execute_error(self, query, m__init__, m_error):
        '''
        This is a utility method. varify that error dict is returned.

        :param dict query: argument of this method.
        '''
        cmd = CalendarCommand({})
        actual = cmd._parse_query(query)
        expect = {'error': 'error_message'}
        assert expect == actual

    def test_query_is_empty(self):
        '''
        :type: normal
        :case: *query* is empty.
        :expect: arguments are None.
        '''
        self.execute('', {'month': None, 'year': None})
        print '****'
        self.execute('   ', {'month': None, 'year': None})
        print '****'

    def test_query_is_month(self):
        '''
        :type: normal
        :case: month is set in *query*.
        :expect: the parse result is set in *month*.
        '''
        for m in range(1, (12 + 1)):
            # normal
            self.execute(('%d' % m), {'month': m, 'year': None})

            # 0-padding
            self.execute(('%03d' % m), {'month': m, 'year': None})

    def test_query_is_invalid_month(self):
        '''
        :type: error
        :case: month is invalid.
        :expect: raise ValueError.
        '''
        # out of range (1..12)
        self.execute_error('0')
        self.execute_error('13')

        # not integer
        self.execute_error('abc')
        self.execute_error('1.0')

    def test_query_are_month_and_year(self):
        '''
        :type: normal
        :case: month and year are set in *query*.
        :expect: the parse result is set in *month* and *year*.
        '''
        # normal
        self.execute('1 0', {'month': 1, 'year': 0})
        self.execute('12 9999', {'month': 12, 'year': 9999})

        # 0-padding
        self.execute('0001 00000', {'month': 1, 'year': 0})
        self.execute('0012 09999', {'month': 12, 'year': 9999})

    def test_query_are_invalid_month_and_year(self):
        '''
        :type: error
        :case: month and year are invalid.
        :expect: raise ValueError.
        '''
        # out of range (0..9999)
        self.execute_error('1 -1')
        self.execute_error('1 10000')

        # not integer
        self.execute_error('1 abc')
        self.execute_error('1 2014.0')

    def test_query_are_invalid(self):
        '''
        :type: error
        :case: length of query is invalid.
        :expect: raise ValueError.
        '''
        self.execute_error('1 2014 1')


class TestExecute():
    '''
    Unit test for *CalendarCommand.execute()*.
    '''

    @patch('alc.command.CalendarCommand.__init__', return_value=None)
    @patch('alc.formatter.CalendarFormatter')
    @patch('alc.script_filter.ScriptFilter.xml_s')
    @patch('alc.script_filter.ScriptFilter.append_item')
    def test_default(self, m_append_item, m_xml_s, m_CalendarFormatter, m__init__):
        '''
        :type: error
        :case: call this method.
        :expect: generated calendar is correctly.
        '''
        cmd = CalendarCommand({})
        cmd._datetime = datetime(2014, 7, 24, 23, 18, 00)
        cmd._datetime_format = '%Y-%m-%d'
        cmd._firstweekday = calendar.MONDAY
        actual_xml = cmd.execute()

        expect_args_list = [(('2014-07-24',),),
                            (('Mo\tTu\tWe\tTh\tFr\tSa\tSu',),),
                            (('\t01\t02\t03\t04\t05\t06\t',),),
                            (('07\t08\t09\t10\t11\t12\t13\t',),),
                            (('14\t15\t16\t17\t18\t19\t20\t',),),
                            (('21\t22\t23\t24\t25\t26\t27\t',),),
                            (('28\t29\t30\t31\t\t\t\t',),)]

        assert expect_args_list == m_append_item.call_args_list
        assert m_xml_s == actual_xml
