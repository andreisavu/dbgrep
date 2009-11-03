#! /usr/bin/env python
"""
Convert a simple csv file to an sqlite database table
"""

import sqlite3
import logging
import csv

from optparse import OptionParser

def main():
    opt, args = parse_args()

    if None not in (opt.db, opt.file, opt.table, opt.cols):
        create_db(opt.db, opt.file, opt.table, opt.cols)


def create_db(db_file, csv_file, table, columns):
    columns = filter(None, [el.strip() for el in columns.split(',')])
    logging.info("Table columns: %s" % str(columns))

    db = init_db(db_file, table, columns)
    reader = csv.reader(open(csv_file))
    for row in reader:
        if len(row) != len(columns):
            logging.error('Size mismatch. Skip row: %s' % str(row))
            continue;
        write_row(db, table, columns, row)
    db.close()


def init_db(db_file, table, columns):
    db = sqlite3.connect(db_file)
    db_cols = ["%s text" % el for el in columns]
    db.execute("create table if not exists %s (%s)" % (table, ",".join(db_cols)))
    db.commit()
    return db


def write_row(db, table, columns, row):
    query = "insert into %s(%s)values(%s)" % (table, ",".join(columns), ",".join(['?']*len(row)))
    db.execute(query, row)
    db.commit()


def parse_args():
    parser = OptionParser()

    parser.add_option('-d', '--db', dest='db',
        help='output DATABASE file', metavar='DATABASE')

    parser.add_option('-f', '--file', dest='file',
        help='input FILE', metavar='FILE')

    parser.add_option('-c', '--columns', dest='cols',
        help='table COLUMNS - csv', metavar='COLUMNS')

    parser.add_option('-t', '--table', dest='table',
        help='destination TABLE', metavar='TABLE')
    
    return parser.parse_args()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()

