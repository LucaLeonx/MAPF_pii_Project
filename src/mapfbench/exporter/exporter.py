import csv
from datetime import datetime
from typing import Any

import yaml

from mapfbench.description import Plan, Action, ActionType
from mapfbench.metrics.results import AggregatePlanResults, Results, PlanResults


def export_results_to_csv(results: Results, filename: str, inner_prefix: str = "_plans"):
    export_to_csv([results.results], filename)

    entries = [inner_result.results for inner_result in results.inner_results]
    export_to_csv(entries, filename + inner_prefix)


def scalar(value):
    return isinstance(value, (int, float, str, bool))


def export_to_csv(entries: list[dict[str, Any]], filename: str):
    if len(entries) == 0:
        return

    non_scalar_values = set([])
    for entry in entries:
        for key, value in entry.items():
            if not scalar(value):
                non_scalar_values.add(key)

        for key in non_scalar_values:
            entry.pop(key)

    with open(filename + ".csv", 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, entries[0].keys())
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry)


def export_to_yaml(dictionary: dict[str, Any], filename: str):
    with open(filename, 'w') as f:
        print(dictionary)
        yaml.safe_dump(dictionary, stream=f, indent=4, sort_keys=False)


def export_plans(results: AggregatePlanResults, filename: str):
    dictionary = results.results
    plans = results.inner_results
    dictionary.update({"Plans": []})

    for plan in plans:
        plan_dict = plan.results
        plan_dict.update({"Actions": convert_actions_to_dict(plan.data.actions)})
        dictionary["Plans"].append(plan_dict)

    with open(filename + ".yaml", "w") as file:
        yaml.safe_dump(dictionary, file, indent=4, sort_keys=False)


def convert_actions_to_dict(actions: list[Action]):

    action_list = []
    for action in actions:
        action_list.append({'Timestep': action.timestep, 'Agent': action.subject_id,
                            'Type': ActionType(action.action_type).name,
                            'Start position': str(action.start_position.tolist()),
                            'End position': str(action.end_position.tolist())})

    return action_list


def export_plan_results(plan: Plan, filename: str):
    actions = plan.actions
    action_list = []
    for action in actions:
        action_list.append({'t': action.timestep, 'Agent': action.subject_id, 'type': str(action.action_type),
                            'start_position': action.start_position.tolist(),
                            'end_position': action.end_position.tolist()})

    export_to_yaml({"actions": action_list}, filename)


def prepend_timestamp(string: str):
    return '{date:%Y-%m-%d_%H-%M-%S}_'.format(date=datetime.datetime.now()) + string
