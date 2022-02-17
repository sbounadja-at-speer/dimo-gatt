
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


class AudioService(Service):
    """
    Audio service

    """
    AUDIO_SVC_UUID = '181A'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.AUDIO_SVC_UUID, True)
        self.add_characteristic(Speak(bus, 0, self))


class Speak(Characteristic):
    """


    """
    SPEAK_ID = '75e2ce6f-df8b-4935-8cc3-dd0c03b53cd6'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.SPEAK_ID,
            ['write'],
            service)
        self.value = []
        self.add_descriptor(SpeakDescriptor(bus, 0, self))

    def WriteValue(self, value, options):
        print('Speak Write: ' + repr(value))
        self.value = value
        # Run logic to speak w/e is sent


class SpeakDescriptor(Descriptor):
    """

    """
    SPEAK_D_ID = 'a6d2b08f-e05c-44ef-88fb-f118f1a0d01f'

    def __init__(self, bus, index, characteristic):
        Descriptor.__init__(
            self, bus, index,
            self.SPEAK_D_ID,
            ['write'],
            characteristic)

    def ReadValue(self, options):
        return [
            dbus.Byte('T'), dbus.Byte('e'), dbus.Byte('s'), dbus.Byte('t')
        ]
