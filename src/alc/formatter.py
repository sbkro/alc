# -*- coding:utf-8 -*-

import calendar


class CalendarFormatter:
    '''
    Provide functions to getting string from specified datetime.

    :param datetime datetime: be formatted datetime.
    '''

    def __init__(self, datetime):
        self._datetime = datetime

    def datetime(self, datetime_format='%Y/%m/%d'):
        '''
        Return a string that is converted in the specified format.
        Conforms a specification of datetime class.

        .. seealso::
            http://docs.python.org/2/library/datetime.html#strftime-strptime-behavior

        :param str datetime_format: datetime format.
        :rtype: str
        :return: formatted datetime.
        '''
        return self._datetime.strftime(datetime_format)

    def weekdays(self):
        '''
        Return a matrix of calendar from specified datetime.
        Day format is '%02d' and during the date separeted by tab.

        :rtype: generator
        :return: matrix of calendar.
        '''

        y = self._datetime.year
        m = self._datetime.month

        for w in calendar.monthcalendar(y, m):
            formatter = lambda x: '%02d\t' % x if (x != 0) else '\t'
            yield ''.join(map(formatter, w))

    @classmethod
    def weekheader(cls):
        '''
        Return a week header.

        e.g.::

            CalendarFormatter.weekheader()
            # Mo\tTu\tWe\tTh\tFr\tSt\tSu

        :rtype: str
        :return: week header.
        '''
        return calendar.weekheader(2).replace(' ', '\t')

    @classmethod
    def setfirstweekday(cls, firstweekday):
        '''
        Set the weekday to start each week.

        :param int firstweekday:
            first week day (0 is Monday, 6 is Sunday).
            Use constant of calendar class.

        e.g.::

            import calendar
            CalendarFormatter.setfirstweekday(calendar.MONDAY)

        '''
        calendar.setfirstweekday(firstweekday)

    @classmethod
    def default_firstweekday(cls):
        '''
        Return a first week day.
        Monday is always returned.

        :return: calendar.MONDAY
        '''
        return calendar.MONDAY
