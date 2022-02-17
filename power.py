
#!/usr/bin/env python3
# SPDX-License-Identifier: LGPL-2.1-or-later
from utils import Characteristic, Descriptor, NotPermittedException, Service


import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service

import array
try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject
import sys

from random import randint


class PowerService(Service):
    """
    Dummy Cellular service that provides characteristics and descriptors that
    exercise various API functionality.

    """
    POWER_SVC_UUID = '180D'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.POWER_SVC_UUID, True)
        self.add_characteristic(SleepDelay(bus, 0, self))
        self.add_characteristic(Sleep(bus, 1, self))


class SleepDelay(Characteristic):
    """


    """
    SLEEP_DELAY_ID = '552d0f70-c83b-4c68-a7d9-5993f31191c4'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.SLEEP_DELAY_ID,
            ['read', 'write'],
            service)
        self.value = []
        self.add_descriptor(SleepDelayDescriptor(bus, 0, self))

    def ReadValue(self, options):
        return "30 min"

    def WriteValue(self, value, options):
        print('SleepDelay Write: ' + repr(value))
        self.value = value
        # Run logic to change the sleep delay


class SleepDelayDescriptor(Descriptor):
    """

    """
    SLEEP_DELAY_D_ID = '64784856-e249-4977-99be-4b3477789d11'

    def __init__(self, bus, index, characteristic):
        Descriptor.__init__(
            self, bus, index,
            self.SLEEP_DELAY_D_ID,
            ['read', 'write'],
            characteristic)

    def ReadValue(self, options):
        return [
            dbus.Byte('T'), dbus.Byte('e'), dbus.Byte('s'), dbus.Byte('t')
        ]


class Sleep(Characteristic):
    """
    If this is written to put the AutoPI to sleep.

    """
    SLEEP_ID = '03becea2-e15f-4537-b350-2bd8853c72cf'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.SLEEP_ID,
            ['write'],
            service)
        self.value = []
        self.add_descriptor(SleepDescriptor(bus, 0, self))

    def WriteValue(self, value, options):
        print('Sleep Write: ' + repr(value))
        self.value = value
        # Run logic to sleep


class SleepDescriptor(Descriptor):
    """

    """
    SLEEP_D_ID = '7de2925b-b7b6-4dfb-9d86-800d3d23fa68'

    def __init__(self, bus, index, characteristic):
        Descriptor.__init__(
            self, bus, index,
            self.SLEEP_D_ID,
            ['write'],
            characteristic)

    def ReadValue(self, options):
        return [
            dbus.Byte('T'), dbus.Byte('e'), dbus.Byte('s'), dbus.Byte('t')
        ]
