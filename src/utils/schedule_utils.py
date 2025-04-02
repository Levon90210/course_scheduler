import json
from tabulate import tabulate

def save_schedule(schedule, path):
    with open(path, 'w') as f:
        output = {
            "schedule": [
                {
                    "course": entry["course"],
                    "time_slot": entry["time_slot"],
                    "instructor": entry["instructor"]
                }
                for entry in schedule
            ]
        }
        json.dump(output, f, indent=2)

def print_schedule_table(schedule):
    time_slots = sorted({entry["time_slot"].split(' ')[1] for entry in schedule})
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    table = []
    for slot in time_slots:
        row = [slot]
        for day in days:
            entry = next(
                (f"{c['course']} ({c['instructor']})"
                 for c in schedule
                 if c['time_slot'] == f"{day} {slot}"),
                "Free"
            )
            row.append(entry)
        table.append(row)

    headers = ["Time"] + days
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))