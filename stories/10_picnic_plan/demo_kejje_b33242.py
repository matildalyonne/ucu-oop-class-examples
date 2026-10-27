"""Demo tests for PicnicClock.add_more.

Run this file with:
    python demo.py

Place demo.py in the same folder as story.py.
"""

from story import PicnicClock


def check(description, condition):
    status = "PASS" if condition else "FAIL"
    print(f"{status}: {description}")
    if not condition:
        raise AssertionError(description)


def main():
    clock = PicnicClock(40)

    # A positive whole number should be added successfully.
    check("add_more(10) returns True", clock.add_more(10) is True)
    check("remaining increases from 40 to 50", clock.remaining == 50)

    # Invalid inputs must be refused without changing remaining.
    invalid_amounts = [0, -5, 2.5, True, False]
    for amount in invalid_amounts:
        before = clock.remaining
        result = clock.add_more(amount)
        check(f"add_more({amount!r}) returns False", result is False)
        check(f"remaining stays {before} after refusing {amount!r}",
              clock.remaining == before)

    # A positive whole number should still work after refused requests.
    check("add_more(3) returns True", clock.add_more(3) is True)
    check("remaining increases from 50 to 53", clock.remaining == 53)

    print("\nAll add_more tests passed.")


if __name__ == "__main__":
    main()
