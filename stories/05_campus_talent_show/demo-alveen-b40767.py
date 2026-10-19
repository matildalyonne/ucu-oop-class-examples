"""Demo: LightningDance (ShortDance duration minus 1, minimum 1)."""
from story import TalentShow, audition, ShortDance

class LightningDance(ShortDance):  # Performance -> Dance -> ShortDance -> LightningDance
    def duration(self):
        return max(1, super().duration() - 1)  # Parent's duration minus 1, never below 1

def check(label, expected, actual):
    print(f"  {label}: expected {expected!r}, actual {actual!r} -> "
          f"{'OK' if expected == actual else 'MISMATCH'}")


print("=== Normal case: default 6-minute dance ===")
flash = LightningDance("Flash Crew")           # Dance(6) -> ShortDance 3 -> Lightning 2
audition([flash])                               # existing function, polymorphic describe()
show = TalentShow("Joel", 8)
check("booking message", "MC Joel books Flash Crew dance.", show.book(flash))
check("minutes left", 6, show.clock.remaining)
check("act count", 1, show.act_count)

print("\n=== Boundary case: 1-minute dance (ShortDance would give 0) ===")
tiny = LightningDance("Tiny Crew", minutes=1)   # 1 // 2 = 0, minus 1 = -1 -> clamped to 1
check("duration", 1, tiny.duration())
show2 = TalentShow("Faith", 8)
check("booking message", "MC Faith books Tiny Crew dance.", show2.book(tiny))
check("minutes left", 7, show2.clock.remaining)

print("\n=== Refused case: no time left, state must not change ===")
full = TalentShow("Grace", 0)
before = (full.clock.remaining, full.act_count)
msg = full.book(LightningDance("Late Crew"))
check("refusal message",
      "No slot for Late Crew dance. The timetable has entered the chat.", msg)
check("clock + act count unchanged", before, (full.clock.remaining, full.act_count))