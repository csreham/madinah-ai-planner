from agents.planner import PlannerAgent


def main():

    print("=" * 60)
    print("        MADINAH TOURISM AI AGENT")
    print("=" * 60)

    user_request = input(
        "\nEnter your trip request: "
    )

    planner = PlannerAgent()

    try:

        result = planner.run(
            user_request
        )

    except Exception as e:

        print("\nERROR:")
        print(e)

        return

    if not result:

        print("\nNo result generated.")

        return

    # ==================================================
    # BASIC INFORMATION
    # ==================================================

    print("\n" + "=" * 60)
    print("TRIP INFORMATION")
    print("=" * 60)

    print(
        f"City: {result.get('city')}"
    )

    print(
        f"Days: {result.get('days')}"
    )

    # ==================================================
    # SCHEDULE
    # ==================================================

    print("\n" + "=" * 60)
    print("TRIP SCHEDULE")
    print("=" * 60)

    schedule_result = result.get(
        "schedule",
        {}
    )

    # إذا ScheduleAgent يرجع
    # {"schedule": {...}}
    if isinstance(
        schedule_result,
        dict
    ) and "schedule" in schedule_result:

        schedule = schedule_result.get(
            "schedule",
            {}
        )

    else:

        schedule = schedule_result

    if isinstance(schedule, dict):

        for day, activities in schedule.items():

            print(
                f"\n{day}"
            )

            print("-" * 50)

            if not isinstance(
                activities,
                list
            ):

                print(activities)

                continue

            for i, activity in enumerate(
                activities,
                start=1
            ):

                if isinstance(
                    activity,
                    dict
                ):

                    print(
                        f"{i}. "
                        f"{activity.get('name', 'Unknown')}"
                    )

                else:

                    print(
                        f"{i}. {activity}"
                    )

    else:

        print(schedule)

    # ==================================================
    # TRANSPORTATION
    # ==================================================

    transportation = result.get(
        "transportation",
        {}
    )

    print("\n" + "=" * 60)
    print("TRANSPORTATION")
    print("=" * 60)

    if transportation:

        for day, data in transportation.items():

            print(
                f"\n{day}"
            )

            if not isinstance(
                data,
                dict
            ):
                continue

            print(
                f"Trips: "
                f"{data.get('number_of_trips', 0)}"
            )

            print(
                f"Distance: "
                f"{data.get('total_distance_km', 0)} km"
            )

            print(
                f"Estimated cost: "
                f"{data.get('total_estimated_cost', 0)} SAR"
            )

            routes = data.get(
                "routes",
                []
            )

            for route in routes:

                print(
                    f"{route.get('from')} "
                    f"→ "
                    f"{route.get('to')}"
                )

                print(
                    f"  {route.get('distance_km')} km | "
                    f"{route.get('transport')} | "
                    f"{route.get('estimated_cost')} SAR"
                )

    else:

        print(
            "No transportation data."
        )

    # ==================================================
    # BUDGET
    # ==================================================

    budget = result.get(
        "budget",
        {}
    )

    print("\n" + "=" * 60)
    print("TRIP BUDGET")
    print("=" * 60)

    if budget:

        hotel = budget.get(
            "hotel",
            {}
        )

        restaurants = budget.get(
            "restaurants",
            {}
        )

        transportation_budget = budget.get(
            "transportation",
            {}
        )

        print(
            f"Hotel: "
            f"{hotel.get('name')} | "
            f"{hotel.get('cost', 0)} SAR"
        )

        print(
            f"Restaurants: "
            f"{restaurants.get('cost', 0)} SAR"
        )

        print(
            f"Transportation: "
            f"{transportation_budget.get('cost', 0)} SAR"
        )

        print("-" * 60)

        print(
            f"TOTAL TRIP COST: "
            f"{budget.get('total_cost', 0)} SAR"
        )

    else:

        print(
            "No budget data."
        )

    # ==================================================
    # END
    # ==================================================

    print("\n" + "=" * 60)
    print("TRIP GENERATION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":

    main()