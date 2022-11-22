import datetime
from django.utils import timezone


class CronUtils:
    def __init__(self, **kwargs):
        self.cron_string = kwargs.get("cron_string")

    def get_next_date(self):
        # TODO: Currently on Arizona time as of 4/19 make this more robust in future
        today = datetime.datetime.now(tz=timezone.utc).date()
        tomorrow = today + datetime.timedelta(days=1)
        available_days = self.cron_string.split(" ")[4].split(",")
        temp_day = tomorrow
        while temp_day.strftime("%a").upper() not in available_days:
            temp_day += datetime.timedelta(days=1)

        return datetime.datetime.combine(temp_day, datetime.time(), tzinfo=timezone.utc)
