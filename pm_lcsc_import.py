"""
Part Manager - import LCSC BOM file
"""
import argparse
import csv
import sqlite3
import pm_assistent
from enum import Enum
from pathlib import Path
from pm_general import ComponentType, PackageType, MountType
from pm_setup_db import DB_NAME, create_connection

def get_type(descr) -> ComponentType:
    ldescr = descr.lower()
    if 'resistor' in ldescr:
        return ComponentType.RES
    elif 'capacitor' in ldescr and 'ceramic' in ldescr:
        return ComponentType.CAP_CER
    elif 'inductor' in ldescr:
        return ComponentType.IND
    elif 'led' in ldescr:
        return ComponentType.LED
    elif 'diode' in ldescr:
        return ComponentType.DIODE
    elif 'crystal' in ldescr:
        return ComponentType.XTAL
    elif 'usb' in ldescr:
        return ComponentType.CON_USB
    return ComponentType.UNKNOWN

def get_package(pkg) -> PackageType:
    p = pkg.lstrip('SMD-')
    p = p.replace('-', '_')
    for pt in PackageType:
        if str(pt) == p or str(pt) == ('0'+p):
            return pt
    if 'SOD-123' in pkg:
        return PackageType.PSOD_123
    return PackageType.PUnknown

class LCSC_entry:
    def __init__(self, raw_entry):
        # TODO: make this more flexible than hard coding columns
        self.raw = ','.join(raw_entry)
        self.mf_part_nr = raw_entry[1]
        self.package = get_package(raw_entry[4])
        self.description = raw_entry[5]
        self.order_qty = raw_entry[7]
        self.type = get_type(self.description)

    @property
    def value(self):
        if (self.type is ComponentType.RES or
            self.type is ComponentType.CAP_CER or
            self.type is ComponentType.IND or
            self.type is ComponentType.XTAL):
            return self.description.split()[0]
        return None

class LCSC_file:
    def __init__(self, csv_file):
        rdr = csv.reader(csv_file)
        self.header = [i.strip().lower() for i in next(rdr)]
        self.content = [l for l in rdr]
        self.idx = 0

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        if self.idx < len(self.content):
            result = LCSC_entry(self.content[self.idx])
            self.idx += 1
            return result
        else:
            raise StopIteration


def main(csv_file):
    conn = create_connection(DB_NAME)
    lcsc = LCSC_file(csv_file)
    manual_entries = []
    for e in lcsc:
        if e.type is not ComponentType.UNKNOWN:
            print(f"{e.order_qty} {e.type} {e.package} {e.value}")
            pm_assistent.add_part(conn, e.type, e.package, MountType.SMT,
                    e.value, e.order_qty, e.mf_part_nr, e.description)
        else:
            manual_entries.append(e)
    print("\nThese entries have to be imported manually")
    for e in manual_entries:
        print(e.raw)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('BOM', help='CSV file exported from LCSC order')
    args = parser.parse_args()
    csv_f = Path(args.BOM)
    if csv_f.is_file():
        with csv_f.open() as f:
            main(f)
    else:
        print(f"error: {args.BOM} is not a file")
