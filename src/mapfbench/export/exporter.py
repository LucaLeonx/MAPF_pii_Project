import csv
from datetime import datetime
from typing import Any

import yaml

from mapfbench.description import Plan
from mapfbench.metrics.new_results import AggregatePlanResults


def export_results_to_csv(results: AggregatePlanResults, filename: str):
    lines = []
    for plan_result in results.per_plan_results.values():
        lines.append(plan_result)

    export_to_csv(lines, filename)


def export_to_csv(entries: list[dict[str, Any]], filename: str):
    if len(entries) == 0:
        return

    with open(filename, 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, entries[0].keys())
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry)


def export_to_yaml(dictionary: dict[str, Any], filename: str):
    with open(filename, 'w') as f:
        print(dictionary)
        yaml.safe_dump(dictionary, stream=f, indent=4, sort_keys=False)


def export_plan_results(plan: Plan, filename: str):
    actions = plan.actions
    action_list = []
    for action in actions:
        action_list.append({'t': action.timestep, 'Agent': action.subject_id, 'type': str(action.action_type),
                           'start_position': action.start_position.tolist(), 'end_position': action.end_position.tolist()})

    export_to_yaml({"actions":action_list}, filename)


def prepend_timestamp(string: str):
    return '{date:%Y-%m-%d_%H-%M-%S}_'.format(date=datetime.datetime.now()) + string
