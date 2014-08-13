import sys
from distutils.util import strtobool
from collections import OrderedDict
import psycopg2
import re

# TODO: Move units somewhere else, they don't belong here
# Units to friendly name mappings
# Also note dividing units must be first due to the nature of their sanitation

UNITS = OrderedDict([("E3m3/d", re.compile("[\s ]+E3m3/d[\s ]*")),
         ("m3/m3", re.compile("[\s ]+m3/m3[\s ]*")),
         ("m3/E3m3", re.compile("[\s ]+m3/E3m3[\s ]*")),
         ("E3m3", re.compile("[\s ]+E3m3[\s ]*")),
         ("m3", re.compile("[\s ]+m3[\s ]*")),
         ("kPag", re.compile("[\s ]+kPag[\s ]*")),
         ("kpa", re.compile("[\s ]+kpa[\s ]*")),
         ("Hours On", re.compile("[\s ]+Hours On[\s ]*")),
         ("%", re.compile("[\s ]+%[\s ]*")),
         ("C", re.compile("[\s ]+C[\s ]*")),])

# Match Codes
MATCH_PERFECT = 0x00
MATCH_CONTAINS_MULTIPLE = 0x01
MATCH_MISSING_COLUMNS = 0x02

MAX_LEVENSHTEIN_DISTANCE = 2

# yes/no prompt responses
PROMPT_RESPONSES = set(["yes", "y", "no", "n"])


def schema_table_insert(row, schema, table, conn):
    """Appends a row to eventually be inserted into the schema and table"""
    key_string = ",".join(("%s",) * len(row.keys())) % tuple(row.keys())
    value_string = ",".join(("%s",) * len(row.values()))
    with conn.cursor() as cur:
        query = """SET search_path TO %s;
            INSERT INTO %s (%s) VALUES (%s)""" % (schema, table, key_string, value_string)
        ### XXX: You have to mogrify here because it returns a binary string so you can't format the original query string with this value
        query = cur.mogrify(query, tuple(map(lambda v: to_clean_value(v) if v else None, row.values())))
        cur.execute(query)
    
    conn.commit()

    # rows is a array of rows
    # table is file output name
    # schema from preferences
    # Task:
    # insert rows to database
    # collect a bunch of rows and write at once
    #
def schema_table_insertmany(rows, schema, table, conn):
    key_string = ",".join(("%s",) * len(rows[0].keys())) % tuple(rows[0].keys())
    query = """SET search_path TO %s;
            INSERT INTO %s (%s) VALUES""" % (schema, table, key_string)
    with conn.cursor() as cur:
        values_string = ','.join("(" + cur.mogrify(",".join(("%s",) * len(row.values())) + ")", tuple(map(lambda v: to_clean_value(v) if v else None, row.values()))).decode("utf-8") for row in rows if row != None)
        cur.execute(query + values_string)
    conn.commit()
    
def schema_table_exists(schema, table, conn):
    """Determines if the given table exists in the schema"""
    query = """
        SELECT EXISTS(
            SELECT * 
            FROM information_schema.tables 
            WHERE 
                table_schema = '{0}' AND
                table_name = '{1}'
        );
        """.format(schema, table)
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchone()[0] == 't'
    
    #return False

def schema_table_create(column_mapping, user, schema, table, conn):
    """Creates the table in the given schema types are inferred and should be double checked manually, data is a tuple with the column name and sample data"""
    query = """SET search_path TO {0};
        CREATE TABLE {1} (
            {2}
            ) WITH (
                OIDS=FALSE
            );
            ALTER TABLE {3}
            OWNER TO {4};""".format(schema, table, ",".join([mapped_column[0] + " " + mapped_column[1] for mapped_column in column_mapping.items()]), table, user);
    
    with conn.cursor() as cur:
        cur.execute(query)
    
    conn.commit()
    
def to_clean_value(val):
    if val.isdigit():
        return int(val)
    elif val.replace(".", "", 1).isdigit():
        return float(val)
    else:
        return val
    
def get_data_type(datum):
    """Determines the data type to set for the PostgreSQL database"""
    
    if datum.isdigit():
        return "integer"
    elif datum.replace(".", "", 1).isdigit():
        return "decimal"
    return "text"

def verify_table(headers, schema, table, conn):
    """Tries to map the headers of a CSV file to table columns
    Returns a map that holds:
        "table" which is a map that contains a header to its closest column mappings and their levenshtein distance and a match flag determing whether or not the CSV verified perfectly
        "match" which is the match status
        "duplicates" which is a list of headers that contain multiple possible matches
        "close" which is a list of headers that have a close match
        "missing" which is a list of headers that have no close match
        
    The match flag is ORed with each constant to determine the final value"""
    match = MATCH_PERFECT
    query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE
            table_schema='%s' AND
            table_name='%s';
        """ % (schema, table)
    with conn.cursor() as cur:
        cur.execute(query)
        table_columns = cursor.fetchone()
    
        table = {}
        close = []
        missing = []
        
        for header in headers:
            converted_column = header_to_column(header)[0]
            
            closest = [table_columns[0]]
            closest_distance = levenshtein(converted_column, table_columns[0])
            
            for i in range(1, len(table_columns)):
                distances = levenshtein(converted_column, table_columns[i])
                
                if distance == closest_distance:
                    closest.append(table_columns[i])
                elif distance < closest_distance:
                    closest = [table_columns[i]]
                    closest_distance = distance
            
            table[header] = {
                "matches": closest,
                "distance": closest_distance
            }
            
            if closest_distance > 0 and closest_distance <= MAX_LEVENSHTEIN_DISTANCE:
                close.append(header)
                
            if closest_distance > MAX_LEVENSHTEIN_DISTANCE:
                missing.append(header)
                
            if closest_distance != 0:
                match = match | MATCH_MISSING_COLUMNS
                
            if len(closest) > 1:
                duplicates.append(header)
                match = match | MATCH_CONTAINS_MULTIPLE
        
        
        return {"table": table, "match": match, "duplicates": duplicates, "close": close, "far": missing}

def header_to_column(header):
    """Return a tuple containing the database column friendly string of the header and the units of the header if any"""
    clean = header
    unit = None
    
    # remove units
    for cur_unit, regex in UNITS.items():
        if len(regex.findall(header)) > 0:
            clean = regex.sub("", header[::-1], 1)[::-1]
            unit = cur_unit
            break
        
    clean = re.sub(r'[\s;-]','_', clean.strip()).replace("/", "_per_").replace("%", "percent").replace(":", "").lower()
    return (clean, unit)
    
def prompt(question):
    """Provides a yes/no prompt for a user with only the question (excludes trailing (y/n)) """
    response = input(question + " (Y/n)").lower()
    while response not in PROMPT_RESPONSES:
        response = input("Please enter a valid response. (Y/n)")
    return strtobool(response)
    
def levenshtein(s1, s2):
    """Computes the levenshtein distance between two strings"""
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
 
    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)
 
    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]