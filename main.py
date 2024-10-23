#!/usr/bin/env python

from query_select import SelectQuery
from util import read_query
import misconceptions_check
from query_create import *


t1 = Table('table1')
t2 = Table('table2')

c = TableColumn('column1', int, is_primary_key=True)
t1.add_column(c)
t1.add_column(TableColumn('column2', str))

t2.add_column(TableColumn('column1', int, is_primary_key=True))
t2.add_column(TableColumn('column2', str, is_primary_key=True, foreign_key_column=c))
t2.add_column(TableColumn('column3', int))

tables = [t1, t2]



if __name__ == '__main__':
    from dav_tools import argument_parser, messages
    
    argument_parser.add_argument('file', help='File containing the SELECT query')
    argument_parser.add_argument('table', help='File containing the CREATE TABLE query', nargs='?')
    argument_parser.add_verbose_mode()

    argument_parser.set_developer_info('Davide Ponzini', 'davide.ponzini@edu.unige.it')

    text = read_query(argument_parser.args.file)
    query = SelectQuery(text)

    messages.info(argument_parser.args.file)

    if argument_parser.args.verbose:
        messages.info('============= SELECT =============')
        sel = query.extract_select()
        print(repr(sel))
        messages.message(sel.distinct, icon='DISTINCT', icon_options=[messages.TextFormat.Color.BLUE])
        for identifier in sel.identifiers:
            messages.message(f'{str(identifier).ljust(30)} {repr(identifier).ljust(50)} {identifier.get_parent_name()}.{identifier.get_real_name()} -> {identifier.get_parent_name()}.{identifier.get_name()}', icon='column', icon_options=[messages.TextFormat.Color.GREEN])

        messages.info('============= FROM =============')
        fr = query.extract_from()
        print(repr(fr))
        for identifier in fr.identifiers:
            messages.message(f'{identifier.get_real_name()} -> {identifier.get_name()}', icon='table', icon_options=[messages.TextFormat.Color.GREEN])

        messages.info('============= WHERE =============')
        wh = query.extract_where()
        print(repr(wh))

        messages.info('============= GROUP BY =============')
        gb = query.extract_group_by()
        print(repr(gb))

        messages.info('============= HAVING =============')
        hav = query.extract_having()
        print(repr(hav))

        messages.info('============= ORDER BY =============')
        ob = query.extract_order_by()
        print(repr(ob))

        messages.info('============= MISCONCEPTIONS =============')

    misconceptions_check.syn_6_common_syntax_error_using_where_twice(query)
    misconceptions_check.syn_6_common_syntax_error_additional_semicolon(query)
