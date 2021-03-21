#!/usr/bin/python3
"""
Part Manager - assistent for querying, importing and updating
"""
import argparse
import sqlite3
from pm_general import ComponentType, PackageType, MountType
from pm_setup_db import TABLE_COMPONENT_TYPE, TABLE_PACKAGE_TYPE, TABLE_MOUNT_TYPE, TABLE_PARTS
from pm_setup_db import DB_NAME, create_connection

def get_type_id(c, component_type):
    c.execute(f"SELECT type_id FROM {TABLE_COMPONENT_TYPE} WHERE type_name='{component_type}';")
    rows = c.fetchall()
    if len(rows) != 1:
        raise Exception(f"Invalid component type {component_type}")
    return rows[0][0]

def get_pack_id(c, pack_type):
    c.execute(f"SELECT pack_id FROM {TABLE_PACKAGE_TYPE} WHERE pack_name='{pack_type}';")
    rows = c.fetchall()
    if len(rows) != 1:
        raise Exception(f"Invalid package type {pack_type}")
    return rows[0][0]

def get_mount_id(c, mount_type):
    r = c.execute(f"SELECT mount_id FROM {TABLE_MOUNT_TYPE} WHERE mount_type='{mount_type}';")
    rows = c.fetchall()
    if len(rows) != 1:
        raise Exception(f"Invalid mount type {mount_type}")
    return rows[0][0]

def add_part(
        conn,
        component_type: ComponentType,
        pack_type: PackageType,
        mount_type: MountType,
        value: str,
        qty: int,
        part_nr: str,
        description: str):
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")
    tid = get_type_id(c, component_type)
    pid = get_pack_id(c, pack_type)
    mid = get_mount_id(c, mount_type)
    part = (None, tid, pid, mid, value, qty, part_nr, description)
    c.execute(f"INSERT INTO {TABLE_PARTS} VALUES (?,?,?,?,?,?,?,?);", part)
    conn.commit()

def get_part(conn, component_type=None, pack_type=None, mount_type=None):
    c = conn.cursor()
    where = "WHERE"
    query = f"""
        SELECT type_name, pack_name, mount_type, value, qty, part_nr, description
        FROM {TABLE_PARTS} as a INNER JOIN {TABLE_COMPONENT_TYPE} as b ON a.type_id=b.type_id
                                INNER JOIN {TABLE_PACKAGE_TYPE} as c ON a.pack_id=c.pack_id
                                INNER JOIN {TABLE_MOUNT_TYPE} as d ON a.mount_id=d.mount_id
        """
    if component_type:
        query += f" {where} type_name='{component_type}'"
        where = "AND"
    if pack_type:
        query += f" {where} pack_name='{pack_type}'"
        where = "AND"
    if mount_type:
        query += f" {where} mount_type='{mount_type}'"
        where = "AND"
    query += ";"

    c.execute(query)
    rows = c.fetchall()
    for row in rows:
        print(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='Action to perform: query, update or add')
    parser.add_argument('-c', '--component', help='The component type')
    parser.add_argument('-p', '--package', help='The package type')
    args = parser.parse_args()

    conn = create_connection(DB_NAME)
    if args.action == "query":
        get_part(conn, component_type=args.component, pack_type=args.package)
    else:
        print("Not supported yet")

