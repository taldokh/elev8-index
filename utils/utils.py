import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config.config as cg
from models.configuration_model import Configuration

def str_to_bool(s):
    if s:
        return s.lower() in ("true", "1", "yes", "y")
    return False


def validate_int_env_var(key: str):
    try:
        return int(os.environ.get(key))
    except:
        print(f'environment variable {key} is invalid')


def is_configuration_already_exist(equities_per_firm, number_of_firms, selection_type_top, relative_weight):
    engine = create_engine(f'postgresql://{cg.DB_USERNAME}:{cg.DB_PASSWORD}@{cg.DB_HOST}:5432/{cg.DB_NAME}')
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Example values to check (replace with actual env values or parameters)
        equities_per_firm = int(os.getenv('EQUITIES_PER_FIRM', 4))  # Replace with real value
        number_of_firms = int(os.getenv('NUMBER_OF_FIRMS', 3))  # Replace with real value
        selection_type_top = str_to_bool(os.getenv('SELECTION_TYPE_TOP', 'True'))  # Replace with real value
        relative_weight = str_to_bool(os.getenv('RELATIVE_WEIGHT', 'False'))  # Replace with real value

        # Query to check if the configuration already exists
        existing_config = session.query(Configuration).filter_by(
            equities_per_firm=equities_per_firm,
            number_of_firms=number_of_firms,
            selection_type_top=selection_type_top,
            relative_weight=relative_weight
        ).first()

        if existing_config:
            print("Configuration already exists:", existing_config.id)
            return True
        else:
            print("Configuration does not exist.")
            return False

    except Exception as e:
        print(f"Error checking configuration: {e}")
        return False

    finally:
        # Close the session to release resources
        session.close()
