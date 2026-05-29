from datetime import date, datetime, time, timedelta


def is_past_date(selected_date: date, *, today: date | None = None) -> bool:
    reference = today or date.today()
    return selected_date < reference


def _parse_time(value: str | time) -> time:
    if isinstance(value, time):
        return value
    return time.fromisoformat(value)


def availability_for_date(rows: list[dict], selected_date: date) -> list[dict]:
    day = selected_date.weekday()
    return [row for row in rows if row.get("day_of_week") == day]


def build_slot_options(
    rows: list[dict],
    *,
    selected_date: date | None = None,
    duration_minutes: int = 0,
    step_minutes: int = 30,
    now: datetime | None = None,
) -> list[dict]:
    slots = []
    seen = set()
    slot_date = selected_date or date.today()
    should_filter_past = selected_date is not None
    reference_now = now or datetime.now()
    if reference_now.tzinfo is not None:
        reference_now = reference_now.replace(tzinfo=None)

    for row in rows:
        current = datetime.combine(slot_date, _parse_time(row["start_time"]))
        end = datetime.combine(slot_date, _parse_time(row["end_time"]))

        duration = timedelta(minutes=duration_minutes or step_minutes)
        while current + duration <= end:
            slot_time = current.time().replace(second=0, microsecond=0)
            is_future_slot = (
                not should_filter_past
                or slot_date != reference_now.date()
                or current > reference_now
            )
            if is_future_slot and slot_time not in seen:
                slots.append({"label": slot_time.strftime("%H:%M"), "time": slot_time})
                seen.add(slot_time)
            current += timedelta(minutes=step_minutes)

    return sorted(slots, key=lambda item: item["time"])


def combine_date_time(selected_date: date, selected_time: time) -> str:
    return datetime.combine(selected_date, selected_time).replace(microsecond=0).isoformat()
