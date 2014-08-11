# -*- coding:utf-8 -*-

import calendar

from nose.tools import raises
from mock import patch, call
from alc.command import CalendarCommand, ThrowingArgumentParser
from freezegun import freeze_time


class Test__Init__():
    '''
    Unit test for *CalendarCommand.__init__()*.
    '''

    def test_default(self):
        '''
        :type: normal
        :case: call this method..
        :expect: instance variables are set, dynamically.
        '''

        config = {
            'query': 'query',
            'first_week_day': calendar.MONDAY,
            'default_datetime_format': 'default_datetime_format',
            'specified_datetime_format': 'specified_datetime_format'
        }
        cmd = CalendarCommand(config)

        assert cmd._query == 'query'
        assert cmd._first_week_day == calendar.MONDAY
        assert cmd._default_datetime_format == 'default_datetime_format'
        assert cmd._specified_datetime_format == 'specified_datetime_format'

    def test_config_key_is_empty(self):
        '''
        :type: normal
        :case: specified config key is not defined.
        :expect: using default value.
        '''

        config = {}
        cmd = CalendarCommand(config)

        assert cmd._query == ''
        assert cmd._first_week_day == calendar.MONDAY
        assert cmd._default_datetime_format == '%Y/%m/%d (%a)\t%H:%M:%S'
        assert cmd._specified_datetime_format == '%Y/%m'

    def test_invalid_config_key_is_included(self):
        '''
        :type: normal
        :case: invalid config key is included.
        :expect: not raise.
        '''
        config = {
            'invalid_key': 'invalid_value'
        }
        cmd = CalendarCommand(config)

        assert cmd._query == ''
        assert cmd._first_week_day == calendar.MONDAY
        assert cmd._default_datetime_format == '%Y/%m/%d (%a)\t%H:%M:%S'
        assert cmd._specified_datetime_format == '%Y/%m'


class TestGetQueryParser():
    '''
    Unit test for *CalendarCommand.get_query_parser()*.
    '''

    @patch('alc.command.ThrowingArgumentParser.add_argument')
    def test_default(self, m_add_argument):
        '''
        :type: normal
        :case: call this method.
        :expect: specified arguments are registered.
        '''
        cmd = CalendarCommand({})
        cmd.get_query_parser()

        m_add_argument.assert_any_call('month', nargs='?',
                                       type=int, choices=range(1, 13))
        m_add_argument.assert_any_call('year', nargs='?',
                                       type=int, choices=range(0, 10000))


class TestExecute():
    '''
    Unit test for *CalendarCommand.execute()*.
    '''

    @patch('argparse.ArgumentParser.parse_args')
    @patch('alc.command.CalendarCommand.take_action',
           return_value='dummy')
    @patch('alc.command.CalendarCommand.get_query_parser',
           return_value=ThrowingArgumentParser())
    def test_default(self, m_get_query_parser, m_take_action, m_parse_args):
        '''
        :type: normal
        :case: call this method.
        :expect: return string of *take_action*.
        '''
        cmd = CalendarCommand({})
        actual = cmd.execute()
        expect = m_take_action.return_value

        m_get_query_parser.assert_called_once_with()
        m_parse_args.assert_called_once_with(cmd._query)
        m_take_action(vars(m_parse_args.return_value))

        assert actual == expect

    @patch('alc.command.CalendarCommand.error_action',
           return_value='dummy')
    @patch('alc.command.CalendarCommand.get_query_parser',
           side_effect=Exception('dummy'))
    def test_raise_any_exception(self, m_get_query_parser, m_error_action):
        '''
        :type: error
        :case: raise any exception.
        :expect: return string of *errro_action*.
        '''
        cmd = CalendarCommand({})
        actual = cmd.execute()
        expect = m_error_action.return_value

        assert actual == expect

    @raises(ValueError)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('alc.command.CalendarCommand.take_action',
           return_value=object)
    @patch('alc.command.CalendarCommand.get_query_parser',
           return_value=ThrowingArgumentParser())
    def test_xml_is_not_string(
            self, m_get_query_parser, m_take_action, m_parse_args):
        '''
        :type: error
        :case: raise any exception.
        :expect: raise ValueError.
        '''
        cmd = CalendarCommand({})
        cmd.execute()


class TestTakeAction():
    '''
    Unit test for *CalendarCommand.take_action()*.
    '''

    @patch('alc.script_filter.ScriptFilter.xml_s')
    @patch('alc.script_filter.ScriptFilter.append_item')
    @freeze_time('2014-07-24 23:18:00')
    def test_default(self, m_append_item, m_xml_s):
        '''
        :type: normal
        :case: query is empty.
        :expect: current datetime is diplayed .
        '''
        cmd = CalendarCommand({})
        actual = cmd.take_action({})

        expect_args_list = [call('2014/07/24 (Thu)\t23:18:00'),
                            call('Mo\tTu\tWe\tTh\tFr\tSa\tSu'),
                            call('\t01\t02\t03\t04\t05\t06\t'),
                            call('07\t08\t09\t10\t11\t12\t13\t'),
                            call('14\t15\t16\t17\t18\t19\t20\t'),
                            call('21\t22\t23\t24\t25\t26\t27\t'),
                            call('28\t29\t30\t31\t\t\t\t')]

        assert expect_args_list == m_append_item.call_args_list
        assert m_xml_s == actual

    @patch('alc.script_filter.ScriptFilter.xml_s')
    @patch('alc.script_filter.ScriptFilter.append_item')
    @freeze_time('2014-07-24 23:18:00')
    def test_specfied_month(self, m_append_item, m_xml_s):
        '''
        :type: normal
        :case: specified month in query.
        :expect: specifed month is diplayed .
        '''
        cmd = CalendarCommand({})
        actual = cmd.take_action({'month': 7, 'year': None})

        expect_args_list = [call('2014/07'),
                            call('Mo\tTu\tWe\tTh\tFr\tSa\tSu'),
                            call('\t01\t02\t03\t04\t05\t06\t'),
                            call('07\t08\t09\t10\t11\t12\t13\t'),
                            call('14\t15\t16\t17\t18\t19\t20\t'),
                            call('21\t22\t23\t24\t25\t26\t27\t'),
                            call('28\t29\t30\t31\t\t\t\t')]

        assert expect_args_list == m_append_item.call_args_list
        assert m_xml_s == actual

    @patch('alc.script_filter.ScriptFilter.xml_s')
    @patch('alc.script_filter.ScriptFilter.append_item')
    @freeze_time('2014-07-24 23:18:00')
    def test_specfied_month_and_year(self, m_append_item, m_xml_s):
        '''
        :type: normal
        :case: specified month and year in query.
        :expect: specifed month year are diplayed .
        '''
        cmd = CalendarCommand({})
        actual = cmd.take_action({'month': 7, 'year': 2014})

        expect_args_list = [call('2014/07'),
                            call('Mo\tTu\tWe\tTh\tFr\tSa\tSu'),
                            call('\t01\t02\t03\t04\t05\t06\t'),
                            call('07\t08\t09\t10\t11\t12\t13\t'),
                            call('14\t15\t16\t17\t18\t19\t20\t'),
                            call('21\t22\t23\t24\t25\t26\t27\t'),
                            call('28\t29\t30\t31\t\t\t\t')]

        assert expect_args_list == m_append_item.call_args_list
        assert m_xml_s == actual


class TestErrorAction():
    '''
    Unit test for *CalendarCommand.error_action()*.
    '''

    @patch('alc.script_filter.ScriptFilter.xml_s')
    @patch('alc.script_filter.ScriptFilter.append_item')
    def test_default(self, m_append_item, m_xml_s):
        '''
        :type: normal
        :case: call this method.
        :expect: error node is appended.
        '''
        ex = Exception('dummy')
        cmd = CalendarCommand({})

        actual_xml = cmd.error_action(ex)

        expect_args_list = [
            call('usage: alc [month (1-12)] [year (1900-9999)]')
        ]

        assert expect_args_list == m_append_item.call_args_list
        assert m_xml_s == actual_xml
