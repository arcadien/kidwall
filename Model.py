from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Usage:
    begin: datetime
    end: datetime


@dataclass
class Ip:

    def __init__(self, address: str, mask: int = 32):
        self.adress = address
        self.mask = mask


class Application:
    """
    An application is a web application which can be allowed or restricted
    e.g. Youtube, Fortnite
    """

    def __init__(self, name: str):
        self.name = name
        self.ips: list[Ip] = []
        self.isActive: bool = False


class Registration:
    def __init__(self, application: Application, isAllowed: bool):
        self.app: Application = application
        self.isAllowed: bool = isAllowed
        self.usages: List[Usage] = []
        self.usageStart: datetime | None = None


class Engine:

    def __init__(self):
        self.registrations: dict[str, Registration] = {}
        self.ticks: int = 0

    def add(self, application: Application, isAllowed: bool) -> None:
        self.registrations[application.name] = Registration(application, isAllowed)

    def isAllowed(self, application: Application) -> bool:
        if application.name in self.registrations:
            return self.registrations[application.name].isAllowed
        else:
            raise "Unknown application " + application.name

    def allow(self, application: Application) -> None:
        if application.name in self.registrations:
            self.registrations[application.name].isAllowed = True
        else:
            raise "Unknown application " + application.name

    def disallow(self, application: Application) -> None:
        if application.name in self.registrations:
            self.registrations[application.name].isAllowed = False
        else:
            raise "Unknown application " + application.name

    def tick(self, time: datetime) -> None:
        """
        Should be called at regular interval, to allow application usage measurement
        """
        self.ticks += 1
        for name, registration in self.registrations.items():
            if registration.app.isActive:
                if registration.usageStart is None:
                    # switched to active: begin usage
                    registration.usageStart = time
            else:
                if registration.usageStart is not None:
                    # switched to inactive: end and log usage
                    registration.usages.append(Usage(registration.usageStart, time))
                    registration.usageStart = None

    def getStatistics(self, application: Application) -> int:
        return self.statistics[application.name]
