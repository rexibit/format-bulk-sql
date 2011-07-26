#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       format-bulk-sql.py
#		Function: Form SQL query strings for commonly needed queries
#					to save time from doing by hand and in bulk.
#
#       Copyright 2011 Matthew Watts <matthew@rexibit.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#
#

from string import Template

class FormatBulkSQL:
	# Update each column in a table using the desired template
	def update_all_fields(self, table_name, field_names, template_name, search_replace_list):
		if(isinstance(table_name, basestring) and
			isinstance(field_names, (list, tuple)) and
			isinstance(template_name, basestring)):

			template = self.get_query_template(template_name)
			query = Template(template[0]).substitute(table_name=table_name)

			for field in field_names:
				if (field != field_names[-1]):
					if (isinstance(search_replace_list, (list, tuple))):
						query += Template(template[1]).substitute(field_name=field, search_string=search_replace_list[0], replace_string=search_replace_list[1]) + ', '
					else:
						query += Template(template[1]).substitute(field_name=field) + ', '
				else:
					if (isinstance(search_replace_list, (list, tuple))):
						query += Template(template[1]).substitute(field_name=field, search_string=search_replace_list[0], replace_string=search_replace_list[1])
					else:
						query += Template(template[1]).substitute(field_name=field)
			
			# Check if there is need for a WHERE clause
			if (template[2] != 'none'):
				query += ' WHERE '

				for field in field_names:
					if (field != field_names[-1]):
						query += Template(template[2]).substitute(field_name=field,
									replace_string=search_replace_list[1], search_string=search_replace_list[0]) + ' OR '
					else:
						query += Template(template[2]).substitute(field_name=field, replace_string=search_replace_list[1], search_string=search_replace_list[0]) + ';'

						return query
			else:
				query += ';'

				return query

		else:
			raise Exception("TypeError: Check parameter types.")
	
	# Define the templates to be used to form the SQL query
	def get_query_template(self, template_name):
		template_types = {
							'search_replace': ['UPDATE ${table_name} SET ', "`${field_name}` = COALESCE(NULLIF(`${field_name}`, '${search_string}'), '${replace_string}')", 'none'],
							'search_replace_in': ['UPDATE ${table_name} SET ', "`${field_name}` = replace(`${field_name}`, '${search_string}', '${replace_string}')", 'none'],
							'trim': ['UPDATE ${table_name} SET ', '`${field_name}` = LTRIM(RTRIM(`${field_name}`))', 'none']
						}
		
		return template_types[template_name]