from onoma.onoma_database import OnomaDatabase
from onoma.person_name import PersonName


class WikiUploader:
    """
    Tool class to upload given female, given male, and family names
    for a culture using text files (obtained from Wikipedia).
    """
    def __init__(self, database_source: str):
        self._database = OnomaDatabase()
        self._database.open(database_source)

    def upload_names(self, file_name: str, culture: str, gender: str, component: str):
        """
        Uploads names onto the database.
        :param file_name: The file name to take the names from.
        :param culture: The onomastic culture (e.g. "IT" for Italian).
        :param gender: The gender. Supported are: 'F', 'M', 'A'.
        :param component: Given name or family name. Supported: 'family', 'given'.
        :return: None.
        """
        names = list[PersonName]()

        with open(file_name, 'r') as file:
            lines = file.read().split('\n')

        for line in lines:
            pn = PersonName()
            pn.gender = gender
            pn.culture = culture
            pn.component = component
            pn.alphabetic = line.strip()

            names.append(pn)

        self._database.insert_names(names)

if __name__ == '__main__':
    database_path = "../../../Data/onoma.db3"

    uploader = WikiUploader(database_path)

    # Upload Greek female given names
    # file_name = "../../../Data/greek_female_given_names.txt"

    # uploader.upload_names(file_name, "GR", "F", "given")

    # Upload Greek male given names
    # file_name = "../../../Data/greek_male_given_names.txt"

    # uploader.upload_names(file_name, "GR", "M", "given")

    # Upload Greek family names
    # file_name = "../../../Data/greek_family_names.txt"

    # uploader.upload_names(file_name, "GR", "A", "family")

    # Upload Italian female given names
    # file_name = "../../../Data/italian_female_given_names.txt"

    # uploader.upload_names(file_name, "IT", "F", "given")

    # Upload Italian male given names
    # file_name = "../../../Data/italian_male_given_names.txt"

    # uploader.upload_names(file_name, "IT", "M", "given")

    # Upload Italian family names
    file_name = "../../../Data/italian_family_names.txt"

    uploader.upload_names(file_name, "IT", "A", "family")