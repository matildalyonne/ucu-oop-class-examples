"""Demo: Extension 4 - cancel_last() in TalentShow.

Run from the repository root:
    py -3 stories/05_campus_talent_show/demo_clancy_B34915.py

Shows the normal case (cancel a booked act) and the empty case (nothing to
cancel), plus a refused booking so the clock stays honest.
"""
from story import Dance, Poetry, TalentShow


def check(label, expected, actual):
    print(f"  {label}: expected {expected!r}, actual {actual!r} -> "
          f"{'OK' if expected == actual else 'MISMATCH'}")


print("=== Normal case: cancel the most recent booking ===")
show = TalentShow("Joel", 8)
show.book(Dance("Mukono Movers"))                 # 6 minutes.
show.book(Poetry("Achen's spoken word"))          # 4 minutes won't fit, refused.
show.book(Dance("Brief Crew", minutes=2))         # 2 minutes fits.
check("clock before cancel", 0, show.clock.remaining)
check("act count before cancel", 2, show.act_count)
check("cancel_last() returned", True, show.cancel_last())
check("clock after cancel", 2, show.clock.remaining)
check("act count after cancel", 1, show.act_count)

print("\n=== Boundary case: nothing booked, cancel must refuse ===")
fresh = TalentShow("Faith", 6)
before = (fresh.clock.remaining, fresh.act_count)
check("cancel_last() returned", False, fresh.cancel_last())
check("clock and act count unchanged", before,
      (fresh.clock.remaining, fresh.act_count))

print("\n=== Refused booking does not change the clock ===")
full = TalentShow("Grace", 1)
check("refused message",
      "No slot for Long Crew dance. The timetable has entered the chat.",
      full.book(Dance("Long Crew", minutes=2)))
check("clock and act count unchanged", (1, 0),
      (full.clock.remaining, full.act_count))
check("cancel_last() on an empty show", False, full.cancel_last())
