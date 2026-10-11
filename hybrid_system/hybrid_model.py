
import sys
import random
import importlib.util
import traceback
from pathlib import Path
from datetime import datetime

import pandas as pd
import joblib



BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

DAY1_FILE = ROOT_DIR / "day1" / "machine.py"
MODEL_FILE = ROOT_DIR / "day2" / "random_forest_model.pkl"
LOG_FILE = BASE_DIR / "hybrid_log.txt"

FEATURES = [
    "temperature",
    "pressure",
    "vibration",
    "rpm",
    "current"
]



def load_day1():
    if not DAY1_FILE.exists():
        raise FileNotFoundError(
            f"Day 1 file not found: {DAY1_FILE}\n"
            "Check whether day1/machine.py exists."
        )

    spec = importlib.util.spec_from_file_location(
        "day1_machine", DAY1_FILE
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["day1_machine"] = module
    spec.loader.exec_module(module)
    return module


def load_ai_model():
    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            f"AI model not found: {MODEL_FILE}\n"
            "Check whether day2/random_forest_model.pkl exists."
        )

    return joblib.load(MODEL_FILE)



def generate_reading(day1):
    return day1.generate_sensor_data()



def get_logical_decision(day1, reading):
    rule_name, action = day1.evaluate_rules(
        reading, day1.RULES
    )
    return rule_name, action




def get_ai_prediction(model, reading):
    input_data = pd.DataFrame(
        [[reading[feature] for feature in FEATURES]],
        columns=FEATURES
    )

    prediction = str(model.predict(input_data)[0])

    confidence = None
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_data)[0]
        confidence = float(max(probabilities)) * 100

    return prediction, confidence


def combine_decisions(rule_name, logical_action, ai_state):
    if logical_action == "EMERGENCY_STOP":
        return "STOPPED", "EMERGENCY_STOP"

    if logical_action == "STOP_MACHINE":
        return "STOPPED", "STOP_MACHINE"

    if ai_state == "STOPPED":
        return "STOPPED", "STOP_MACHINE"

    warning_actions = {
        "REDUCE_LOAD",
        "COOL_MACHINE",
        "CHECK_PRESSURE"
    }

    if logical_action in warning_actions:
        return "WARNING", logical_action

    if ai_state == "WARNING":
        return "WARNING", "INSPECT_MACHINE"

    return "NORMAL", "CONTINUE_NORMAL"


def get_shared_decision(rule_name, logical_action, ai_state):
    final_status, final_action = combine_decisions(
        rule_name, logical_action, ai_state
    )

    day1_final = (final_status, final_action)
    day2_final = (final_status, final_action)

    return day1_final, day2_final



def log_result(machine, reading, rule, action,
               ai_state, confidence, final_status,
               final_action):

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(f"\nTimestamp: {datetime.now()}\n")
        file.write(f"Machine: {machine}\n")
        file.write(f"Sensor readings: {reading}\n")
        file.write(f"Logical rule: {rule}\n")
        file.write(f"Logical action: {action}\n")
        file.write(f"AI prediction: {ai_state}\n")

        if confidence is not None:
            file.write(f"AI confidence: {confidence:.2f}%\n")

        file.write(f"Final status: {final_status}\n")
        file.write(f"Final action: {final_action}\n")
        file.write("-" * 50 + "\n")



def main():
    print("=" * 60)
    print("HYBRID INDUSTRIAL MACHINE MONITORING SYSTEM")
    print("=" * 60)

    day1 = load_day1()
    model = load_ai_model()

    LOG_FILE.write_text(
        "HYBRID MACHINE MONITORING LOG\n",
        encoding="utf-8"
    )

    machines = getattr(
        day1,
        "MACHINES",
        ["Industrial Machine"]
    )

    for tick in range(1, 4):
        print(f"\n{'=' * 60}")
        print(f"TICK {tick}")
        print("=" * 60)

        for machine in machines:
            reading = generate_reading(day1)

            rule_name, logical_action = get_logical_decision(
                day1, reading
            )

            ai_state, confidence = get_ai_prediction(
                model, reading
            )
            day1_final, day2_final = get_shared_decision(
                rule_name, logical_action, ai_state
            )

            day1_status, day1_action = day1_final
            day2_status, day2_action = day2_final

            print(f"\nMachine: {machine}")
            print(f"Sensor readings: {reading}")
            print(f"Day 1 final status: {day1_status}")
            print(f"Day 1 final action: {day1_action}")
            print(f"Day 2 final status: {day2_status}")
            print(f"Day 2 final action: {day2_action}")

            if confidence is not None:
                print(f"AI confidence: {confidence:.2f}%")

            print(f"FINAL STATUS: {day2_status}")
            print(f"FINAL ACTION: {day2_action}")

            log_result(
                machine, reading, rule_name, logical_action,
                ai_state, confidence, day1_status, day1_action
            )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"\nERROR: {error}")
        print("\nCheck the file paths and installed dependencies.")

