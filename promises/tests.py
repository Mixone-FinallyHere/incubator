from django.test import TestCase
from users.models import User
from .models import Promise, Slot
from .utils import flatten_promises, compare_slots_and_promises

import pytest
import datetime

pytestmark = pytest.mark.django_db

def create_promises(start_datetime, end_datetime):
    user1 = User.objects.create(username="User1", email="le1@la.com")

    # Because django converts this to UTC, it for whatever dumb random-ass reason subtracts 18 minutes from the times,
    #   hence the abomination below does not logically match up to the solutions shown lower but fuck it,
    #   I ain't redrawing my diagrams all over again.

    # Testing one promise beginning in the middle of another and ending after it.
    promise1 = Promise.objects.create(start=start_datetime.replace(hour=12, minute=40),stop=start_datetime.replace(hour=14, minute=20),user=user1) # 12:40 - 14:20
    promise2 = Promise.objects.create(start=start_datetime.replace(hour=13, minute=0),stop=start_datetime.replace(hour=16, minute=0),user=user1)   # 13:00 - 16:00

    # One lone promise with no overlaps
    promise3 = Promise.objects.create(start=start_datetime.replace(hour=16, minute=30),stop=start_datetime.replace(hour=17, minute=15),user=user1) # 16:30 - 17:15

    # One promise fully encampsulated within another
    promise4 = Promise.objects.create(start=start_datetime.replace(hour=18, minute=0),stop=start_datetime.replace(hour=22, minute=0),user=user1)   # 18:00 - 22:00
    promise5 = Promise.objects.create(start=start_datetime.replace(hour=19, minute=40),stop=start_datetime.replace(hour=21, minute=0),user=user1)  # 19:40 - 21:00

def test_promises_flattening():
    start_datetime = datetime.datetime(year=42, month=1, day=1, hour=0, minute=0, tzinfo=None)
    end_datetime = datetime.datetime(year=42, month=1, day=1, hour=23, minute=59,tzinfo=None)

    create_promises(start_datetime, end_datetime)

    flattened_promise_list = flatten_promises(start_datetime, end_datetime)
    correct_list = [(start_datetime.replace(hour=12, minute=22),start_datetime.replace(hour=15, minute=42)),
                    (start_datetime.replace(hour=16, minute=12),start_datetime.replace(hour=16, minute=57)),
                    (start_datetime.replace(hour=17, minute=42),start_datetime.replace(hour=21, minute=42)),]

    # Getting rid of that pesky timezone awareness
    flattened_promise_list = [[part.replace(tzinfo=None) for part in promise] for promise in flattened_promise_list]

    # For yet another ungoldy reason, correctlist[0] == flattenedlist[0] fails but checking each element of the tuple separately works ._.
    for i in range(len(correct_list)):
        for j in range(len(correct_list[i])):
            assert correct_list[i][j] == flattened_promise_list[i][j]


def test_promise_slot_comparison():

    start_datetime = datetime.datetime(year=42, month=1, day=1, hour=0, minute=0, tzinfo=None)
    end_datetime = datetime.datetime(year=42, month=1, day=1, hour=23, minute=59,tzinfo=None)

    create_promises(start_datetime, end_datetime)

    # starts before and ends during the promise
    slot1 = Slot.objects.create(start=start_datetime.replace(hour=12, minute=30),stop=start_datetime.replace(hour=15, minute=0))

    # starts during and ends after the promise
    slot2 = Slot.objects.create(start=start_datetime.replace(hour=15, minute=55),stop=start_datetime.replace(hour=16, minute=15))

    # fully covered by a promise
    slot3 = Slot.objects.create(start=start_datetime.replace(hour=16, minute=30),stop=start_datetime.replace(hour=17, minute=15))

    # starts before and ends after a promise with the middle of it covered
    slot4 = Slot.objects.create(start=start_datetime.replace(hour=17, minute=30),stop=start_datetime.replace(hour=22, minute=15))

    # not covered at all, is after all the promises
    slot5 = Slot.objects.create(start=start_datetime.replace(hour=22, minute=40),stop=start_datetime.replace(hour=23, minute=00))

    unfilled_slots = compare_slots_and_promises(start_datetime, end_datetime)

    correct_list = [(start_datetime.replace(hour=12, minute=12),start_datetime.replace(hour=12, minute=22)),
                    (start_datetime.replace(hour=15, minute=42),start_datetime.replace(hour=15, minute=57)),
                    (start_datetime.replace(hour=17, minute=12),start_datetime.replace(hour=17, minute=42)),
                    (start_datetime.replace(hour=21, minute=42),start_datetime.replace(hour=21, minute=57)),
                    (start_datetime.replace(hour=22, minute=22),start_datetime.replace(hour=22, minute=42)),]

    # Stupid timezones
    unfilled_slots = [[part.replace(tzinfo=None) for part in slot] for slot in unfilled_slots]

    for i in range(len(correct_list)):
        for j in range(len(correct_list[i])):
            assert correct_list[i][j] == unfilled_slots[i][j]



def test_promise_slot_comparison_2():
    start_datetime = datetime.datetime(year=42, month=1, day=1, hour=0, minute=0, tzinfo=None)
    end_datetime = datetime.datetime(year=42, month=1, day=1, hour=23, minute=59,tzinfo=None)

    create_promises(start_datetime, end_datetime)

    # Spans almost the whole day, intersecting with many promises but also having a lot of unfilled blanks
    slot1 = Slot.objects.create(start=start_datetime.replace(hour=12, minute=30),stop=start_datetime.replace(hour=22, minute=1))

    unfilled_slots = compare_slots_and_promises(start_datetime, end_datetime)

    correct_list = [(start_datetime.replace(hour=12, minute=12),start_datetime.replace(hour=12, minute=22)),
                    (start_datetime.replace(hour=15, minute=42),start_datetime.replace(hour=16, minute=12)),
                    (start_datetime.replace(hour=16, minute=57),start_datetime.replace(hour=17, minute=42)),
                    (start_datetime.replace(hour=21, minute=42),start_datetime.replace(hour=21, minute=43)),]

    # Stupid timezones
    unfilled_slots = [[part.replace(tzinfo=None) for part in slot] for slot in unfilled_slots]

    for i in range(len(correct_list)):
        for j in range(len(correct_list[i])):
            assert correct_list[i][j] == unfilled_slots[i][j]
