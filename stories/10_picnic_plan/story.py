"""The Mabira Picnic Plan — a complete Weeks 1–6 story.
Run: python3 story.py. All numbers and events are invented for learning.
"""
from abc import ABC, abstractmethod


# ACT 1: The resource owns its value and the rules for changing it.
class PicnicClock:
    def __init__(self, amount):
        self.remaining = amount  # Starting values go through the setter too.

    @property
    def remaining(self):
        return self.__remaining  # Name mangling, not a security lock.

    @remaining.setter
    def remaining(self, amount):
        if amount < 0:
            raise ValueError("Remaining minutes cannot be negative.")
        self.__remaining = amount

    def use(self, amount):
        if amount <= 0 or amount > self.remaining:
            return False  # Refuse before changing state.
        self.remaining = self.remaining - amount
        return True

    def add_more(self, amount):
        if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
            return False
        self.remaining = self.remaining + amount
        return True


# ACT 2: The abstract family says what every concrete choice must provide.
class PicnicActivity(ABC):
    unit = "minutes"  # Class attribute; every instance has its own name.

    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"{self.name} needs {self.duration():,} {self.unit}."

    @abstractmethod
    def duration(self):
        pass


class NatureWalk(PicnicActivity):
    def __init__(self, stops=2):
        if not isinstance(stops, int) or isinstance(stops, bool) or stops <= 0:
            raise ValueError("Stops must be a positive whole number.")
        super().__init__("Nature walk")
        self.stops = stops

    def duration(self):
        return self.stops * 10


class TeamQuiz(PicnicActivity):  # Siblings show hierarchical inheritance.
    def duration(self):
        return 15


class ShortWalk(NatureWalk):  # A third level in the same family.
    def __init__(self, stops=2):
        super().__init__(stops)
        self.name = "Short nature walk"

    def duration(self):
        return super().duration() // 2  # Reuse, then specialise, the parent's calculation.


# ACT 3: Multiple inheritance adds a small descriptive ability.
class PicnicHype:
    def describe(self):
        return f"The picnic team is ready! {super().describe()}"


class FeaturedWalk(PicnicHype, ShortWalk):
    pass  # The full hierarchy combines multiple and multilevel inheritance.


class GroupPhoto:  # No shared parent: callers use its matching behaviour.
    name = "Group photo"

    def duration(self):
        return 5

    def describe(self):
        return "Group photo: 5 minutes in this classroom model."


class ThankYouCircle:
    def __init__(self):
        self.name = "Thank-you circle"

    def duration(self):
        return 0

    def describe(self):
        return f"{self.name}: a moment to thank everyone."


# ACT 4: The coordinator HAS-A resource, and USES-A chosen object.
class PicnicPlan:
    def __init__(self, student, amount):
        self.student = student
        self.clock = PicnicClock(amount)  # Owned part: composition.
        self._entries = []  # Internal by convention; fresh for every instance.

    @property
    def completed_count(self):
        return len(self._entries) 
    def summary(self):
        return {
            "student": self.student,
            "remaining": self.clock.remaining,
            "completed_count": self.completed_count,
            "choices": [entry["choice"].name for entry in self._entries],
        }
     # Read-only: it reflects actual history.

    def schedule(self, choice):
        needed = choice.duration()  # Each choice knows its own calculation.
        if needed < 0:
            return "Invalid negative requirement. Nothing recorded."
        if needed == 0 or self.clock.use(needed):
            # Save the quoted cost now: later edits to the choice cannot change it.
            self._entries.append({"choice": choice, "cost": needed})
            return f"{self.student} completes {choice.name}: {needed:,} minutes."
        return f"Not enough minutes for {choice.name}. Nothing recorded."
    
    def complete_bundle(self, choices):
        """Record every choice or none of them."""
        if not choices:
            return False
        # Ask each choice once, so the quote we check is the quote we record.
        costs = [choice.duration() for choice in choices]
        if any(cost < 0 for cost in costs):
            return False
        total = sum(costs)
        # clock.use() refuses 0, so a zero-cost bundle skips it (same as schedule()).
        if total > 0 and not self.clock.use(total):
            return False
        for choice, cost in zip(choices, costs):
            self._entries.append({"choice": choice, "cost": cost})
        return True


def show_choices(choices):
    for choice in choices:
        print(choice.describe())  # Same call, different implementations.


# ACT 5: A complete story, including a refusal and independent object state.
def main():
    print("=== THE MABIRA PICNIC PLAN ===")
    print("Faith is planning a fictional student picnic near Mabira. Activities must finish before the group leaves.")
    choices = [NatureWalk(), TeamQuiz("Team quiz"),
               FeaturedWalk(), GroupPhoto()]
    show_choices(choices)  # Includes an unrelated duck-typed guest.
    session = PicnicPlan("Faith", 40)
    other = PicnicPlan("Alex", 40)
    print(session.schedule(choices[2]))
    print(session.schedule(choices[0]))
    print(session.schedule(choices[0]))  # Eventually the same request will not fit.
    print(session.schedule(choices[3]))
    print(other.schedule(choices[1]))
    print(f"{session.student}: {session.clock.remaining:,} minutes; completed: {session.completed_count}")
    print(f"{other.student}: {other.clock.remaining:,} minutes; completed: {other.completed_count}")
    print("MRO (method lookup order):")
    for parent in FeaturedWalk.__mro__:
        print(parent.__name__)
    print("Ending: The group has enjoyed the picnic and can leave on time.")

    print("=== FOUNDATION 3: A GUEST FROM A DIFFERENT FAMILY ===")
    guest = ThankYouCircle()
    show_choices([guest])
    zero_resource_session = PicnicPlan("Mulembeke", 0)
    print(
        f"Before: {zero_resource_session.clock.remaining} minutes; "
        f"completed: {zero_resource_session.completed_count}"
    )
    print(zero_resource_session.schedule(guest))
    print(
        f"After guest: {zero_resource_session.clock.remaining} minutes; "
        f"completed: {zero_resource_session.completed_count}"
    )
    print(zero_resource_session.schedule(GroupPhoto()))
    print(
        f"After refusal: {zero_resource_session.clock.remaining} minutes; "
        f"completed: {zero_resource_session.completed_count}"
    )


if __name__ == "__main__":
    main()
