from insertEquitiesToDB import insert_equities_to_db
from generateEquitiesFile import generate_equities_file

if __name__ == '__main__':
    generate_equities_file()
    insert_equities_to_db()
