
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
import os


OWNER_ADDRESS = os.environ("OWNER_ADDRESS")

IS_PAIRED = False
if(OWNER_ADDRESS and len(OWNER_ADDRESS)):
    IS_PAIRED = True


class Identity(Service):
    """
    Dummy Cellular service that provides characteristics and descriptors that
    exercise various API functionality.

    """
    IDENTITY_SVC_UUID = '180C'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.IDENTITY_SVC_UUID, True)
        self.add_characteristic(PublicKey(bus, 0, self))
        self.add_characteristic(SignedNonce(bus, 1, self))
        # if(IS_PAIRED):
        #     self.add_characteristic(SignMessage(bus, 2, self))


class PublicKey(Characteristic):
    """
    Dummy test characteristic. Allows writing arbitrary bytes to its value, and
    contains "extended properties", as well as a test descriptor.

    """
    PK_UUID = '12345678-1234-5678-1234-56789abcdef1'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.PK_UUID,
            ['read'],
            service)
        self.value = []
        self.add_descriptor(PublicKeyDescriptor(bus, 0, self))

    def ReadValue(self, options):
        # Fetch autopi public key and return it
        print('PublicKey Read: ' + repr(self.value))
        return self.value


class PublicKeyDescriptor(Descriptor):
    """
    Dummy test descriptor. Returns a static value.

    """
    PK_D_UUID = '12345678-1234-5678-1234-56789abcdef2'

    def __init__(self, bus, index, characteristic):
        Descriptor.__init__(
            self, bus, index,
            self.PK_D_UUID,
            ['read'],
            characteristic)

    def ReadValue(self, options):
        return [
            dbus.Byte('T'), dbus.Byte('e'), dbus.Byte('s'), dbus.Byte('t')
        ]


class SignedNonce(Characteristic):
    """
    SignMessage Characteristic

    """
    NONCE_UUID = '12345678-1234-5678-1234-56789abcdef2'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.NONCE_UUID,
            ['read'],
            service)
        self.value = []
        self.add_descriptor(SignedNonceDescriptor(bus, 0, self))

    def ReadValue(self, options):
        # Sign token of pre-defined format and return it
        return "Signed nonce: "


class SignedNonceDescriptor(Descriptor):
    """
    Descriptor for signed nonce characteristic/

    """
    NONCE_D_UUID = '12345678-1234-5678-1234-56989abcdef2'

    def __init__(self, bus, index, characteristic):
        Descriptor.__init__(
            self, bus, index,
            self.NONCE_D_UUID,
            ['read'],
            characteristic)

    def ReadValue(self, options):
        return [
            dbus.Byte('T'), dbus.Byte('e'), dbus.Byte('s'), dbus.Byte('t')
        ]


# Need to discuss how to make this characteristic secure.
# Leaving out for now.
class SignMessage(Characteristic):
    """
    SignMessage Characteristic

    """
    SIGN_UUID = '12345678-1234-5678-1234-56789abcdef2'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.SIGN_UUID,
            ['write'],
            service)
        self.value = []
        self.add_descriptor(SignMessageDescriptor(bus, 0, self))

    def WriteValue(self, value, options):
        print('SignMessage Write: ' + repr(value))
        self.value = value
        # Sign message and return it

        if not IS_PAIRED:
            # Start polling AutoPI pairing service
            pass

        return "Signed message: "


class SignMessageDescriptor(Descriptor):
    """
    Dummy test descriptor. Returns a static value.

    """
    SIGN_D_UUID = '12345678-1234-5678-1234-56989abcdef2'

    def __init__(self, bus, index, characteristic):
        Descriptor.__init__(
            self, bus, index,
            self.SIGN_D_UUID,
            ['write'],
            characteristic)

    def ReadValue(self, options):
        return [
            dbus.Byte('T'), dbus.Byte('e'), dbus.Byte('s'), dbus.Byte('t')
        ]
