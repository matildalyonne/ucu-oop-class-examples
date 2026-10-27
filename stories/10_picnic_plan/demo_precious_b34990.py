from story import PicnicPlan, NatureWalk, TeamQuiz, GroupPhoto


def main():
    # Test 1: A new session should have an empty summary.
    plan = PicnicPlan("Precious", 40)

    initial = plan.summary()
    print("Test 1 - New session:")
    print(initial)

    assert initial == {
        "student": "Precious",
        "remaining": 40,
        "completed_count": 0,
        "choices": [],
    }

    # Test 2: Successful choices should appear in order.
    assert plan.schedule(NatureWalk())
    assert plan.schedule(TeamQuiz("Team quiz"))

    result = plan.summary()
    print("\nTest 2 - After successful choices:")
    print(result)

    assert result["student"] == "Precious"
    assert result["completed_count"] == 2
    assert result["choices"] == [NatureWalk(), TeamQuiz("Team quiz")]
    assert result["remaining"] == 15

    # Test 3: A refused choice must not appear in the summary.
    refused = plan.schedule(GroupPhoto())

    print("\nTest 3 - Refused choice:")
    print("Accepted:", refused)
    print(plan.summary())

    assert refused is False
    assert plan.summary()["completed_count"] == 2
    assert plan.summary()["choices"] == ["Nature walk", "Team quiz"]

    print("\nAll summary tests passed!")


if __name__ == "__main__":
    main()