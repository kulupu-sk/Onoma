from typing import Optional
import sqlite3
from sqlite3 import Error

from onoma.person_name import PersonName


class OnomaDatabase:
    """
    CRUD actions with an existing Onoma database.
    At the moment, only selection operation are supported.
    """
    # region Protected data
    _table_name = "name"
    _sql_create_table_name ="""
    CREATE TABLE IF NOT EXISTS `name` 
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        culture VARCHAR(4), 
        component VARCHAR(16), 
        gender VARCHAR(4), 
        alphabetic VARCHAR(64), 
        ideographic VARCHAR(64), 
        phonetic VARCHAR(64)
    );
    """
    # endregion

    def __init__(self):
        """
        Initialization of the SQLite connection.
        """
        self._connection = None

    def open(self, database_path: str) -> None:
        """
        Opens the database from its path.
        :param database_path: The path to the database
        :return: None.
        :exception: OSError if the database source_file could not be found.
        """
        try:
            self._connection = sqlite3.connect(database_path)
            result = self._create_tables()

            if not result:
                raise UserWarning("Tables could not be created")
        except Error as e:
            raise e

    def supported_cultures(self) -> list[str]:
        """
        Returns the list of all supported cultures.
        :return:
        """
        sql = f"SELECT DISTINCT `culture` FROM {self._table_name}"
        self._connection.row_factory = sqlite3.Row
        cursor = self._connection.cursor()
        cursor.execute(sql)
        self._connection.commit()
        fetched = cursor.fetchall()

        result = []

        for f in fetched:
            result.append(f["culture"])

        return result

    def select_name(self, item_id: int) -> Optional[PersonName]:
        """
        Selects a name item by its id.
        :param item_id: The id of the item to find.
        :return: The name item, if found, otherwise None.
        """
        sql = f"SELECT * FROM {self._table_name} WHERE id = {item_id}"

        self._connection.row_factory = sqlite3.Row
        cursor = self._connection.cursor()
        cursor.execute(sql)
        self._connection.commit()
        fetched = cursor.fetchone()

        return self._get_person_name(fetched)

    def select_names(self, pattern: str,
                     culture: str = '',
                     gender: str = '',
                     component='',
                     limit: int = -1) -> list[PersonName]:
        """
        Selects a number of person names defined by the name pattern and, optionally, culture, gender, and component.
        :param pattern: The alphabetic name pattern to find. The search is performed by containment, case-insensitive.
        :param culture: The culture to limit to; by default, all cultures.
        :param gender:  The gender to limit to; by default, all genders.
        :param component: The component to limit to; by default, both components.
        :param limit: The maximum number of results desired; by default, no limit.
        :return: List of name items fulfilling the query conditions.
        """
        sql = f"SELECT * FROM {self._table_name} WHERE `alphabetic` LIKE '%{pattern}%'"
        if len(culture) > 0:
            sql += f" AND `culture` = '{culture}'"

        if len(gender) > 0:
            sql += f" AND `gender` = '{gender}'"

        if len(component) > 0:
            sql += f" AND `component` = '{component}'"

        if limit > 0:
            sql += f" LIMIT {limit}"

        self._connection.row_factory = sqlite3.Row
        cursor = self._connection.cursor()
        cursor.execute(sql)
        self._connection.commit()

        fetched = cursor.fetchall()

        result = []

        for f in fetched:
            p = self._get_person_name(f)
            result.append(p)

        return result

    def select_names_random(self,
                            number_of_names: int,
                            cultures: list[str] = [],
                            gender: str = '',
                            component: str = '',
                            name_type: str = 'alphabetic'):
        """
        Selects a number of random person names.
        :param number_of_names: Number of names to generate.
        :param cultures: List of cultures from which to generate names; if left empty, all available cultures are taken.
        :param gender: The gender to limit to; by default, all genders.
        :param component: The component to limit to; by default, both components.
        :return: List of names generated.
        """
        if len(cultures) == 0:
            cultures = self.supported_cultures()

        culture_string = '('
        for culture in cultures:
            culture_string += f"'{culture}', "

        culture_string = culture_string.removesuffix(', ')
        culture_string += ')'

        sql = f"SELECT `{name_type}` FROM {self._table_name} WHERE `culture` IN {culture_string}"

        if len(gender) > 0:
            sql += f" AND `gender` = '{gender}'"

        if len(component) > 0:
            sql += f" AND `component` = '{component}'"

        sql += f" ORDER BY RANDOM() LIMIT {number_of_names}"

        self._connection.row_factory = sqlite3.Row
        cursor = self._connection.cursor()
        cursor.execute(sql)
        self._connection.commit()

        fetched = cursor.fetchall()

        result = []

        for f in fetched:
           result.append(f[0])

        return result

    def insert_name(self, person_name: PersonName):
        sql = f"INSERT INTO {self._table_name} VALUES (null, ?, ?, ?, ?, ?, ?)"

        self._connection.execute(sql,
                                 (person_name.culture,
                                  person_name.component,
                                  person_name.gender,
                                  person_name.alphabetic,
                                  person_name.ideographic,
                                  person_name.phonetic))
        self._connection.commit()

    def insert_names(self, person_names: list[PersonName]) -> None:
        cursor = self._connection.cursor()
        cursor.execute("begin")

        for person_name in person_names:
            sql = f"INSERT INTO {self._table_name} VALUES (null, ?, ?, ?, ?, ?, ?)"
            self._connection.execute(sql,
                                 (person_name.culture,
                                  person_name.component,
                                  person_name.gender,
                                  person_name.alphabetic,
                                  person_name.ideographic,
                                  person_name.phonetic))

        self._connection.commit()

    # region Protected Auxiliary
    def _create_tables(self) -> bool:
        """
        Creates all defined tables.
        :return: True, if the operation succeeded.
        """
        result = True
        result &= self._create_table(self._sql_create_table_name)

        return result

    def _create_table(self, sql_creation: str) -> bool:
        """
        Create a specified SQL table.
        :param sql_creation: The creation SQL for the table.
        :return: True, if the operation succeeded.
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(sql_creation)
            return True
        except Error:
            return False

    def _get_person_name(self, fetched) -> Optional[PersonName]:
        """
        Converts a fetched SQLite database row into a PersonName object.
        :param fetched: The SQL row to create from.
        :return: The PersonName object created, if successful, otherwise None.
        """
        try:
            result = PersonName()
            result.id = fetched["id"]
            result.culture = fetched["culture"]
            result.gender = fetched["gender"]
            result.component = fetched["component"]
            result.alphabetic = fetched["alphabetic"]
            result.phonetic = fetched["phonetic"]
            result.ideographic = fetched["ideographic"]

            return result

        except:
            return None
    # endregion


if __name__ == '__main__':
    database_path = "onoma_test.db3"

    db = OnomaDatabase()
    db.open(database_path)

    person_names = [PersonName(culture='PL', gender='F', component='given', alphabetic='Agnieszka'),
                    PersonName(culture='PL', gender='F', component='given', alphabetic='Jadwiga')]

    db.insert_names(person_names)

