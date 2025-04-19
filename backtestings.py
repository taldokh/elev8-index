import os

from main import backtest

# All boolean combinations
bool_combinations = [
    (True, True),
    (True, False),
    (False, True),
    (False, False)
]

for equities_per_firm in range(1, 11):
    for number_of_firms in range(1, 11):
        for selection_type_top, relative_weight in bool_combinations:
            # Set env vars
            os.environ["EQUITIES_PER_FIRM"] = str(equities_per_firm)
            os.environ["NUMBER_OF_FIRMS"] = str(number_of_firms)
            os.environ["SELECTION_TYPE_TOP"] = str(selection_type_top)
            os.environ["RELATIVE_WEIGHT"] = str(relative_weight)

            print(f"\nRunning backtest with: "
                  f"EQUITIES_PER_FIRM={equities_per_firm}, "
                  f"NUMBER_OF_FIRMS={number_of_firms}, "
                  f"SELECTION_TYPE_TOP={selection_type_top}, "
                  f"RELATIVE_WEIGHT={relative_weight}\n")

            try:
                backtest()
            except Exception as e:
                print(f"Backtest failed for this config: {e}")
