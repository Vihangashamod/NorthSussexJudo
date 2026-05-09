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

