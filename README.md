# ETL EXAMPLE STEP 6
---

version 0.1 
Note that the explanation below is still obtuse and will be reworked.

** Towards automating the ETL process **

You are reading the `README.md `file in the `ETL_6` repository for Russ Robbins. This repository shows files related to:

- Reading a text file which represents a codebook for a data file
- Writing a series of comma separated values (CSV) files that could be used by an automated process that uses Oracle tools such as SQL Loader, ODI, or PL/SQL.

Note that an alterative process is opening a connection to the database, creating tables, and inserting the data directly from a program, such as the one shown in this repository.

# Inputs to Step 6

** Inputs from IHIS web site **

 - `ihis_household_1997_2014.cbk`
 - `ihis_household_1997_2014.dat`
 - outputs from steps 5, 4, 3, 2, and 1
   - not referenced here for brevity
   - see specific repostories for outputs

Note that `ihis_household_1997_2014.dat `has lines that are composed of fields. The information in these fields (at the end of this extended ETL, multiple repository example) will be placed in columns in Oracle data tables. The information in the columns of the Oracle data tables will relate (via foriegn key) to other Oracle code tables that explain (and constrain) the data table column values.

Note that ihis_household_1997_2014.cbk describes ihis_household_1997_2014.dat and is the source for much of the information to be used in the ETL process.

# Processing in Step 6

 An early version program was built that can, after robust testing/fixing/refactoring, read a particular *.cbk (codebook) file and produce CSV files that represent:

- the names of the fields in the IHIS data file as well as their positions in any particular row. These names will be used as column names in Oracle tables.
- the names of the fields in the IHIS data file as well as a short written description of the information they represent. This information will be in the meta-data for Oracle tables.
- the fields in the data file, as well as all of the appropriate and possible values that can are associated with those fields.
- indications of which years sampled data has been drawn from IHIS data
- indications of whether variables were captured in that particular year's NHIS survey. Variables' values are stored in *.dat file fields, which in turn will be stored in Oracle data and code tables.
- information about the form of the *.dat file downloaded from IHIS

The file used to process `ihis_household_1997_2014.cbk` is `read_codebook.py`. The file that provides documentation of `read_codebook.py` (beyond inline documentation) is `read_codebook_README.md`.
	

# Outputs of Step 6

The program `read_codebook.py` read and parsed the input codebook file `ihis_household_1997_2014.cbk` which describes some data in the data file `ihis_household_1997_2014.dat`. The files created and output by `read_codebook.py` are:

- data file field names to be used as table column names as well as short descriptions of each of these
 - `CODE_DEFINITIONS.csv`
- data file field names to be used as table column names as well as the numeric positions in any line in the *.dat file which contains the value that will be placed in that column in an Oracle table.
 - `CODE_POSITIONS.csv`
- a file that indicates the years from which data was sampled when the IHIS web site provided data to be used by this ETL process.
 - `SAMPLES_NAMES_AND_TYPES.csv`
- a file that contains information about whether an IHIS code is in a sample drawn for a particular year. A file that is a key that explains how to read cell contents is also provided.
 - `CODED_DATA_BY_SAMPLE_INFO.csv`
 - `CODED_DATA_BY_SAMPLE_KEY.csv`
- files which include, for any field/column, the appropriate data values that are/can be stored in that field/column in the data file/Oracle tables. For the selected household data, the files are:
 - `CODE_VALUES_ASTATFLG.csv`
 - `CODE_VALUES_CSTATFLG.csv`
 - `CODE_VALUES_FAMACPTNO.csv`
 - `CODE_VALUES_FAMNUMTOT.csv`
 - `CODE_VALUES_LIVINGQTR.csv`
 - `CODE_VALUES_NONIVIEW.csv`
 - `CODE_VALUES_QUARTER.csv`
 - `CODE_VALUES_REGION`
 - `CODE_VALUES_YEAR`

Note that for any *.cbk file (which explains a *.dat file) when read_codebook.py is run against it, these files will always be created:

 - `CODE_DEFINITIONS.csv`
 - `CODE_POSITIONS.csv`
 - `SAMPLES_NAMES_AND_TYPES.csv`
 - `CODED_DATA_BY_SAMPLE_INFO.csv`
 - `CODED_DATA_BY_SAMPLE_KEY.csv`

Note also, that, based on what data is in a *.dat file (from IHIS) a series of additional CSV files will be created, based on information in a *.cbk file, which is provided with a *.dat file from IHIS. In this specific case, these were the files above with the prefix CODE_VALUES.


