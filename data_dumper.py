# These are functions created for the data dumper. They are run when buttons are pushed from the sanitize_win GUI.
# These functions generally organize and read data, as well as write sanitized data.

# Please run Sanitize_win.py if you want to run the Data Dumper GUI.

import csv
import os.path
import psycopg2
import yaml
from collections import OrderedDict

import psql_tools
import sanitizing_functions
from preferences import Preferences


class DataDumper():
    def __init__(self):
        self.preferences = Preferences("settings_default.yaml")
        self.mapping = None

    # MAP CSV FILE, Triggered by button press
    # ------------------------------------------------------------------------------------------
    # The purpose is to map the names of the columns with its properties,
    # in order to quickly read important information when creating a django model,
    # exporting to postgres or sanitizing the data.
    # A map of the output has four columns:
    #   a. The original header name
    #   b. The sanitized header name
    #   c. The data type for the column
    #   d. T/F if it has any blank entries in the table

    def csv_map(self, set_status, make_map):
        with open(self.preferences.file_in, "rb") as file_in:
            reader = csv.DictReader(file_in, delimiter=',')

            # Run Type Inference
            # Creates two dictionaries. Column_type will keep track of the current type per column.
            # check_blank keeps track of whether there are any blank data entries in the column.
            set_status("Inferring the Type.")
            print ("Inferring the Type.")
            check_blank = {}
            column_type = {}
            inference_count = {}
            inference_threshold = self.preferences.inference_size*self.preferences.confidence_percent
            # Cycles through the csv file checking each column by row and reads the type.
            row_count = 0
            for row in reader:
                # pop is needed to remove cases where there is an empty key
                row.pop(None, None)
                row.pop("", None)
                row_count += 1
                for key, val in row.items():
                    # initializes inference count dictionary if it doesn't exist.
                    # inference_count keeps track of how many values have been checked that haven't returned 'none'
                    if key not in inference_count:
                        inference_count[key] = 0
                    # while the loop hasn't reached the confidence percent of the inference size, keep reading
                    if inference_count[key] < inference_threshold:
                        new_type = sanitizing_functions.get_type(val)
                         # if there aren't any values in the column_type dictionary yet, initialize the values.
                        if key not in column_type:
                            column_type[key] = new_type
                            if new_type == 'none':
                                check_blank[key] = True
                            else:
                                check_blank[key] = False
                        # as long as the values have something in them, run a type check.
                        elif new_type != 'none':
                            cur_type = column_type[key]
                            if new_type == 'text':
                                column_type[key] = new_type
                            elif new_type == 'date' and cur_type != 'text':
                                column_type[key] = new_type
                            elif new_type == "decimal" and cur_type != "date" and cur_type != 'text':
                                column_type[key] = new_type
                            elif new_type == "integer" and cur_type != "decimal" and \
                                            cur_type != "date" and cur_type != 'text':
                                column_type[key] = new_type
                        else:
                            check_blank[key] = True
                        # add one to the counter if not 'none'
                        if new_type != 'none':
                            inference_count[key] += 1
            # Check to make sure it is a confident inference. If smaller, returns a warning message
            if row_count < self.preferences.inference_size:
                inference_threshold = row_count*self.preferences.confidence_percent
            for key, val in inference_count.items():
                if val < inference_threshold:
                    print "WARNING: A confident type inference could not be made for column %s: %s/%s" % (key,val,inference_threshold)

            # Run Mapping to YAML
            # We can now use the three dictionaries created above to create a mapping.
            set_status("Sanitizing Keys.")
            print ("Sanitizing Keys.")
            all_rows = {}
            # Evaluates each key from the reader, sanitizes it and saves its type
            for key in reader.fieldnames:
                # gets rid of columns with empty keys
                if key == '' or key is None:
                    continue
                map_row = []
                san_key = sanitizing_functions.sanitize_key(key, self.preferences.char_blacklist)
                map_row.append(("new_name", san_key))
                map_row.append(("data_type", column_type[key]))
                map_row.append(("has_blank", check_blank[key]))
                map_row = dict(map_row)
                all_rows[key] = map_row
                all_rows = OrderedDict(all_rows)
            f = open(self.preferences.map_file, "wb+")
            # This outputs the "all_rows" dictionary to a yaml file. The mapping is now complete.
            yaml.dump(all_rows, f)
            f.close()
            set_status(("Wrote %s" % (self.preferences.map_file)))
            print("Wrote %s" % (self.preferences.map_file))



    # DATA SANITATION Triggered by button press.
    # --------------------------------------------------------
    # The purpose of this function is to take data from a file
    # and output a new sanitized file with a standardized format.
    # 1. A sanitized output, where all data is:
    #   a. Lowercase
    #   b. No symbols
    #   c. Words are separated by underscores

    def csv_sanitize(self, set_status, make_map):
        with open(self.preferences.file_in, "rb") as file_in:
            reader = csv.DictReader(file_in, delimiter=',')
            with open(self.preferences.file_out, "wb+") as f_out:
                # if the mapping exists, run the sanitation
                # if the program can't find the mapping, it will create one if the checkbox is checked off, or
                # it will return an error message if it is not checked.
                if os.path.isfile(self.preferences.map_file):
                    column_mapping = []
                    with open (self.preferences.map_file, "rb") as file_map:
                        map_dictionary = yaml.load(file_map)
                        # makes a list of all the sanitized names. These are used as keys when writing the clean csv.
                        for item in map_dictionary:
                            column_mapping.append(map_dictionary[item]['new_name'])

                        # Sanitize data
                    set_status("Sanitizing the Data.")
                    print "Sanitizing the Data."
                    csvwriter = csv.DictWriter(f_out, fieldnames=column_mapping)
                    # Write the keys to the file
                    csvwriter.writeheader()
                    # Cycles through the csv file checking each column by row and sanitizing.
                    rowcount= 0
                    for row in reader:
                        rowcount += 1
                        if rowcount%1000==0:
                            print rowcount
                        row.pop(None, None)
                        row.pop("", None)
                        # clears the current row
                        new_row = {}
                        # adds the new row
                        for key, val in row.items():
                            new_row[map_dictionary[key]["new_name"]] = sanitizing_functions.sanitize(val, self.preferences.char_blacklist)
                        # writes the current row
                        csvwriter.writerow(new_row)
                    set_status("Wrote new sanitized .csv to %s" % (self.preferences.file_out))
                    print ("Wrote new sanitized .csv to %s" % (self.preferences.file_out))

                else:
                    if make_map:
                        self.csv_map(set_status, make_map)
                        self.csv_sanitize(set_status, make_map)
                    else:
                        print("%s could not be found or does not exist. "
                              "Please press map .csv if you haven't created a map yet." % (self.preferences.map_file))
                        set_status("%s could not be found or does not exist. "
                                   "Please press map .csv if you haven't created a map yet."
                                   % (self.preferences.map_file))




    # DJANGO MODEL CREATION, Triggered by menu button
    # -----------------------------------------------------------------------
    # The purpose is to output a .py file with a class in Django model format
    # Output is file_out_django.py

    def create_django_model(self, set_status, make_map):

        try:
            # This will read the mapping file and will store the columns in lists for later access
            with open (self.preferences.map_file, "rb") as file_map:
                map_dictionary = yaml.load(file_map)
                col_names = []
                col_type = []
                col_blank = []
                # reads the column name and type from the map file and stores as lists
                for item in map_dictionary:
                    col_names.append(map_dictionary[item]['new_name'])
                    col_type.append(map_dictionary[item]['data_type'])
                    col_blank.append(map_dictionary[item]['has_blank'])
            # This will create and write out the django file
            py_file = (self.preferences.file_in).replace('.csv','_django.py')
            with open (py_file, 'w+') as export_file:
                # Writes the class name, removing underscores and capitalizing words.
                export_file.write("class %s(models.Model):\n" %
                                  (sanitizing_functions.django_class_name(self.preferences.file_out.replace(".csv", ""))))
                # converts type to its respective field type
                for i in range(0, len(col_names)):
                    if col_type[i] == 'integer':
                        field_type = 'Integer'
                    elif col_type[i] == 'decimal':
                        field_type = 'Float'
                    elif col_type[i] == 'date':
                        field_type = "Date"
                    else:
                        field_type = 'Text'
                    # Writes the row to the file.
                    # This is an example of the output line:
                    #   field = models.TextField(blank = True)
                    export_file.write("   %s = models.%sField" % (col_names[i], field_type))

                    if col_blank[i] == True:
                        export_file.write("(blank = True)\n")
                    else:
                        export_file.write("()\n")
            print("Django model created!")
            set_status("Django model created!")
        except IOError:
            if make_map:
                self.csv_map(set_status, make_map)
                self.create_django_model(set_status, make_map)
            else:
                print("%s could not be found or does not exist. "
                      "Please press map .csv if you haven't created a map yet."
                      % (self.preferences.map_file))
                set_status("%s could not be found or does not exist. "
                           "Please press map .csv if you haven't created a map yet."
                           % (self.preferences.map_file))



    # EXPORT TO POSTGRES, Triggered by menu button
    #------------------------------------------------------
    # The purpose of this is to export the data to postgres database. This reads the raw data.
    # A lot of functions in this section are used from Jay's psql_tools.py file
    # For more documentation, read through psql_tools

    def create_postgres(self, set_status, make_map):
        column_mapping = []
        with open (self.preferences.map_file, "rb") as file_map:
            map_dictionary = yaml.load(file_map)
            for item in map_dictionary:
                column_mapping.append((item, {"new_name": map_dictionary[item]['new_name'],
                                              "data_type": map_dictionary[item]['data_type']}))
        column_mapping = OrderedDict(column_mapping)
        print column_mapping


        print("Connecting to %s ... with username: %s" % (self.preferences.host, self.preferences.username))
        connection_string = "dbname='%s' user='%s' host='%s' password=%s" % (self.preferences.database,
                                                                             self.preferences.username,
                                                                             self.preferences.host,
                                                                             self.preferences.password)
        conn = None
        try:
            conn = psycopg2.connect(connection_string)
        except:
            print("Unable to connect to database")



        table_exists =  psql_tools.schema_table_exists(self.preferences.schema, self.preferences.schema, conn)
        if not table_exists:
            table_mapping = {}
            for original_name, data in column_mapping.items():
                table_mapping[data['new_name']] = data['data_type']
            psql_tools.schema_table_create(table_mapping,
                                           self.preferences.username,
                                           self.preferences.schema,
                                           self.preferences.schema, conn)

        cache = []
        with open(self.preferences.file_in, "rb") as file_in:

            reader = csv.DictReader(file_in, delimiter=',')

            # Cycles through the csv file checking each column by row and sanitized.
            for row in reader:
                row.pop(None, None)
                row.pop("", None)
                if len(cache) == self.preferences.cache_size:
                    # insert cache to database
                    psql_tools.schema_table_insertmany(cache, self.preferences.schema, self.preferences.schema, conn)
                    cache = []
                else:
                    new_row = []
                    for key, val in row.items():
                        new_row.append((column_mapping[key]['new_name'], val.replace('*', '')))
                    new_row = OrderedDict(new_row)
                    cache.append(new_row)
            psql_tools.schema_table_insertmany(cache, self.preferences.schema, self.preferences.schema, conn)
        set_status("Exported to postgreSQL!")
        print("Exported to postgreSQL!")