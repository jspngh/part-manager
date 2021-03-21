"""
Part Manager - setup sqlite3 database
"""
import sqlite3
from pm_general import *

DB_NAME = "inventory.db"

TABLE_COMPONENT_TYPE = "TYPES"
TABLE_PACKAGE_TYPE= "PACKAGE"
TABLE_MOUNT_TYPE = "MOUNT"
TABLE_PARTS = "PARTS"

def create_connection(db_path):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
    except Error as e:
        print(e)

    return conn

def create_tables(conn):
    table_types = f"""CREATE TABLE {TABLE_COMPONENT_TYPE}(
                        type_id INTEGER NOT NULL PRIMARY KEY,
                        type_name text NOT NULL
                      ); """
    table_packs = f"""CREATE TABLE {TABLE_PACKAGE_TYPE}(
                        pack_id INTEGER NOT NULL PRIMARY KEY,
                        pack_name text NOT NULL,
                        pack_info text
                      ); """
    table_mount = f"""CREATE TABLE {TABLE_MOUNT_TYPE}(
                        mount_id INTEGER NOT NULL PRIMARY KEY,
                        mount_type text NOT NULL
                      ); """
    table_parts = f"""CREATE TABLE {TABLE_PARTS}(
                        part_id INTEGER NOT NULL PRIMARY KEY,
                        type_id INTEGER NOT NULL,
                        pack_id INTEGER NOT NULL,
                        mount_id INTEGER NOT NULL,
                        value CHAR(20),
                        qty INTEGER,
                        part_nr TEXT,
                        description TEXT,
                        FOREIGN KEY (type_id) REFERENCES TYPES(type_id),
                        FOREIGN KEY (pack_id) REFERENCES PACKAGE(pack_id)
                        FOREIGN KEY (mount_id) REFERENCES MOUNT(mount_id)
                      ); """
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")
    c.execute(table_types)
    c.execute(table_packs)
    c.execute(table_mount)
    c.execute(table_parts)

def initial_fill(conn):
    insert_type = f"INSERT INTO {TABLE_COMPONENT_TYPE} (type_name) VALUES (?);"
    insert_pack = f"INSERT INTO {TABLE_PACKAGE_TYPE} (pack_name) VALUES (?);"
    insert_mount = f"INSERT INTO {TABLE_MOUNT_TYPE} (mount_type) VALUES (?);"

    c = conn.cursor()
    for t in ComponentType:
        c.execute(insert_type, (str(t),))
    for p in PackageType:
        c.execute(insert_pack, (str(p),))
    for m in MountType:
        c.execute(insert_mount, (str(m),))

if __name__ == "__main__":
    conn = create_connection(DB_NAME)
    create_tables(conn)
    initial_fill(conn)
    conn.commit()
