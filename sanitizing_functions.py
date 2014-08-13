# These are functions that actually sanitize the data. These are called from the DataDumper class.

# Please run Sanitize_win.py if you want to run the Data Dumper GUI.

import re

# determines the type of value being passed. Returns the data type.
# Examples of outputs:
# 2014 => integer
# 2014.07 => decimal
# 2014.07.23 => text
# 2014-07-23 => date
def get_type(value):
    if value.strip() == '' or value == '*':
        return 'none'
    elif value.isdigit():
        return "integer"
    elif value.replace(".", "", 1).isdigit():
        return "decimal"
    # These are the restrictions if the value is a date from the past millennium, formatted: 2014-07-16
    elif value.translate(None,"-/").isdigit():
        if value.startswith("1") or value.startswith("20"):
            if "/" in value:
                if value.index('/') == 4:
                    return "date"
            elif "-" in value:
                if value.index("-") == 4:
                    return "date"
    return "text"


# This is for sanitation done only on keys and that aren't done on the bulk of the data.
def sanitize_key(key_val, CHAR_BLACKLIST):
    san_val = key_val
    if '(' in san_val:
        san_val = remove_brackets(key_val, CHAR_BLACKLIST)
    san_val = split_upper(san_val)
    san_val = remove_characters_for_key(san_val, CHAR_BLACKLIST)
    san_val = remove_duplicates(san_val)
    san_val = remove_edge_underscores(san_val)
    return san_val

# reformats data passed to this function, returns the sanitized value.
def sanitize(col_val, CHAR_BLACKLIST):
    san_val = split_upper(col_val)
    san_val = remove_characters(san_val, CHAR_BLACKLIST)
    san_val = remove_duplicates(san_val)
    return san_val


# Removes text in brackets, and the brackets themselves
def remove_brackets(passed_value, CHAR_BLACKLIST):
    regex_string =  '(\([\s\S]*\))'
    regex = re.compile(regex_string,re.IGNORECASE)
    return re.sub(regex, "", passed_value)


def convert_slash_to_per(passed_value):
    # Code to deal with slashes, by replacing it with _per_. Intended purpose is to replace m/s with m_per_s
    san_val = passed_value
    while '/' in san_val:
        slash_index = san_val.index('/')
        # as long as the slash is not at the start or end of the string
        # check to see if two characters beside the / are strings or integers.
        if slash_index != 0 and slash_index != (len(san_val)-1):
            # if they're not integers
            if san_val[slash_index-1].isalpha() and san_val[slash_index+1].isalpha():
                san_val = san_val.replace('/', '_per_')
    return san_val

# Removes underscores in the first and last index
def remove_edge_underscores(passed_value):
    ret = passed_value
    if len(ret)>=1:
        if ret[0] == "_":
            ret = ret[1:]
        if ret[-1] == "_":
            ret = ret[:-1]
    return ret

# Removes symbols specified in the char blacklist, and gets rid of uppercases and spaces
def remove_characters (passed_value, CHAR_BLACKLIST):
    return passed_value.lower().replace(' ', '_').translate(None,CHAR_BLACKLIST)

# Removes the symbols and replaces /s and -s with underscores
def remove_characters_for_key (passed_value, CHAR_BLACKLIST):
    san_val = remove_characters(passed_value, CHAR_BLACKLIST)
    san_val = san_val.replace("/", "_").replace("-", "_")
    return san_val

# Converts any number of repeating underscores to a single underscore
def remove_duplicates (passed_value):
    return re.sub(r'_{2}_*', '_', passed_value)

# splits a string with underscores at capital letters. Returns reformatted value.
# Examples of outputs:
# TrueVDpth > true_v_dpth
# RRDate > rr_date
# Triples Run-time
def split_upper(passed_value):
    if len(passed_value) > 0:
        ret = passed_value[0]
        lastChar = '0' # some arbitrary declaration value
        for i in range (1, len(passed_value)):
            # if it changes from lower to upper or upper to lower, insert an underscore
            if (passed_value[i].isupper() and lastChar.islower()):
                ret = ret[:-1] + lastChar + '_' + passed_value[i]
            elif(passed_value[i].islower() and lastChar.isupper()):
                ret = ret[:-1] + '_' + lastChar + passed_value[i]
            else:
                ret += passed_value[i]
            lastChar = passed_value[i]
        # replaces spaces with underscores, and reduces any amount of repeating underscores to a single underscore
        ret = ret.replace(' ', '_')
        return ret
    else:
        return passed_value


# Sanitizes the class name for the django model
# Removes underscores and capitalizes words
def django_class_name(passed_value):
        value = str(passed_value)
        # Removes the file path, keeps the name
        if value[-1]=='/':
            value = value[:-1]
        if '/' in value:
            value = value[value.rindex("/")+1:]

        ret = value[0].upper()
        lastChar = '0'
        for i in range (1, len(value)):
            # if the previous character is an underscore, remove it and make the current character uppercase
            if lastChar == '_':
                ret = ret[:-1] + value[i].upper()
            else:
                ret += value[i]
            lastChar = value[i]
        # if an underscore is overlooked (Ex: if the last character is an underscore), remove it
        ret = ret.translate(None,'_')
        return ret
