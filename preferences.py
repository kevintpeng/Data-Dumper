# These are functions created for the data dumper.
# Please run Sanitize_win.py if you want to run the Data Dumper GUI.

# PREFERENCES AND SETTINGS
# -------------------------------------------------------------------------------------------------
# This class stores values for all of the user input, as well as the default settings on boot.

import os.path
import yaml

class Preferences():
    def __init__(self, settings_path):
        self.settings_path = settings_path
        # Checks for existence of settings file
        if not os.path.isfile(self.settings_path):
            self.generate_settings_file()

        self.load_settings_file()


    # used when there is no setting file to read from
    # This will generate a new file with the following values determined as defaults.
    def generate_settings_file(self):
        f = open(self.settings_path, "wb+")
        # These are the set default values
        yaml.dump({'CACHE_SIZE': 100,
                   'CHAR_BLACKLIST': '!@#$%^&():;*',
                   'CONFIDENCE_PERCENT': 0.4,
                   'DATABASE': 'database',
                   'HOST': 'local host',
                   'FILE_IN': 'data.csv',
                   'USERNAME': 'username',
                   'INFERENCE_SIZE': 100}, f)
        f.close()

    # Loads the settings file and saves its values into cached variables
    def load_settings_file(self):
        f = open(self.settings_path)
        settings = yaml.safe_load(f)
        f.close()

        self.host = settings["HOST"]
        self.database = settings["DATABASE"]
        self.cache_size = settings["CACHE_SIZE"]
        self.char_blacklist = settings["CHAR_BLACKLIST"]
        self.confidence_percent = float(settings["CONFIDENCE_PERCENT"])
        self.file_in = settings["FILE_IN"]
        self.file_out = self.file_in.replace(".csv", "_clean.csv")
        self.username = settings["USERNAME"]
        self.inference_size = settings["INFERENCE_SIZE"]
        self.map_file = self.file_in.replace(".csv", "_map.yaml")

    # Overwrites the current values in the settings files with the values of the variables
    def write_settings_file(self):
        f = open(self.settings_path, "wb+")
        # These are the set default values
        yaml.dump({'CACHE_SIZE': self.cache_size,
                   'CHAR_BLACKLIST': self.char_blacklist,
                   'CONFIDENCE_PERCENT': self.confidence_percent,
                   'DATABASE': self.database,
                   'HOST': self.host,
                   'FILE_IN': self.file_in,
                   'USERNAME': self.username,
                   'INFERENCE_SIZE': self.inference_size}, f)
        f.close()

    # Overwrites the current variables with the variables in the fields on the main screen
    def check_fields(self, file_in, file_out, schema, table, password):
        self.file_in = file_in
        self.file_out = file_out
        self.schema = schema
        self.table = table
        self.password = password
        self.map_file = str(self.file_in)
        self.map_file = self.map_file.replace(".csv", "_map.yaml")

    # This is the function used when the "Save Changes" button is pressed in the settings window
    # It will overwrite the current variables in memory with the ones in the fields on the settings screen
    def update_settings(self, host, database, username, confidence_percent, inference_size, blacklist):
        self.host =host
        self.database = database
        self.username = username
        self.confidence_percent = confidence_percent
        self.inference_size = inference_size
        self.char_blacklist = blacklist