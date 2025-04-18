import os
from InsertEquitiesToDBTopRelative import insert_equities_to_db_relative_weight
from calculateIndexPoints import calculate_index_points
from generateEquitiesFile import generate_equities_file_top
from generateEquitiesFileTercile import generate_equities_file_tercile
from insertEquitiesToDB import insert_equities_to_db_equal_weight
import utils.utils as utils

os.environ["SELECTION_TYPE_TOP"] = 'True'
os.environ["RELATIVE_WEIGHT"] = 'False'
os.environ["EQUITIES_PER_FIRM"] = '4'
os.environ["NUMBER_OF_FIRMS"] = '3'


selection_type_top = utils.str_to_bool(os.environ.get('SELECTION_TYPE_TOP'))
relative_weight = utils.str_to_bool(os.environ.get('RELATIVE_WEIGHT'))

equities_per_firm = utils.validate_int_env_var('EQUITIES_PER_FIRM')
number_of_firms = utils.validate_int_env_var('NUMBER_OF_FIRMS')

if selection_type_top:
    generate_equities_file_top(equities_per_firm=equities_per_firm, number_of_firms=number_of_firms)
else:
    generate_equities_file_tercile(equities_per_firm=equities_per_firm, number_of_firms=number_of_firms)

if relative_weight:
    insert_equities_to_db_relative_weight()
else:
    insert_equities_to_db_equal_weight()

print("starting Backtesting")
calculate_index_points()
