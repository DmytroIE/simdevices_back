from django.utils.timezone import datetime


class DateTimeToUnixConverter:
    regex = '[0-9]{13}'

    def to_python(self, value):
        miliseconds = int(value)
        return datetime.fromtimestamp(miliseconds / 1000.0)

    def to_url(self, value):
        return int(value.timestamp() * 1000)



# https://stackoverflow.com/questions/56890806/django-url-converters-for-date-time-values
# https://stackoverflow.com/questions/70768547/how-to-pass-date-and-id-through-url-in-django