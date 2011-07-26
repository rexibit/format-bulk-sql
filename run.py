#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#		run.py
#		Function: Enable command line access to the FormatBulkSQL class
#		Github Repository URL: https://github.com/rexibit/format-bulk-sql
#
#	   Copyright 2011 Matthew Watts <matthew@rexibit.com>
#
#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU General Public License as published by
#	   the Free Software Foundation; either version 2 of the License, or
#	   (at your option) any later version.
#
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU General Public License for more details.
#
#	   You should have received a copy of the GNU General Public License
#	   along with this program; if not, write to the Free Software
#	   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#	   MA 02110-1301, USA.
#
#

from optparse import OptionParser
from format_bulk_sql import FormatBulkSQL

def main():
	parser = OptionParser(usage = "usage: %prog [options] table_name fields_list_file_name",
						  version = "%prog 1.0")
	parser.add_option('-t', '--template',
						dest = 'template_name',
						default = 'trim', type = 'string',
						help = "Choose which SQL template to use.")
	parser.add_option('-s', '--search',
						dest = 'search_string',
						type = 'string',
						help = "List the string to search for in the query.")
	parser.add_option('-r', '--replace',
						dest = 'replace_string',
						type = 'string',
						help = "List the string to replace the searched text with in the query.")
	parser.add_option('-o', '--output',
						dest = 'sql_file_path',
						default = None, type = 'string',
						help = "List the path to the file where the SQL query will be saved.")
	(options, args) = parser.parse_args()

	if (len(args) != 2):
		parser.error("Wrong number of arguments. Include the table name and path to the fields list file.")

	if(options.template_name != None and options.sql_file_path != None):
		# Setup the variables to be used for the SQL
		table_name = args[0]
		template_name = options.template_name
		fields_list_file = open(args[1], "r")
		field_names = []
		sql_file = open(options.sql_file_path, "w")
		format_sql = FormatBulkSQL()

		# Populate the field_names list
		for line in fields_list_file:
			if len(line.strip()) > 0:
				field_names.append(line.strip())

		fields_list_file.close()

		# Check if there is a search & replace option set
		if (options.search_string != None and options.replace_string != None):
			search_replace_list = [options.search_string, options.replace_string]

			sql_file.write(format_sql.update_all_fields(table_name, field_names, template_name, search_replace_list))
		else:
			sql_file.write(format_sql.update_all_fields(table_name, field_names, template_name, None))

		sql_file.close()

	else:
		raise Exception('Make sure you include the correct options.')

if __name__ == '__main__':
	main()