from datetime import datetime, timedelta, timezone
import sys
from typing import List
import unittest
import logging

from Model import Application, Usage
from Model import Engine


class ModelTest(unittest.TestCase):

    def test_Application_has_a_name(self):
        app = Application("Fortnite")
        self.assertEqual("Fortnite", app.name)

    def test_application_contains_a_collection_of_ip_address(self):
        app = Application("Fortnite")
        self.assertEqual([], app.ips)

    def test_application_current_activity_can_be_queried(self):
        app = Application("Fortnite")
        self.assertEqual(False, app.isActive)

    def test_engine_maintains_list_of_stateful_applications(self):
        engine = Engine()
        fortnite = Application("Fortnite")
        youtube = Application("Youtube")
        engine.add(application=fortnite, isAllowed=False)
        engine.add(application=youtube, isAllowed=True)

        self.assertEqual(False, engine.isAllowed(fortnite))
        self.assertEqual(True, engine.isAllowed(youtube))

    def test_engine_allow_to_disallow_application(self):
        engine = Engine()
        fortnite = Application("Fortnite")
        engine.add(application=fortnite, isAllowed=True)
        self.assertEqual(True, engine.isAllowed(fortnite))
        engine.disallow(fortnite)
        self.assertEqual(False, engine.isAllowed(fortnite))

    def test_engine_can_allow_application(self):
        engine = Engine()
        fortnite = Application("Fortnite")
        engine.add(application=fortnite, isAllowed=False)
        self.assertEqual(False, engine.isAllowed(fortnite))
        engine.allow(fortnite)
        self.assertEqual(True, engine.isAllowed(fortnite))

    def test_engine_collect_application_usage_as_interval(
        self,
    ):
        self.maxDiff = None

        engine = Engine()
        fortnite = Application("Fortnite")
        engine.add(application=fortnite, isAllowed=False)
        eachFiveMinutesInADay = 24 * 60 * 60 / 5
        time = datetime(year=1970, month=1, day=1, hour=0, minute=0, second=0)
        end = datetime(year=1970, month=1, day=1, hour=23, minute=59, second=59)

        # application is used 20 min per hour between 9 and 22h
        def appIsUsed(time):
            return (
                time.hour >= 9
                and time.hour <= 22
                and time.minute > 20
                and time.minute < 40
            )

        while time < end:
            if appIsUsed(time):
                fortnite.isActive = True
            else:
                fortnite.isActive = False

            engine.tick(time)
            time += timedelta(minutes=1)

        fakeTime = datetime(year=1970, month=1, day=1, hour=9, minute=0, second=0)
        expected: List[Usage] = []
        for usageHour in range(0, 14):
            expected.append(
                Usage(
                    fakeTime + timedelta(minutes=21), fakeTime + timedelta(minutes=40)
                )
            )
            fakeTime += timedelta(hours=1)
        sortedExpected = sorted(expected, key=lambda usage: usage.begin.timestamp())

        self.assertEqual((24 * 60), engine.ticks)
        sortedActual = sorted(
            engine.registrations[fortnite.name].usages,
            key=lambda usage: usage.begin.timestamp(),
        )
        self.assertListEqual(sortedExpected, sortedActual)


if __name__ == "__main__":
    unittest.main()
