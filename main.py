import os
from InsertEquitiesToDBTopRelative import insert_equities_to_db_relative_weight
from calculateIndexPoints import calculate_index_points
from generateEquitiesFile import generate_equities_file_top
from generateEquitiesFileTercile import generate_equities_file_tercile
from insertEquitiesToDB import insert_equities_to_db_equal_weight
from utils import helpers
import config.config as cg

# os.environ["SELECTION_TYPE_TOP"] = 'True'
# os.environ["RELATIVE_WEIGHT"] = 'True'
# os.environ["EQUITIES_PER_FIRM"] = '2'
# os.environ["NUMBER_OF_FIRMS"] = '3'

def backtest(selection_type_top: bool = helpers.str_to_bool(os.environ.get('SELECTION_TYPE_TOP')),
             relative_weight: bool = helpers.str_to_bool(os.environ.get('RELATIVE_WEIGHT')),
             equities_per_firm: int = helpers.validate_int_env_var('EQUITIES_PER_FIRM'),
             number_of_firms: int = helpers.validate_int_env_var('NUMBER_OF_FIRMS')):

    try:
        configuration_exist = helpers.is_configuration_already_exist(selection_type_top=selection_type_top,
                                                    relative_weight=relative_weight,
                                                    equities_per_firm=equities_per_firm,
                                                    number_of_firms=number_of_firms)

    except Exception as e:
        print(f"caught an error while trying to check if the configuration already exists. aborting backtesting. {e}")
        raise e

    if configuration_exist:
        print(f"""this configuration has already been backtested:
                  selection_type_top: {selection_type_top}
                  relative_weight: {relative_weight}
                  equities_per_firm: {equities_per_firm}
                  number_of_firms: {number_of_firms}  
              """)
    else:
        try:
            print("new configuration detected")
            print("creating configuration")
            config_id = helpers.create_configuration(selection_type_top=selection_type_top, relative_weight=relative_weight,
                                                   equities_per_firm=equities_per_firm, number_of_firms=number_of_firms)
        except Exception as e:
            print(f'error creating configuration. aborting. {e}')
            raise e

        try:
            if selection_type_top:
                generate_equities_file_top(equities_per_firm=equities_per_firm, number_of_firms=number_of_firms)
            else:
                generate_equities_file_tercile(equities_per_firm=equities_per_firm, number_of_firms=number_of_firms)
            if relative_weight:
                insert_equities_to_db_relative_weight(config_id)
            else:
                insert_equities_to_db_equal_weight(config_id)
            print("starting Backtesting")
            calculate_index_points(config_id)
        except Exception as e:
            print(f'somthing went wrong. Reverting... - {e}')
            helpers.delete_configuration(config_id)
        finally:
            helpers.remove_file(cg.RESULT_EQUITIES_FILE_PATH)

if __name__ == '__main__':
    backtest()



