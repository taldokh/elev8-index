import os

from main import backtest

# All boolean combinations
bool_combinations = [
    (True, True),
    (True, False),
    (False, True),
    (False, False)
]

for number_of_firms in range(10, 0, -1):
    for equities_per_firm in range(10, 0, -1):
        for selection_type_top, relative_weight in bool_combinations:

            print(f"\nRunning backtest with: "
                  f"EQUITIES_PER_FIRM={equities_per_firm}, "
                  f"NUMBER_OF_FIRMS={number_of_firms}, "
                  f"SELECTION_TYPE_TOP={selection_type_top}, "
                  f"RELATIVE_WEIGHT={relative_weight}\n")

            try:
                backtest(selection_type_top=selection_type_top, relative_weight=relative_weight, number_of_firms=number_of_firms, equities_per_firm=equities_per_firm)
            except Exception as e:
                print(f"Backtest failed for this config: {e}")
