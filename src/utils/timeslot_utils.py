def get_time_penalty(time_slot: str) -> float:
    start_time = time_slot.split()[1].split("-")[0]
    hours, minutes = map(float, start_time.split(":"))
    time_value = hours + minutes / 60

    return time_value - 9.0

def get_time_slot_length(time_slot) -> float:
    time_interval = time_slot.split()[1]
    start_time = time_interval.split("-")[0]
    end_time = time_interval.split("-")[1]

    start_h, start_m = map(float, start_time.split(":"))
    end_h, end_m = map(float, end_time.split(":"))

    return (end_h + end_m / 60) - (start_h + start_m / 60)