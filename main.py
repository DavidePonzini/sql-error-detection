#!/usr/bin/env python

import query
import util
import misconceptions_check


# debugging
script_select = util.read_file('test.sql')
script_create = util.read_file('test_create.sql')
q = query.SelectQuery(script_select, script_create)


if __name__ == '__main__':
    from dav_tools import argument_parser, messages
    
    argument_parser.add_argument('file', help='File containing the SELECT query')
    argument_parser.add_argument('table', help='File containing the CREATE TABLE query')
    argument_parser.add_verbose_mode()

    argument_parser.set_developer_info('Davide Ponzini', 'davide.ponzini@edu.unige.it')

    script_select = util.read_file(argument_parser.args.file)
    script_create = util.read_file(argument_parser.args.table)
    q = query.SelectQuery(script_select, script_create)

    if argument_parser.args.verbose:
        messages.info('============= SCHEMA =============')
        print(repr(q.available_tables))

        messages.info('============= SELECT =============')
        sel = q.extract_select()
        print(repr(sel))
        messages.message(sel.distinct, icon='DISTINCT', icon_options=[messages.TextFormat.Color.BLUE])
        for identifier in sel.identifiers:
            messages.message(f'{str(identifier).ljust(30)} {repr(identifier).ljust(50)} {identifier.get_parent_name()}.{identifier.get_real_name()} -> {identifier.get_parent_name()}.{identifier.get_name()}', icon='column', icon_options=[messages.TextFormat.Color.GREEN])

        messages.info('============= FROM =============')
        fr = q.extract_from()
        print(repr(fr))
        for identifier in fr.identifiers:
            messages.message(f'{identifier.get_real_name()} -> {identifier.get_name()}', icon='table', icon_options=[messages.TextFormat.Color.GREEN])

        messages.info('============= WHERE =============')
        wh = q.extract_where()
        print(repr(wh))

        messages.info('============= GROUP BY =============')
        gb = q.extract_group_by()
        print(repr(gb))

        messages.info('============= HAVING =============')
        hav = q.extract_having()
        print(repr(hav))

        messages.info('============= ORDER BY =============')
        ob = q.extract_order_by()
        print(repr(ob))

        messages.info('============= MISCONCEPTIONS =============')

    misconceptions_check.syn_6_common_syntax_error_using_where_twice(q)
    misconceptions_check.syn_6_common_syntax_error_additional_semicolon(q)
