#!/usr/bin/env python3
# SPDX-License-Identifier: LGPL-2.1-or-later

import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service

import array
from audio import AudioService
from cellular import CellularService
from device_info import DeviceInformation
from identity import Identity
from power import PowerService

from utils import Advertisement, Characteristic, Descriptor, Service
from wifi import WifiService
try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject
import sys
import os

from random import randint


OWNER_ADDRESS = os.environ("OWNER_ADDRESS")

IS_PAIRED = False
if(OWNER_ADDRESS and len(OWNER_ADDRESS)):
    IS_PAIRED = True


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


class InvalidArgsException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.freedesktop.DBus.Error.InvalidArgs'


class NotSupportedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.NotSupported'


class NotPermittedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.NotPermitted'


class InvalidValueLengthException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.InvalidValueLength'


class FailedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.Failed'


class AutoPIBLEApplication(dbus.service.Object):
    """
    org.bluez.GattApplication1 interface implementation
    """

    def __init__(self, bus):
        self.path = '/'
        self.services = []
        dbus.service.Object.__init__(self, bus, self.path)
        self.add_service(CellularService(bus, 0))
        self.add_service(DeviceInformation(bus, 1))
        self.add_service(Identity(bus, 2))
        self.add_service(PowerService(bus, 3))
        self.add_service(WifiService(bus, 4))
        self.add_service(AudioService(bus, 5))
        if(IS_PAIRED):
            # Add any services that are only accessible after the autopi has been paired.
            pass

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_service(self, service):
        self.services.append(service)

    @dbus.service.method(DBUS_OM_IFACE, out_signature='a{oa{sa{sv}}}')
    def GetManagedObjects(self):
        response = {}
        print('GetManagedObjects')

        for service in self.services:
            response[service.get_path()] = service.get_properties()
            chrcs = service.get_characteristics()
            for chrc in chrcs:
                response[chrc.get_path()] = chrc.get_properties()
                descs = chrc.get_descriptors()
                for desc in descs:
                    response[desc.get_path()] = desc.get_properties()

        return response


def register_app_cb():
    print('GATT application registered')


def register_app_error_cb(error):
    print('Failed to register application: ' + str(error))
    mainloop.quit()


def find_adapter(bus):
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
                               DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()

    for o, props in objects.items():
        if GATT_MANAGER_IFACE in props.keys():
            return o

    return None


class AutoPIAdvertisement(Advertisement):
    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index, 'peripheral')
        self.add_service_uuid(CellularService.CELLULAR_SVC_UUID)
        self.add_service_uuid(DeviceInformation.DI_UUID)
        self.add_service_uuid(Identity.IDENTITY_SVC_UUID)
        self.add_service_uuid(PowerService.POWER_SVC_UUID)
        if(IS_PAIRED):
            self.add_service_uuid(WifiService.WIFI_SVC_UUID)
            self.add_solicit_uuid(AudioService.AUDIO_SVC_UUID)
        # self.add_service_uuid("180D")
        # self.add_service_uuid("180F")
        # self.add_manufacturer_data(0xffff, [0x00, 0x01, 0x02, 0x03])
        # self.add_service_data('9999', [0x00, 0x01, 0x02, 0x03, 0x04])
        self.add_local_name('AutoPI')
        self.include_tx_power = True
        # self.add_data(0x26, [0x01, 0x01, 0x00])


def register_ad_cb():
    print('Advertisement registered')


def register_ad_error_cb(error):
    print('Failed to register advertisement: ' + str(error))
    mainloop.quit()


def main():
    global mainloop

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    adapter = find_adapter(bus)
    if not adapter:
        print('GattManager1 interface not found')
        return

    service_manager = dbus.Interface(
        bus.get_object(BLUEZ_SERVICE_NAME, adapter),
        GATT_MANAGER_IFACE)

    app = AutoPIBLEApplication(bus)

    mainloop = GObject.MainLoop()

    print('Registering GATT application...')
    service_manager.RegisterApplication(app.get_path(), {},
                                        reply_handler=register_app_cb,
                                        error_handler=register_app_error_cb)

    print("Registering advertisements")
    ad_manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                                LE_ADVERTISING_MANAGER_IFACE)

    test_advertisement = AutoPIAdvertisement(bus, 0)

    ad_manager.RegisterAdvertisement(test_advertisement.get_path(), {},
                                     reply_handler=register_ad_cb,
                                     error_handler=register_ad_error_cb)

    mainloop.run()


if __name__ == '__main__':
    main()
