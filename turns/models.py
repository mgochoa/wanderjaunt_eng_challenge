from typing import Generator
import datetime
from datetime import date

from django.db import models

from dateutil import relativedelta


class ValidationError(Exception):
    def __init__(self, error_type, *args):
        self.message = error_type + f': {args[0]}' if args else ' has been raised'


class Turn(models.Model):
    created_at = models.DateField()
    scheduled_for = models.DateField()
    is_same_day = models.BooleanField()

    @staticmethod
    def projected_sameday_turns(asked_date: date) -> float:
        return Turn.projected_turns(asked_date, True)

    @staticmethod
    def projected_turns(asked_date: date, is_same_day=False) -> float:
        """
        return the projected number of turns for the future date, based on other records
        :param is_same_day: Flag to filter the same day turns in the projection
        :param asked_date:
        :return:
        """
        is_same_day_filter = [True, False] if not is_same_day else [is_same_day]
        today = date.today()
        if asked_date < today:
            raise ValidationError('asked_date should be greater than today')
        today_month_ago = today - relativedelta.relativedelta(months=1)
        num_scheduled_turns = Turn.objects.filter(scheduled_for=asked_date, is_same_day__in=is_same_day_filter).count()
        last_month_average_turns = []
        scheduled_turns_for_current_range = None
        is_analyzing_range = False
        for day in Turn._get_date_range(today_month_ago, today):
            if day.weekday() == today.weekday():
                is_analyzing_range = True
                scheduled_turns_for_current_range = []
            if is_analyzing_range:
                scheduled_turns_for_current_range.append(
                    Turn.objects.filter(scheduled_for=day, is_same_day__in=is_same_day_filter).count())
            if day.weekday() == asked_date.weekday():
                is_analyzing_range = False
                if scheduled_turns_for_current_range:
                    last_month_average_turns.append(sum(scheduled_turns_for_current_range))
                    scheduled_turns_for_current_range = []
        projected_turns = num_scheduled_turns + sum(last_month_average_turns) / len(last_month_average_turns)
        return float('%.2f' % projected_turns)

    @staticmethod
    def _get_date_range(start_date, end_date, steps=1) -> Generator[date, None, None]:
        """
        Get generator to iterate throw a start_date and end_date
        :param start_date:
        :param end_date:
        :param steps:
        :return:
        """
        num_days = (end_date - start_date).days
        for x in range(0, num_days, steps):
            yield start_date + datetime.timedelta(days=x)
