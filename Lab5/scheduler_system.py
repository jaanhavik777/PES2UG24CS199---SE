"""Meeting-room scheduler: books rooms, allocates equipment, logs conflicts."""
import itertools
import json
from collections import Counter
from datetime import datetime

# Global state
reservations = {}
equipment_pool = {"projector": 2, "microphone": 4, "webcam": 1}
conflicts = []
reservation_ids = itertools.count(1)


def parse_slot(time_slot):
    """Return (start, end) hours from a slot like '09-11'.

    Raises ValueError if the slot is malformed or start is not before end.
    """
    if not isinstance(time_slot, str):
        raise ValueError(f"Slot must be text like '09-11', got {time_slot!r}")
    parts = time_slot.split("-")
    if len(parts) != 2 or not all(p.isdigit() for p in parts):
        raise ValueError(f"Slot must look like '09-11', got {time_slot!r}")
    start, end = int(parts[0]), int(parts[1])
    if not 0 <= start < end <= 24:
        raise ValueError(
            f"Slot {time_slot!r} must have 0 <= start < end <= 24")
    return start, end


def slot_hours(time_slot):
    """Return the length of a slot in hours."""
    start, end = parse_slot(time_slot)
    return end - start


def overlaps(slot_a, slot_b):
    """Return True if two slots share any time."""
    start_a, end_a = parse_slot(slot_a)
    start_b, end_b = parse_slot(slot_b)
    return start_a < end_b and start_b < end_a


def schedule_room(room_id, time_slot, equipment_list=None):
    """Book a room and its equipment; return the reservation id.

    Raises ValueError if the slot is invalid, the room is already booked,
    or the equipment is unknown or out of stock. Nothing is changed when
    a booking is rejected.
    """
    if equipment_list is None:
        equipment_list = []
    parse_slot(time_slot)
    for booking in reservations.values():
        if booking["room"] == room_id and overlaps(booking["slot"], time_slot):
            conflicts.append(f"{room_id} double-booked at {time_slot}")
            raise ValueError(f"{room_id} is already booked at {time_slot}")
    for item, needed in Counter(equipment_list).items():
        if item not in equipment_pool:
            raise ValueError(f"Unknown equipment: {item!r}")
        if equipment_pool[item] < needed:
            raise ValueError(f"Not enough {item} available")
    for item in equipment_list:
        equipment_pool[item] -= 1
    reservation_id = next(reservation_ids)
    reservations[reservation_id] = {
        "room": room_id,
        "slot": time_slot,
        "equipment": list(equipment_list),
    }
    return reservation_id


def cancel_reservation(reservation_id):
    """Cancel a reservation and return its equipment to the pool."""
    if reservation_id not in reservations:
        print(f"No reservation {reservation_id} to cancel")
        return
    for item in reservations[reservation_id]["equipment"]:
        equipment_pool[item] += 1
    del reservations[reservation_id]


def export_schedule(file="schedule.json"):
    """Write all reservations to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(reservations, f)


def log_conflicts(file="conflicts.log"):
    """Append conflicts to the log file, then print the log."""
    with open(file, "a", encoding="utf-8") as f:
        for conflict in conflicts:
            f.write(f"{datetime.now()} {conflict}\n")
    with open(file, encoding="utf-8") as f:
        print(f.read())


def try_schedule(room_id, time_slot, equipment_list=None):
    """Book a room, printing the reason instead of crashing on failure."""
    try:
        return schedule_room(room_id, time_slot, equipment_list)
    except ValueError as err:
        print(f"Booking rejected: {err}")
        return None


def main():
    """Run the demo bookings and export the results."""
    try_schedule("Board-1", "09-11")
    try_schedule("Board-1", "09-11")
    huddle = try_schedule("Huddle-3", "14-12")
    try_schedule("Huddle-3", 1530)
    if huddle is not None:
        print("Slot length:", slot_hours(reservations[huddle]["slot"]))
    cancel_reservation(77)
    slot = input("Slot for Board-2, like 10-12 (Enter for 10-12): ") or "10-12"
    try_schedule("Board-2", slot, ["projector", "webcam"])
    export_schedule()
    log_conflicts()
    print("Equipment left:", equipment_pool)
    print("Reservations:", reservations)


if __name__ == "__main__":
    main()
