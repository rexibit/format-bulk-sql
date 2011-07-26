**About**

This project came about as a need of constantly having to clean up many messy database tables when designing websites for clients. Following the, "If you have to do it by hand twice, then you need to automate it" philosophy, here we are after consolidating and cleaning scripts into a single class and run script.

Currently, there are only a few update templates, but I'll be adding more in the future; or someone can add their own templates and expand the methods.

FormatBulkSQL is developed using Python 2.7 and hasn't been tested in prior versions.

Github Repository URL: https://github.com/rexibit/format-bulk-sql

**Usage**

The FormatBulkSQL class currently has the following methods:
- ``update_all_fields`` , outputs a formatted UPDATE SQL query using the table name, list of field names, and optional search and replace values for the specified template name.

	::
		format_sql = FormatBulkSQL()
		
		# Setup the variables to pass to the object
		table_name = 'test_table_name'
		field_name_list = ['test_field_1', 'test_field_2']
		template_name = 'trim'

		# Pass the parameters and print the returned result
		# None will be used in place of the search_replace list parameter since it's not needed
		print format_sql(table_name, field_name_list, template_name, None)

- ``get_query_template`` , returns a list for the parts of the requested template name.

	::
		Currently used templates:
		search_replace - checks each field's value against the search phrase and replaces it if true.
		search_replace_in - searches inside each field for the matching search phrase and replaces it.
		trim - trims white space at the beginning and end of each field.

		Note:
		Each template list contains three parts: beginning of the query, each field part, where clause.

		If the template doesn't have need for a where clause, put 'none' so it won't be added to the query.

**Command Line Run Script**

Use run.py to quickly access the templates to copy-paste the SQL into phpMyAdmin or related SQL management area.

List of Options:

	::
		-t, --template : List the template's name to be used.

		-s, --search : Enter the search string to be used.

		-r, --replace : Enter the replace string to be used.

		-o, --output : List the path to the file where the SQL will be saved.

Examples:

- Trim whitespace from each field:
	::
		$ python run.py -t trim -o "/path/to/file/output-sql-query.txt" table_name "/path/to/file/field-names.txt"

- Search each field for "Array" and replace it with an empty string:
	::
		$ python run.py -t search_replace -s "Array" -r "" -o "/path/to/file/output-sql-query.txt" table_name "/path/to/file/field-names.txt"

- Search in each field for the phrase "yummy cheese" and replace it with "moldy cheese":
	::
		$ python run.py -t search_replace_in -s "yummy cheese" -r "moldy cheese" -o "/path/to/file/output-sql-query.txt" table_name "/path/to/file/field-names.txt"