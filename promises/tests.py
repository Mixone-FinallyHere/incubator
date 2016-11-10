from django.test import TestCase
from users.models import User
from .models import Promise, Slot
from .utils import flatten_promises


import pytest
import datetime
# Create your tests here.


def test_promises_flattening():
    user1 = User.objects.create(name="User1", email="le1@la.com")

    start_datetime = datetime.datetime(year=42, month=1, day=1, hour=0, minute=0)
    end_datetime = datetime.datetime(year=42, month=1, day=1, hour=23, minute=59)

    # Testing one promise beginning in the middle of another and ending after it.
    promise1 = Promise.objects.create(start=start_datetime.replace(hour=12, minute=40),stop=start_datetime.replace(hour=14, minute=20),user=user1) # 12:40 - 14:20
    promise2 = Promise.objects.create(start=start_datetime.replace(hour=13, minute=0),stop=start_datetime.replace(hour=16, minute=0),user=user1)   # 13:00 - 16:00

    # One lone promise with no overlaps
    promise3 = Promise.objects.create(start=start_datetime.replace(hour=16, minute=30),stop=start_datetime.replace(hour=17, minute=15),user=user1) # 16:30 - 17:15

    # One promise fully encampsulated within another
    promise4 = Promise.objects.create(start=start_datetime.replace(hour=18, minute=0),stop=start_datetime.replace(hour=22, minute=0),user=user1)   # 18:00 - 22:00
    promise5 = Promise.objects.create(start=start_datetime.replace(hour=19, minute=40),stop=start_datetime.replace(hour=21, minute=0),user=user1)  # 19:40 - 21:00

    flattened_promise_list = flatten_promises(start, end_datetime)
    correct_list = [(start_datetime.replace(hour=12, minute=40),start_datetime.replace(hour=16, minute=0)),
                    (start_datetime.replace(hour=16, minute=30),start_datetime.replace(hour=17, minute=15)),
                    (start_datetime.replace(hour=18, minute=00),start_datetime.replace(hour=22, minute=0)),]

    assert flattened_promise_list == correct_list