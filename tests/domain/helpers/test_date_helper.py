from datetime import datetime
from unittest import TestCase

from domain.helpers.date_helper import convert_str_to_date, generate_datetime


class TestDateHelper(TestCase):
    def test_convert_str_to_date(self):
        result = convert_str_to_date(date_as_string="20220314")
        self.assertIsInstance(result, datetime)
        self.assertEqual(result, datetime(year=2022, month=3, day=14,
                                          hour=0, minute=0, second=0))

    def test_generate_datetime(self):
        result = generate_datetime(min_or_max_datetime="min")
        self.assertIsInstance(result, datetime)
        self.assertEqual(result, datetime(year=2022, month=3, day=1,
                                          hour=0, minute=0, second=0))

        result = generate_datetime(min_or_max_datetime="max")
        self.assertIsInstance(result, datetime)
        self.assertEqual(result, datetime(year=2022, month=3, day=31,
                                          hour=23, minute=59, second=59,
                                          microsecond=999999))
