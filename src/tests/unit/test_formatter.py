# -*- coding:utf-8 -*-

import calendar

from mock import patch
from datetime import datetime
from alc.formatter import CalendarFormatter


class TestDatetime:
    '''
    Unit test for *CalendarFormatter.datetime()*.
    '''

    def test_default(self):
        '''
        :type: normal
        :case: *datetime_format* is None.
        :expect: convert datetime using default format (%Y/%m/%d).
        '''
        cf = CalendarFormatter(datetime(2014, 7, 24, 23, 18, 00))

        expect = '2014/07/24'
        actual = cf.datetime()

        assert expect == actual

    def test_datetime_format_is_specified(self):
        '''
        :type: normal
        :case: *datetime_format* is specified.
        :expect: convert datetime using specified format.
        '''
        cf = CalendarFormatter(datetime(2014, 7, 24, 23, 18, 00))

        expect = '2014/07/24 23:18:00'
        actual = cf.datetime('%Y/%m/%d %H:%M:%S')

        assert expect == actual


class TestWeekheader:
    '''
    Unit test for *CalendarFormatter.weekheader()*.
    '''

    def test_default(self):
        '''
        :type: normal
        :case: call this method.
        :expect: get a week header.
        '''
        expect = 'Mo\tTu\tWe\tTh\tFr\tSa\tSu'
        actual = CalendarFormatter.weekheader()
        assert expect == actual

    def test_first_weekday_is_specified(self):
        '''
        :type: normal
        :case: set the first week day in advance. (Sunday)
        :expect: get a week header of start Sunday.
        '''
        calendar.setfirstweekday(calendar.SUNDAY)
        expect = 'Su\tMo\tTu\tWe\tTh\tFr\tSa'
        actual = CalendarFormatter.weekheader()
        assert expect == actual


class TestWeekdays:
    '''
    Unit test for *CalendarFormatter.weekdays()*.
    '''

    def test_default(self):
        '''
        :type: normal
        :case: call this method. datetime is '2014/07'.
        :expect: get a calendar for '2014/07'.
        '''
        cf = CalendarFormatter(datetime(2014, 7, 24, 23, 18, 00))

        expect = [
            '\t01\t02\t03\t04\t05\t06\t',
            '07\t08\t09\t10\t11\t12\t13\t',
            '14\t15\t16\t17\t18\t19\t20\t',
            '21\t22\t23\t24\t25\t26\t27\t',
            '28\t29\t30\t31\t\t\t\t'
        ]

        for i, w in enumerate(cf.weekdays()):
            assert expect[i] == w


class TestSetfirstweekday:
    '''
    Unit test for *CalendarFormatter.setfirstweekday()*.
    '''

    @patch('calendar.setfirstweekday')
    def test_default(self, m_setfirstweekday):
        '''
        :type: normal
        :case: call this method.
        :expect: call *calendar.setfirstweekday*.
        '''
        CalendarFormatter.setfirstweekday(calendar.MONDAY)
        m_setfirstweekday.assert_called_once_with(calendar.MONDAY)
