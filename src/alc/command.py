# -*- coding:utf-8 -*-

import argparse

from alc.formatter import CalendarFormatter
from alc.script_filter import ScriptFilter
from datetime import datetime


class ArgumentParserError(Exception):
    '''
    When failed to parse argument, this exception is raised.
    '''
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    '''
    This is a wrapper class of *argparse.ArgumentParser*.
    When failed to parse argument, raise *ArgumentParserError*.
    '''

    def error(self, message):
        '''
        :raise ArgumentParserError: failed to parse arguments.
        '''
        raise ArgumentParserError(message)


class CalendarCommand:
    '''
    Command for getting *Script Filter XML* of calendar.

    e.g.::

        config = {
            'query': '{query}',
            'first_week_day': calendar.MONDAY,
            'default_datetime_format': '%Y/%m/%d (%a)\t%H:%M:%S',
            'specified_datetime_format': '%Y/%m'
        }
        print CalendarCommand(config).execute()

    :param dict config: configuration of command. The format is as follow.

    +---------------------------+------+----------------------------+
    | key                       | type | default                    |
    +===========================+======+============================+
    | query                     | str  | ''                         |
    +---------------------------+------+----------------------------+
    | first_week_day            | int  | 0 (Mon.)                   |
    +---------------------------+------+----------------------------+
    | default_datetime_format   | str  | '%Y/%m/%d (%a) %H:%M:%S'   |
    +---------------------------+------+----------------------------+
    | specified_datetime_format | str  | '%Y/%m'                    |
    +---------------------------+------+----------------------------+

    '''

    def __init__(self, config):
        if ('first_week_day' in config) is False:
            config['first_week_day'] = CalendarFormatter.default_firstweekday()

        if ('query' in config) is False:
            config['query'] = ''

        if ('default_datetime_format' in config) is False:
            config['default_datetime_format'] = '%Y/%m/%d (%a)\t%H:%M:%S'

        if ('specified_datetime_format' in config) is False:
            config['specified_datetime_format'] = '%Y/%m'

        self._firstweekday = config['first_week_day']

        parsed_query = self._parse_query(config['query'])
        len_parsed_query = len([k for k in parsed_query.keys()
                                if parsed_query[k] is not None])

        tmp_datetime = datetime.now()
        tmp_dateformat = ''

        if len_parsed_query is 0:
            tmp_dateformat = config['default_datetime_format']
        else:
            month = parsed_query['month']
            year = parsed_query['year'] if (len_parsed_query is 2) \
                else tmp_datetime.year

            tmp_datetime = datetime.strptime('%s-%s' % (year, month), '%Y-%m')
            tmp_dateformat = config['specified_datetime_format']

        self._datetime = tmp_datetime
        self._datetime_format = tmp_dateformat

    def _parse_query(self, query):
        args = query.strip().split(' ') if query.strip() != '' else ''

        parser = ThrowingArgumentParser(description='parser for query.')
        parser.add_argument('month', nargs='?', type=int,
                            choices=range(1, 13))
        parser.add_argument('year', nargs='?', type=int,
                            choices=range(0, 10000))

        try:
            return vars(parser.parse_args(args))
        except ArgumentParserError as e:
            return {'error': e.message}

    def execute(self):
        '''
        Execute thie command. Return string of *Script Filter XML*.

        :rtype: str
        :return: *Script Filter XML*
        '''

        sf = ScriptFilter()
        f = CalendarFormatter(self._datetime)
        CalendarFormatter.setfirstweekday(self._firstweekday)

        sf.append_item(f.datetime(self._datetime_format))
        sf.append_item(f.weekheader())
        for w in f.weekdays():
            sf.append_item(w)

        return sf.xml_s
