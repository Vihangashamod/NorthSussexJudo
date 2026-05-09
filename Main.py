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

