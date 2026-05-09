import os

# Constants - Prices and the details

PLANS = {
    "1": ("Beginner",     25.00),   # 2 sessions per week
    "2": ("Intermediate", 30.00),   # 3 sessions per week
    "3": ("Elite",        35.00),   # 5 sessions per week
}

CATEGORIES = {
    "1": ("Flyweight",          66),
    "2": ("Lightweight",        73),
    "3": ("Light-Middleweight", 81),
    "4": ("Middleweight",       90),
    "5": ("Light-Heavyweight", 100),
    "6": ("Heavyweight",      None),  # no upper limit
}

COACHING_RATE = 9.50   # coaching fee per hour
COMP_FEE      = 22.00  # charge per competition
WEEKS         = 4      # weeks in a month
MAX_COACHING  = 5      # max coaching hours per week

SEPARATOR = "=" * 56   # easier to call than typing the line each time
DASH      = "-" * 56


# ATHLETE CLASS

class Athlete:

    def __init__(self, name, plan, weekly_rate, weight,
                 category, cat_limit, competitions, coaching):
        self.name         = name
        self.plan         = plan
        self.weekly_rate  = weekly_rate   # per week from PLANS
        self.weight       = weight        # current weight in kg
        self.category     = category      # weight category
        self.cat_limit    = cat_limit     # upper kg limit
        self.competitions = competitions  # number of competitions this month
        self.coaching     = coaching      # private coaching hours per week

    def can_compete(self):
        # only Intermediate and Elite are allowed to compete
        return self.plan in ("Intermediate", "Elite")

    def weight_status(self):
        # Heavyweight has no limit - check None before any maths
        if self.cat_limit is None:
            return f"Heavyweight (no upper limit) - current: {self.weight:.1f} kg"
        diff = self.weight - self.cat_limit
        if diff < 0:
            return (f"{self.weight:.1f} kg - {abs(diff):.1f} kg UNDER "
                    f"{self.category} limit ({self.cat_limit} kg)")
        elif diff == 0:
            return (f"{self.weight:.1f} kg - exactly AT "
                    f"{self.category} limit ({self.cat_limit} kg)")
        return (f"{self.weight:.1f} kg - {diff:.1f} kg OVER "
                f"{self.category} limit ({self.cat_limit} kg)")

    def __str__(self):
        return f"{self.name} [{self.plan}]"


# CALCULATIONS

def calc_training(athlete):     # weekly rate x 4 weeks
    return athlete.weekly_rate * WEEKS

def calc_coaching(athlete):     # cap hours at MAX_COACHING then multiply out
    hours = min(athlete.coaching, MAX_COACHING)
    return hours * WEEKS * COACHING_RATE

def calc_competitions(athlete): # Beginners cannot compete
    if not athlete.can_compete():
        return 0.00
    return athlete.competitions * COMP_FEE

def calc_total(athlete):        # sum all three fees
    return calc_training(athlete) + calc_coaching(athlete) + calc_competitions(athlete)

# INPUT VALIDATIONS

def ask_string(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  Field cannot be blank.\n")

def ask_number(prompt, whole=False, minimum=0.0, maximum=None):
    while True:
        try:
            raw   = input(prompt).strip()
            value = int(raw) if whole else float(raw)
            if value < minimum:
                print(f"  Must be {minimum} or above.\n")
            elif maximum is not None and value > maximum:
                print(f"  Must be {maximum} or below.\n")
            else:
                return value
        except ValueError:
            msg = "whole number" if whole else "number (e.g. 74.5)"
            print(f"  Please enter a {msg}.\n")

def ask_yes_no(prompt):    # return True for y, False for n
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"): return True
        if answer in ("n", "no"):  return False
        print("  Type y or n.\n")

def choose_plan():    # display plan menu and return (plan_name, weekly_rate)
    print("\n  Training Plans:")
    print("  " + DASH)
    for key, (name, rate) in PLANS.items():
        print(f"    {key}. {name:<14}  £{rate:.2f}/week")
    print("  " + DASH)
    while True:
        choice = input("  Choose plan (1-3): ").strip()
        if choice in PLANS:
            return PLANS[choice]   # returns (name, weekly_rate)
        print("  Enter 1, 2 or 3.\n")

def choose_category():    # display category menu and return (name, limit_kg)
    print("\n  Weight Categories:")
    print("  " + DASH)
    for key, (name, limit) in CATEGORIES.items():
        info = "No upper limit" if limit is None else f"Up to {limit} kg"
        print(f"    {key}. {name:<24}  {info}")
    print("  " + DASH)
    while True:
        choice = input("  Choose category (1-6): ").strip()
        if choice in CATEGORIES:
            return CATEGORIES[choice]   # returns (name, limit)
        print("  Enter 1 to 6.\n")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# DISPLAY

def print_header():
    print(SEPARATOR)
    print("   NORTH SUSSEX JUDO - Monthly Fee Calculator")
    print("   by AQ Digital Solutions (AQDS)")
    print(SEPARATOR)

def print_report(athlete):    # print full monthly report for one athlete
    t     = calc_training(athlete)
    c     = calc_coaching(athlete)
    x     = calc_competitions(athlete)
    total = t + c + x

    print(f"\n{SEPARATOR}")
    print(f"  Monthly Report - {athlete.name}")
    print(DASH)
    print(f"  Plan   : {athlete.plan}")
    print(f"  Weight : {athlete.weight_status()}")
    print(f"\n  Itemised Costs")
    print(DASH)

    # training - always shown
    print(f"  Training Plan ({athlete.plan})")
    print(f"    £{athlete.weekly_rate:.2f}/week x {WEEKS} weeks"
          f"                  £{t:>7.2f}")

    # coaching - only shown if athlete has any
    if athlete.coaching > 0:
        hrs = min(athlete.coaching, MAX_COACHING)
        print(f"  Private Coaching")
        print(f"    {hrs:.1f} hr/wk x {WEEKS} wks x £{COACHING_RATE:.2f}/hr"
              f"       £{c:>7.2f}")

    # competitions - only shown if eligible and entered any
    if athlete.can_compete() and athlete.competitions > 0:
        print(f"  Competition Entries")
        print(f"    {athlete.competitions} x £{COMP_FEE:.2f}"
              f"                           £{x:>7.2f}")

    print(DASH)
    print(f"  TOTAL DUE THIS MONTH                      £{total:>7.2f}")
    print(SEPARATOR)


def print_summary(athletes):    # one row per athlete and grand total at end
    print(f"\n{DASH}")
    print(f"  {'#':<4}  {'Name':<22}  {'Plan':<14}  {'Total':>8}")
    print(DASH)
    grand = 0.00
    for i, athlete in enumerate(athletes, start=1):
        total  = calc_total(athlete)
        grand += total
        print(f"  {i:<4}  {athlete.name:<22}  {athlete.plan:<14}  £{total:>7.2f}")
    print(DASH)
    print(f"  {'Grand Total':<42}  £{grand:>7.2f}\n")


# EVENT HANDLERS

def handle_register(athletes):    # collect details and register a new athlete
    print(f"\n{DASH}\n  Register New Athlete\n{DASH}")

    while True:
        name = ask_string("  Athlete name: ")
        if any(a.name.lower() == name.lower() for a in athletes):
            print(f"  '{name}' is already registered.\n")
        else:
            break

    plan_name, weekly_rate = choose_plan()
    weight                 = ask_number("\n  Current weight (kg): ", minimum=0.1)
    category, cat_limit    = choose_category()

    if plan_name == "Beginner":
        print("\n  Beginners cannot enter competitions. Set to 0.")
        competitions = 0
    else:
        competitions = ask_number("\n  Competitions this month: ", whole=True)

    coaching = 0.0
    if ask_yes_no("\n  Add private coaching? (y/n): "):
        coaching = ask_number(
            f"  Hours per week (0 - {MAX_COACHING}): ",
            minimum=0.0, maximum=float(MAX_COACHING)
        )

    athletes.append(Athlete(
        name, plan_name, weekly_rate,
        weight, category, cat_limit,
        competitions, coaching
    ))
    print(f"\n  {name} registered successfully.\n")

def handle_report(athletes):    # user picks an athlete and sees their report
    if not athletes:
        print("\n  No athletes registered yet.\n")
        return
    print("\n  Registered athletes:")
    for i, athlete in enumerate(athletes, start=1):
        print(f"    {i}. {athlete}")
    pick = ask_number(
        f"\n  Enter number (1-{len(athletes)}): ",
        whole=True, minimum=1, maximum=len(athletes)
    )
    print_report(athletes[int(pick) - 1])

def handle_summary(athletes):    # show summary table for all athletes
    if not athletes:
        print("\n  No athletes registered yet.\n")
        return
    print_summary(athletes)

def handle_exit():
    if ask_yes_no("\n  Exit the program? (y/n): "):
        print("\n  Thank you for using the North Sussex Judo Calculator.")
        print("  Developed by AQDS\n")
        raise SystemExit


# MAIN LOOP

def main():
    athletes = []   # stores all registered Athlete objects

    handlers = {
        "1": lambda: handle_register(athletes),
        "2": lambda: handle_report(athletes),
        "3": lambda: handle_summary(athletes),
        "4": handle_exit,
    }

    while True:
        clear_screen()
        print_header()
        print(f"\n  Athletes registered: {len(athletes)}\n")
        print("  1. Register a new athlete")
        print("  2. View athlete report")
        print("  3. View all athletes summary")
        print("  4. Exit\n")

        choice = input("  Your choice (1-4): ").strip()

        if choice in handlers:
            handlers[choice]()
            if choice != "4":
                input("\n  Press Enter to continue...")
        else:
            print("\n  Please enter 1, 2, 3 or 4.")
            input("  Press Enter to continue...")


if __name__ == "__main__":
    main()