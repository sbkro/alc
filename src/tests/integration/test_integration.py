# -*- coding: utf-8 -*-

import calendar

from alc.command import CalendarCommand
from freezegun import freeze_time


@freeze_time('2014-07-26 12:00:00')
def test_default():
    '''
    Integration scenario when have not been put parameter in Aflred's prompt.
    '''

    config = {
        'query': '',
        'first_week_day': calendar.SUNDAY,
        'default_datetime_format': '%Y/%m/%d (%a)\t%H:%M:%S',
        'specified_datetime_format': '%Y/%m'
    }
    expect = '<items>' + \
             '<item autocomplete="" uid="0" valid="no">' + \
             '<title>2014/07/26 (Sat)\t12:00:00</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="1" valid="no">' + \
             '<title>Su\tMo\tTu\tWe\tTh\tFr\tSa</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="2" valid="no">' + \
             '<title>\t\t01\t02\t03\t04\t05\t</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="3" valid="no">' + \
             '<title>06\t07\t08\t09\t10\t11\t12\t</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="4" valid="no">' + \
             '<title>13\t14\t15\t16\t17\t18\t19\t</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="5" valid="no">' + \
             '<title>20\t21\t22\t23\t24\t25\t26\t</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="6" valid="no">' + \
             '<title>27\t28\t29\t30\t31\t\t\t</title>' + \
             '</item>' + \
             '</items>'

    actual = CalendarCommand(config).execute()

    assert expect == actual


@freeze_time('2014-07-26 12:00:00')
def test_query_is_space_only():
    '''
    Integration scenario when have not been put parameter in Aflred's prompt.
    '''

    config = {
        'query': '   ',
        'first_week_day': calendar.SUNDAY,
        'default_datetime_format': '%Y/%m/%d (%a)\t%H:%M:%S',
        'specified_datetime_format': '%Y/%m'
    }
    expect = '<items>' + \
             '<item autocomplete="" uid="0" valid="no">' + \
             '<title>2014/07/26 (Sat)\t12:00:00</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="1" valid="no">' + \
             '<title>Su\tMo\tTu\tWe\tTh\tFr\tSa</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="2" valid="no">' + \
             '<title>\t\t01\t02\t03\t04\t05\t</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="3" valid="no">' + \
             '<title>06\t07\t08\t09\t10\t11\t12\t</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="4" valid="no">' + \
             '<title>13\t14\t15\t16\t17\t18\t19\t</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="5" valid="no">' + \
             '<title>20\t21\t22\t23\t24\t25\t26\t</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="6" valid="no">' + \
             '<title>27\t28\t29\t30\t31\t\t\t</title>' + \
             '</item>' + \
             '</items>'

    actual = CalendarCommand(config).execute()

    assert expect == actual


def test_query_inclued_month():
    '''
    Integration scenario when have been put month in Aflred's prompt.
    '''
    config = {
        'query': '1',
        'first_week_day': calendar.SUNDAY,
        'default_datetime_format': '%Y/%m/%d (%a)\t%H:%M:%S',
        'specified_datetime_format': '%Y/%m'
    }
    expect = '<items>' + \
             '<item autocomplete="" uid="0" valid="no">' + \
             '<title>2014/01</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="1" valid="no">' + \
             '<title>Su\tMo\tTu\tWe\tTh\tFr\tSa</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="2" valid="no">' + \
             '<title>\t\t\t01\t02\t03\t04\t</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="3" valid="no">' + \
             '<title>05\t06\t07\t08\t09\t10\t11\t</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="4" valid="no">' + \
             '<title>12\t13\t14\t15\t16\t17\t18\t</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="5" valid="no">' + \
             '<title>19\t20\t21\t22\t23\t24\t25\t</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="6" valid="no">' + \
             '<title>26\t27\t28\t29\t30\t31\t\t</title>' + \
             '</item>' + \
             '</items>'

    actual = CalendarCommand(config).execute()

    assert expect == actual


def test_query_include_month_and_year():
    '''
    Integration scenario when have been put month and year in Aflred's prompt.
    '''
    config = {
        'query': '1 2013',
        'first_week_day': calendar.SUNDAY,
        'default_datetime_format': '%Y/%m/%d (%a)\t%H:%M:%S',
        'specified_datetime_format': '%Y/%m'
    }
    expect = '<items>' + \
             '<item autocomplete="" uid="0" valid="no">' + \
             '<title>2013/01</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="1" valid="no">' + \
             '<title>Su\tMo\tTu\tWe\tTh\tFr\tSa</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="2" valid="no">' + \
             '<title>\t\t01\t02\t03\t04\t05\t</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="3" valid="no">' + \
             '<title>06\t07\t08\t09\t10\t11\t12\t</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="4" valid="no">' + \
             '<title>13\t14\t15\t16\t17\t18\t19\t</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="5" valid="no">' + \
             '<title>20\t21\t22\t23\t24\t25\t26\t</title>' + \
             '</item>' + \
             '<item autocomplete="" uid="6" valid="no">' + \
             '<title>27\t28\t29\t30\t31\t\t\t</title>' + \
             '</item>' + \
             '</items>'

    actual = CalendarCommand(config).execute()

    assert expect == actual


def test_query_is_invalid():
    '''
    Integration scenario when have been put invalid query in Aflred's prompt.
    '''
    config = {
        'query': '13 2013',
        'first_week_day': calendar.SUNDAY,
        'default_datetime_format': '%Y/%m/%d (%a)\t%H:%M:%S',
        'specified_datetime_format': '%Y/%m'
    }
    expect = '<items>' + \
             '<item autocomplete="" uid="0" valid="no">' + \
             '<title>usage: alc [month (1-12)] [year (1900-9999)]</title>' + \
             '</item>' + \
             '</items>'

    actual = CalendarCommand(config).execute()

    assert expect == actual
