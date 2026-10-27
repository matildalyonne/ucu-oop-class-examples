from story import PicnicPlan, NatureWalk, TeamQuiz


def main():
    # Test 1: New session
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

    # Test 2: Successful choices
    assert plan.schedule(NatureWalk())
    assert plan.schedule(TeamQuiz("Team quiz"))

    result = plan.summary()
    print("\nTest 2 - Successful choices:")
    print(result)

    assert result["student"] == "Precious"
    assert result["completed_count"] == 2
    assert result["choices"] == ["Nature walk", "Team quiz"]
    assert result["remaining"] == 5

    # Test 3: Refused choice
    refused = plan.schedule(NatureWalk())

    print("\nTest 3 - Refused choice:")
    print("Result:", refused)
    print(plan.summary())

    assert isinstance(refused, str)
    assert plan.summary()["completed_count"] == 2
    assert plan.summary()["choices"] == ["Nature walk", "Team quiz"]
    assert plan.summary()["remaining"] == 5

    print("\nAll summary tests passed!")


if __name__ == "__main__":
    main()