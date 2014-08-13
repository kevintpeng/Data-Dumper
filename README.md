Data-Dumper
===========
This project was created by Kevin Peng in July 2014. The Data Dumper is useful for processing data from the form .csv and cleaning up formatting, mapping information and exporting to postgreSQL and Django. Why is it important to sanitize data? Well this [XKCD](http://imgs.xkcd.com/comics/exploits_of_a_mom.png) comic gives a nice explanation.

The file format that it will take as input is called a .csv file. CSV stands for Comma, Separated, Values. It is a common file type for storing data in the form of a table. One problem is its lack of standardization, and this can lead to issues when analyzing data from it. It is for this reason that we use the data dumper to clean up data.

For setting up Dev Environment, check [Installation](https://github.com/kevinpeng97/Data-Dumper/blob/master/README.md#installation).

For understanding the functions of the program, check [Functions](https://github.com/kevinpeng97/Data-Dumper/blob/master/README.md#functions).

For Help navigating the GUI and first time set up, check [Usage](https://github.com/kevinpeng97/Data-Dumper/blob/master/README.md#usage)

## Installation
This section will cover setting up your dev environment such that it has all prerequisites to be able to run the data dumper. I am working in Windows 8.1, so installation will vary with OS. These installations must be complete in order to run the data dumper.
##### Install Python 2.7
Download [Python 2.7](http://downloads.activestate.com/ActivePython/releases/2.7.6.9/ActivePython-2.7.6.9-win32-x86.msi) from [ActiveState Python 2.7 x32](http://www.activestate.com/activepython/downloads)

This is the compiler. You will also probably want an IDE if you don't already have one. I used PyCharm 3.4.1.
##### Install PyQt4
PyQt4 is needed to create the GUI. All GUI design was done in Qt Designer, then exported using PyQt4 into a .py file.

For Windows, scroll to the bottom and download the Windows 32 bit instaler for Py2.7:
[PyQt4-4.11.1-gpl-Py2.7-Qt4.8.6-x32.exe](http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.1/PyQt4-4.11.1-gpl-Py2.7-Qt4.8.6-x32.exe)	Windows 32 bit installer or for a different OS: http://www.riverbankcomputing.co.uk/software/pyqt/download
##### Install Psycopg2
Psycopg2 lets python communicate with a PostgreSQL databases. It's needed if you are using the export to PostgreSQL function. Install http://initd.org/psycopg/download/ psycopg2
##### Install PyYAML
PyYAML was used for mapping and settings (More on that below). You need it because the program reads from YAML files to get default settings and input/output the mappings for each csv.
Install http://pyyaml.org/download/pyyaml/PyYAML-3.11.win32-py2.7.exe Or for other OS:
http://pyyaml.org/wiki/PyYAML

## Functions
This section will cover the major functions of the data dumper.
##### Mapping CSV
The map is a table with information about the data file. Think of it as a glossary in a book: it has information about each column in the data. The purpose is to map the names of the columns with its properties, in order to quickly read important information when creating a django model,exporting to postgreSQL or sanitizing the data. A map of the output has four columns: The original header name, The sanitized header name, The data type for the header and T/F if it has any blank entries in the table.

To create a mapping, type the input file name into the File Input field. Press the map .csv button to create a new mapping or overwrite an existing map. This will save a new file with the name file_in_map.csv in the current directory.
##### Sanitize CSV
The purpose of this function is to take data from a file and output a new sanitized file with a standardized format. The sanitized output will have all lowercase letters, no symbols and words separated by underscores. 

This takes the File Input .csv and saves a new csv file to csvfile_in_clean.csv by default or file_out.csv if a File Output is specified in the text field.  
##### Create Django Model
The purpose is to output a .py file with a class in Django model format. Output is file_out_django.py. 

The Django model includes each column from the data as a line in the model. Each line includes information about the column's type and whether it has any blank entries in it.
##### Export to PostgreSQL
The purpose is to export the data to the postgreSQL database. It takes input from the raw data, not the sanitized data. Rather than saving an output file on our computer, it sends the data to the database. The database, username, and host needs to be specified in the settings window (File>Settings).

## Usage
This section will cover how to navigate the GUI. Navigation should be relatively intuitive.
##### How to Launch The Application
There are six .py files that are needed to be able to run the application. They are as follows:
1. Sanitize_win.py
2. Settings_win.py 
3. data_dumper.py
4. preferences.py
5. sanitizing_functions.py
6. psql_tools.py

Sanitize_win.py is the main file. It references and uses classes and functions from all the other files. Sanitize_win is what you want to be running in order to launch the application. By launching it, an instance of the GUI will be generated and the user can now easily interact with all the functionality. 

##### Purpose of Each File
Sanitize_win.py launches the program and generates the GUI.

Settings_win.py is the GUI for the settings window; pretty straight forward. Sanitize_win will launch this if the settings button is pressed.

data_dumper.py includes all of the functions that control the organization, reading and writing of data. This includes all of the functions discussed in the above Functions section.

preferences.py stores all of the values from the text fields on the interface. Basically any user specified information is stored here and accessed from here when needed.

sanitizing_functions.py includes the specific functions that actually reformat the data, making changes to case, reformatting space to underscores, splitting words with underscores, etc... This is where all the sanitizing happens!

psql_tools.py is needed in order to connect to the postgreSQL database. All the functions in here are used to write to the database, send queries, etc...

##### Main Window
Upon launching the program, the user will see the main window. The main window has several text fields that take user input. Default values are specified in the code, and in settings for postgreSQL related text fields.

Starting with the first text field, the File Input field is where you input the file name for the data you want to export or clean. When mapping a .csv, it will use the input name and add _map to the file name (Ex: input = data.csv, map = data_map.csv). This file will be saved in the same directory as the input by default. The Open File button will open a file explorer, as an easier way to input the file name. 

File Output is the desired name of the clean output file. The new file will be a .csv file in the same directory as the input file by default. The program will, by default, add _clean to the file name (Ex: input=data.csv, output=data_clean.csv).

There are two buttons in the main window. The first says "Map .csv" and the second says "Sanitize .csv". Map .csv will create a new file or overwrite a current file with the same name. This file will contain the mapping for the input file. The second button, sanitize .csv will take the input file and clean each piece of data in the table.

Below is a checkbox, labelled "Create a mapping if it does not exist." Checking this box will cause the file to be mapped after pressing the sanitize .csv button if it does not exist.

Under File>Export, you can export to Django or PostgreSQL. Exporting to Django will create a new .py file, with specifically formatted data for Django use. Exporting to PostgreSQL will send the table to the database.

##### Settings
By clicking File>Settings, the settings UI will appear. The UI is split into two sections: Server Settings and Sanitizing Blacklist of Characters. In Server Settings, the user can adjust PostgreSQL values for database, username and host, as well as values for type inference including inference size and confidence %. 

In the Blacklist section, the user can add symbols, letters or phrases that are to be removed during the sanitizing process. All changes are automatically saved.
