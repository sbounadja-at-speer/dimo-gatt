
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


class WifiService(Service):
    """
    Dummy Cellular service that provides characteristics and descriptors that
    exercise various API functionality.

    """
    WIFI_SVC_UUID = '180F'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.WIFI_SVC_UUID, True)
        self.add_characteristic(SSID(bus, 0, self))
        self.add_characteristic(SSH(bus, 1, self))


class SSID(Characteristic):
    """


    """
    SSID_ID = '90247c03-f659-4854-9062-127b2070998d'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.SSID_ID,
            ['read', 'write'],
            service)
        self.value = []
        self.add_descriptor(SSIDDescriptor(bus, 0, self))

    def ReadValue(self, options):
        return "Network name"

    def WriteValue(self, value, options):
        print('SSID Write: ' + repr(value))
        self.value = value
        # Run logic to change the wifi settings


class SSIDDescriptor(Descriptor):
    """

    """
    SSID_D_ID = '0eb15ad2-4eaa-4da4-ac91-f4c9c862a013'

    def __init__(self, bus, index, characteristic):
        Descriptor.__init__(
            self, bus, index,
            self.SSID_D_ID,
            ['read', 'write'],
            characteristic)

    def ReadValue(self, options):
        return [
            dbus.Byte('T'), dbus.Byte('e'), dbus.Byte('s'), dbus.Byte('t')
        ]


class SSH(Characteristic):
    """


    """
    SSH_ID = '79c4e837-fbce-4ab9-9d94-24508c488b97'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.SSH_ID,
            ['read', 'write'],
            service)
        self.value = []
        self.add_descriptor(SSHDescriptor(bus, 0, self))

    def ReadValue(self, options):
        return "0"

    def WriteValue(self, value, options):
        print('SSH Write: ' + repr(value))
        self.value = value
        # Run logic to change the SSH settings


class SSHDescriptor(Descriptor):
    """

    """
    SSH_D_ID = 'cef04287-0635-4343-8026-0fd22755c2d1'

    def __init__(self, bus, index, characteristic):
        Descriptor.__init__(
            self, bus, index,
            self.SSID_D_ID,
            ['read', 'write'],
            characteristic)

    def ReadValue(self, options):
        return [
            dbus.Byte('T'), dbus.Byte('e'), dbus.Byte('s'), dbus.Byte('t')
        ]
