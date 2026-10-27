from story import PicnicPlan, TeamQuiz, GroupPhoto, ShortWalk, NatureWalk


class ZeroChoice:  # duck-typed, costs nothing
    name = "Free toast"
    def duration(self):
        return 0


class NegativeChoice:  # broken choice with an invalid requirement
    name = "Broken choice"
    def duration(self):
        return -5


def show(label, plan, result):
    print(f"{label}: returned {result}; remaining {plan.clock.remaining}, "
          f"completed {plan.completed_count}")


# Normal: 15 + 5 + 10 = 30 fits in 60.
plan = PicnicPlan("Faith", 60)
print("Before:", plan.clock.remaining, plan.completed_count)
result = plan.complete_bundle([TeamQuiz("Team quiz"), GroupPhoto(), ShortWalk()])
show("Normal bundle", plan, result)
assert result is True and plan.clock.remaining == 30 and plan.completed_count == 3
assert [e["cost"] for e in plan._entries] == [15, 5, 10]

# Boundary: total exactly equals what is left (30).
result = plan.complete_bundle([NatureWalk(2), ShortWalk()])  # 20 + 10
show("Exact fit", plan, result)
assert result is True and plan.clock.remaining == 0 and plan.completed_count == 5

# Refusal: too big. Nothing spent, nothing recorded (first item alone would fit).
plan = PicnicPlan("Alex", 30)
result = plan.complete_bundle([TeamQuiz("Team quiz"), NatureWalk(2)])  # 15 + 20 = 35
show("Too big", plan, result)
assert result is False and plan.clock.remaining == 30 and plan.completed_count == 0

# Refusal: empty list and a negative requirement.
result = plan.complete_bundle([])
show("Empty list", plan, result)
assert result is False and plan.completed_count == 0
result = plan.complete_bundle([GroupPhoto(), NegativeChoice()])
show("Negative requirement", plan, result)
assert result is False and plan.clock.remaining == 30 and plan.completed_count == 0

# Zero-cost bundle on a zero-resource session.
plan = PicnicPlan("Sam", 0)
result = plan.complete_bundle([ZeroChoice(), ZeroChoice()])
show("Zero-cost bundle", plan, result)
assert result is True and plan.clock.remaining == 0 and plan.completed_count == 2

print("All demo checks passed.")