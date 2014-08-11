# -*- coding:utf-8 -*-

import argparse
import calendar

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

    :param dict config: configuration of command. The format is as follow.

    example::

        config = {
            'query': '{query}',
            'first_week_day': calendar.MONDAY,
            'default_datetime_format': '%Y/%m/%d (%a)\t%H:%M:%S',
            'specified_datetime_format': '%Y/%m'
        }
        print CalendarCommand(config).execute()

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

    _class_val_defs = {
        'query': '',
        'first_week_day': calendar.MONDAY,
        'default_datetime_format': '%Y/%m/%d (%a)\t%H:%M:%S',
        'specified_datetime_format': '%Y/%m'
    }

    def __init__(self, config):
        for k, v in self._class_val_defs.items():
            value = config[k] if (k in config) else v
            setattr(self, '_{0}'.format(k), value)

    def execute(self):
        '''
        Execute thie command. Return string of *Script Filter XML*.

        :rtype: str
        :return: *Script Filter XML*
        :raise ValueError:
            If return type of *take_action* or *error_action* is not string.
        '''

        filter_xml = ''
        try:
            parser = self.get_query_parser()
            args = (self._query.strip().split(' ')
                    if self._query.strip() != '' else '')
            parsed_args = vars(parser.parse_args(args))
            filter_xml = self.take_action(parsed_args)
        except Exception as e:
            filter_xml = self.error_action(e)

        if isinstance(filter_xml, basestring) is False:
            raise ValueError()

        return filter_xml

    def get_query_parser(self):
        '''
        Return argument parser of this command.

        :rtype: argparse.ArgumentParser
        :return: argument parser
        '''
        parser = ThrowingArgumentParser()

        parser.add_argument('month', nargs='?', type=int,
                            choices=range(1, (12 + 1)))
        parser.add_argument('year', nargs='?', type=int,
                            choices=range(0, (9999 + 1)))

        return parser

    def take_action(self, query_args):
        '''
        Create script filter xml.
        When it succeeds in parsing the query, this method is called.

        :param dict query_args: parsed query
        :rtype: str
        :return: *Script Filter XML*
        '''
        len_query_args = len([k for k in query_args.keys()
                              if query_args[k] is not None])

        tmp_datetime = datetime.now()
        tmp_dateformat = self._default_datetime_format

        if len_query_args is not 0:
            month = query_args['month']
            year = query_args['year'] if (len_query_args is 2) \
                else tmp_datetime.year

            tmp_datetime = datetime.strptime('%s-%s' % (year, month), '%Y-%m')
            tmp_dateformat = self._specified_datetime_format

        sf = ScriptFilter()
        f = CalendarFormatter(tmp_datetime)
        CalendarFormatter.setfirstweekday(self._first_week_day)

        sf.append_item(f.datetime(tmp_dateformat))
        sf.append_item(f.weekheader())
        for w in f.weekdays():
            sf.append_item(w)

        return sf.xml_s

    def error_action(self, e):
        '''
        Create error script filter xml.
        This method is called when an error occurs in *'execute'*.

        :param Exception e: exception from *execute*.
        :rtype: str
        :return: *Script Filter XML*
        '''
        sf = ScriptFilter()
        sf.append_item('usage: alc [month (1-12)] [year (1900-9999)]')
        return sf.xml_s
