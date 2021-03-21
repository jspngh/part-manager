"""
Part Manager - general definitions
"""
from enum import Enum, auto

class ComponentType(Enum):
    RES = auto()
    CAP_CER = auto()
    IND = auto()
    SW_TAC = auto()
    MCU = auto()
    XTAL = auto()
    DIODE = auto()
    LED = auto()
    FUSE = auto()
    CON_USB = auto()
    UNKNOWN = auto()

    def __str__(self):
        if self is ComponentType.RES:
            return "Resistor"
        if self is ComponentType.CAP_CER:
            return "Capacitor Ceramic"
        if self is ComponentType.IND:
            return "Inductor"
        if self is ComponentType.SW_TAC:
            return "Switch Tactile"
        if self is ComponentType.MCU:
            return "MCU"
        if self is ComponentType.XTAL:
            return "XTAL"
        if self is ComponentType.DIODE:
            return "Diode"
        if self is ComponentType.LED:
            return "LED"
        if self is ComponentType.FUSE:
            return "Fuse"
        if self is ComponentType.CON_USB:
            return "Connector USB"
        return "Unknown"

class PackageType(Enum):
    P1206 = auto()
    P0805 = auto()
    P0603 = auto()
    P0402 = auto()
    P0603_x4 = auto()
    P0402_x4 = auto()
    P3225_4P = auto()
    P2012_2P = auto()
    PSOD_123 = auto()
    PUnknown = auto()

    def __str__(self):
        return self.name[1:]


class MountType(Enum):
    SMT = auto()
    THT = auto()

    def __str__(self):
        return self.name

