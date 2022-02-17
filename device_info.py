

from utils import Characteristic, FailedException, InvalidValueLengthException, Service

#!/usr/bin/env python3
# SPDX-License-Identifier: LGPL-2.1-or-later

import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service

import array

from utils import Advertisement, Characteristic, Descriptor, Service
try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject
import sys

from random import randint

mainloop = None

BLUEZ_SERVICE_NAME = 'org.bluez'
GATT_MANAGER_IFACE = 'org.bluez.GattManager1'
DBUS_OM_IFACE = 'org.freedesktop.DBus.ObjectManager'
DBUS_PROP_IFACE = 'org.freedesktop.DBus.Properties'
LE_ADVERTISING_MANAGER_IFACE = 'org.bluez.LEAdvertisingManager1'
LE_ADVERTISEMENT_IFACE = 'org.bluez.LEAdvertisement1'
GATT_SERVICE_IFACE = 'org.bluez.GattService1'
GATT_CHRC_IFACE = 'org.bluez.GattCharacteristic1'
GATT_DESC_IFACE = 'org.bluez.GattDescriptor1'


class DeviceInformation(Service):
    """
    Device information service

    """
    DI_UUID = '180A'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.DI_UUID, True)
        self.add_characteristic(ManufacturerName(bus, 0, self))
        self.add_characteristic(BoardID(bus, 1, self))
        self.add_characteristic(UnitID(bus, 2, self))
        self.add_characteristic(HardwareRevision(bus, 3, self))
        self.add_characteristic(IMEI(bus, 4, self))


class ManufacturerName(Characteristic):
    MNFR_C_ID = 'a9ea55f7-df03-4e30-82b9-9c5d59310bbc'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.MNFR_C_ID,
            ['read'],
            service)

    def ReadValue(self, options):
        return "AutoPI"


class BoardID(Characteristic):
    BID_C_ID = '8f931594-b974-42db-bfe4-0dd2f2c398af'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.BID_C_ID,
            ['read'],
            service)

    def ReadValue(self, options):
        return "14341231212"


class UnitID(Characteristic):
    UID_C_ID = 'f73a109a-7494-44af-af7b-77c118828b20'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.UID_C_ID,
            ['read'],
            service)

    def ReadValue(self, options):
        return "c4104189-af1a-4a03-a856-8f650ff705a2"


class HardwareRevision(Characteristic):
    HWR_C_ID = '6fb1b29a-58d6-46ef-a3ef-3ad8c40d34d4'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.HWR_C_ID,
            ['read'],
            service)

    def ReadValue(self, options):
        return "AP01005"


class HardwareRevision(Characteristic):
    SWR_C_ID = '4a7bd9af-08a0-4516-b731-b5545fce31e2'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.SWR_C_ID,
            ['read'],
            service)

    def ReadValue(self, options):
        return "v0.123"


class IMEI(Characteristic):
    IMEI_C_ID = '56f71368-14d9-44b6-8431-b2c957dfe156'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.IMEI_C_ID,
            ['read'],
            service)

    def ReadValue(self, options):
        return "42347238947234123123"
