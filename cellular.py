
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


class CellularService(Service):
    """
    Cellular service

    """
    CELLULAR_SVC_UUID = '180B'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.CELLULAR_SVC_UUID, True)
        self.add_characteristic(CellularStatus(bus, 0, self))
        self.add_characteristic(CellularAPN(bus, 1, self))


class CellularStatus(Characteristic):
    """


    """
    STATUS_C_ID = 'd36a2701-8bd1-413e-bc20-1f655e39dca3'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.STATUS_C_ID,
            ['read', 'notify'],
            service)
        self.value = []
        self.add_descriptor(CellularStatusDescriptor(bus, 0, self))

    def ReadValue(self, options):

        return "{}"

    def StartNotify(self):
        if self.notifying:
            print('Already notifying, nothing to do')
            return

        self.notifying = True
        # Start loop to detect change in value

    def StopNotify(self):
        if not self.notifying:
            print('Not notifying, nothing to do')
            return

        self.notifying = False
        # Stop loop to detect change in value


class CellularStatusDescriptor(Descriptor):
    """

    """
    STATUS_D_UUID = 'eea9d117-6969-4b31-9791-5f06049b21c4'

    def __init__(self, bus, index, characteristic):
        Descriptor.__init__(
            self, bus, index,
            self.STATUS_UUID,
            ['read', 'notify'],
            characteristic)

    def ReadValue(self, options):
        return [
            dbus.Byte('T'), dbus.Byte('e'), dbus.Byte('s'), dbus.Byte('t')
        ]


class CellularAPN(Characteristic):
    """


    """
    APN_UUID = '04c15fb3-9684-4dbf-aa12-24116fc47302'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.APN_UUID,
            ['read', 'write', 'notify'],
            service)
        self.value = []
        self.add_descriptor(CellularStatusDescriptor(bus, 0, self))

    def ReadValue(self, options):
        return "{}"

    def WriteValue(self, value, options):
        print('CellularAPN Write: ' + repr(value))
        self.value = value
        # Run logic to change the APN

    def StartNotify(self):
        if self.notifying:
            print('Already notifying, nothing to do')
            return

        self.notifying = True
        # Start loop to detect change in value

    def StopNotify(self):
        if not self.notifying:
            print('Not notifying, nothing to do')
            return

        self.notifying = False
        # Stop loop to detect change in value


class CellularAPNDescriptor(Descriptor):
    """


    """
    APN_D_ID = '1e8475ad-6fed-4006-8ad7-7a9946c61037'

    def __init__(self, bus, index, characteristic):
        Descriptor.__init__(
            self, bus, index,
            self.APN_D_ID,
            ['read', 'write', 'notify'],
            characteristic)

    def ReadValue(self, options):
        return [
            dbus.Byte('T'), dbus.Byte('e'), dbus.Byte('s'), dbus.Byte('t')
        ]
