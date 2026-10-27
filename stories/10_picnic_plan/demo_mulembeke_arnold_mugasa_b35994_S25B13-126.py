"""Demonstrate Foundation 3: a zero-cost guest from another family."""
from story import GroupPhoto, PicnicPlan, ThankYouCircle, show_choices


guest = ThankYouCircle()
show_choices([guest])

session = PicnicPlan("Mulembeke", 10)
print(f"Before: {session.clock.remaining} minutes; completed: {session.completed_count}")
print(session.schedule(guest))
print(f"After guest: {session.clock.remaining} minutes; completed: {session.completed_count}")

refused_choice = GroupPhoto()
print(session.schedule(refused_choice))
print(f"After refusal: {session.clock.remaining} minutes; completed: {session.completed_count}")

