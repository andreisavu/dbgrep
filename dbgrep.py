#! /usr/bin/env python
"""
Multicolumn & multitable database grep utility
"""

__author__ = 'Andrei Savu <contact@andreisavu.ro>'

import sys
import csv

from optparse import OptionParser
from sqlalchemy import *
from itertools import izip

from dbgrep.rexp import any_match

def main():
    opt, args = parse_args()
    wr = csv.writer(sys.stdout)    

    if None not in [opt.dsn, opt.exp, opt.tables]:
        for result in do_search(opt.dsn, opt.tables, opt.exp):
            wr.writerow(result)

def do_search(dsn, tables, expressions):
    """
    Do a regexp search over the entire database
    """
    engine = create_engine(dsn)

    meta = MetaData(engine)
    meta.reflect()

    for t in meta.sorted_tables:
        if any_match(tables, t.name):
            for r in search_table(t, expressions):
                yield r

def search_table(t, exp):
    """
    Full search on the table. Yield table_name, column, value
    """
    for row in t.select().execute():
        for k, v in dict(row).items():
            if any_match(exp, v):
                yield t.name, k, v
        

def parse_args():
    """
    Parse command-line arguments
    """
    parser = OptionParser()

    parser.add_option('-d', '--dsn', dest='dsn', 
        help='data source URL', metavar='URL')

    parser.add_option('-e', '--exp', dest='exp',
        action="append", help='search regular EXPRESSION', metavar='EXPRESSION')

    parser.add_option('-t', '--table' , dest='tables',
        action='append', help='regexp for TABLE selection', metavar='TABLE')

    return parser.parse_args()

if __name__ == '__main__':
    main()
