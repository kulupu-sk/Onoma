from onoma.onoma_database import OnomaDatabase
from onoma.person_name import PersonName


class PolishUploader:
    def __init__(self, database_path: str):
        self._database = OnomaDatabase()
        self._database.open(database_path)

    def upload_file(self, file_name: str):
        with open(file_name, "r", encoding="utf-8") as file:
            lines = file.read().split('\n')

        person_names = []

        for line in lines:
            # PL;given;F;Agnieszka;;
            cells = line.split(';')
            culture = cells[0]
            component = cells[1]
            gender = cells[2]
            alphabetic = cells[3]

            person_name = PersonName(culture=culture, component=component, gender=gender, alphabetic=alphabetic)

            person_names.append(person_name)

        self._database.insert_names(person_names)


if __name__ == '__main__':
    database_path = "./onoma.db3"

    file_name = "../../../Data/polish_male_given_names.txt"

    uploader = PolishUploader(database_path)

    uploader.upload_file(file_name)

