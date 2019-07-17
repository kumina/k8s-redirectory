"""
CSV Importer
============

The CSV Importer takes care of importing CSV files containing Redirect Rules
and adding them into the SQL database of the management pod.

The behaviour:

1. If a rule in the CSV already exists it is going to be ignored.
2. If a syntax/parsing error occurs somewhere in the CSV file the whole import
   is marked as **failed** and all of the changes to the database are roll backed.

"""
import io
import csv

from werkzeug.datastructures import FileStorage
from kubi_ecs_logger import Logger, Severity

from redirectory.libs_int.database import add_redirect_rule, DatabaseManager


class CSVImporter:
    """
    A new **CSVImporter** is created for every import and the data of the CSV file
    is passed as a parameter in the constructor of the class.
    """

    csv_reader = None
    """Reader object used to parse the CSV file"""
    data_template = {
        "domain": None,
        "domain_is_regex": None,
        "path": None,
        "path_is_regex": None,
        "destination": None,
        "destination_is_rewrite": None,
        "weight": None
    }
    """This is the template that the CSV is checked against. Every row of the CSV must match this template
    otherwise the whole import will fail"""

    def __init__(self, csv_byte_file_in: FileStorage):
        assert csv_byte_file_in.mimetype == "text/csv", "The file must be of type CSV."

        # Get String IO object from encoded stream
        csv_string = csv_byte_file_in.stream.read().decode("utf-8")
        csv_string_file = io.StringIO(csv_string)

        # Create a new dialect for parsing
        csv_dialect_name = "csv_redirectory_dialect"
        csv.register_dialect(csv_dialect_name,
                             delimiter=',',
                             quotechar='"',
                             quoting=csv.QUOTE_ALL,
                             skipinitialspace=True)

        # Parse the file
        self.csv_reader = csv.reader(csv_string_file, dialect=csv_dialect_name)

        # Get columns and validate
        self.columns = next(iter(self.csv_reader))
        self._validate_columns()

    def import_into_db(self):
        """
        Imports all the rules in the given csv file into the database as RedirectRules.
        If a rule is a duplicate it will be skipped.
        If there is an error in parsing the csv then all the changes will
        be roll backed and the whole import will be marked as fail.
        """
        db_session = DatabaseManager().get_session()

        try:
            row_counter = 1
            for row in self.csv_reader:
                row_counter += 1
                assert len(row) == len(self.columns), f"Entry at line: {row_counter} has different amount of " \
                    f"arguments than expected. Expected: {len(self.columns)} instead got: {len(row)}"

                self.data_template["domain"] = row[0]
                self.data_template["domain_is_regex"] = self._get_bool_from_str(row[1])
                self.data_template["path"] = row[2]
                self.data_template["path_is_regex"] = self._get_bool_from_str(row[3])
                self.data_template["destination"] = row[4]
                self.data_template["destination_is_rewrite"] = self._get_bool_from_str(row[5])
                self.data_template["weight"] = int(row[6])

                result = add_redirect_rule(db_session, **self.data_template, commit=False)
                if isinstance(result, int) and result == 2:  # 2 means already exists
                    raise AssertionError
        except AssertionError as e:
            Logger() \
                .event(category="import", action="import failed") \
                .error(message=str(e)) \
                .out(severity=Severity.ERROR)
            db_session.rollback()
        except Exception as e:
            Logger() \
                .event(category="import", action="import failed") \
                .error(message=str(e)) \
                .out(severity=Severity.CRITICAL)
            db_session.rollback()
        else:
            Logger() \
                .event(category="import", action="import successful",
                       dataset=f"Rules added from import: {row_counter - 1}")
            db_session.commit()

        DatabaseManager().return_session(db_session)

    def _validate_columns(self):
        """
        Validates that all the columns in the CSV file are according to the data template

        Raises:
             assertionError if something doesn't match
        """
        assert len(self.data_template) == len(self.columns), f"Invalid number of columns. " \
            f"Expected {len(self.data_template)} got {len(self.columns)}"

        for valid_column in self.data_template.keys():
            assert valid_column in self.columns, f"{valid_column} is a required column"

    @staticmethod
    def _get_bool_from_str(string: str) -> bool:
        """
        Simple conversion of a string to a boolean
        If the string is truthful e.g. 1 or true then True will be returned
        If it is anything else then a False is returned

        Args:
            string: the string to convert from

        Returns:
            the boolean representation of the string
        """
        return string.lower() in ["1", "true"]
