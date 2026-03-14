from datetime import datetime

from universal_multi_agent_sim.scheduler import EventScheduler


def test_scheduler_returns_events_for_step():
    scheduler = EventScheduler(start_time=datetime.fromisoformat("2026-03-12T09:00:00"), step_minutes=15)
    scheduler.schedule(2, {"pressure": 0.4})
    assert scheduler.pop_step_events(1) == []
    assert scheduler.pop_step_events(2) == [{"pressure": 0.4}]


def test_scheduler_timestamp_for_step_is_incremental():
    scheduler = EventScheduler(start_time=datetime.fromisoformat("2026-03-12T09:00:00"), step_minutes=15)
    assert scheduler.timestamp_for_step(2) == "2026-03-12T09:30:00"


def test_scheduler_pop_clears_events_after_reading():
    scheduler = EventScheduler(start_time=datetime.fromisoformat("2026-03-12T09:00:00"), step_minutes=10)
    scheduler.schedule(1, {"pressure": 0.2, "policy_delta": 0.1})
    scheduler.schedule(1, {"pressure": 0.1, "macro_delta": 0.3})

    first_read = scheduler.pop_step_events(1)
    second_read = scheduler.pop_step_events(1)

    assert len(first_read) == 2
    assert second_read == []
