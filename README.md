North Sussex Judo – Monthly Training Fee Calculator

Unit 1: Programming | BTEC HND Computing (Software Engineering)

AQ Digital Solutions (AQDS) 

Academic Year: 2024/25

Name: Vihanga Shamod Hewanayake

ID: 521546


This CLI program is:

A command-line Python program built for North Sussex Judo Club.

This calculates and displays monthly training fees for each athlete based on their training plan, private coaching hours, competitions entered and weight category.


How to Run

python3 main.py

Requires Python 3.8 or above. No extra libraries needed.


Pricing

PlanSessionsWeekly FeeMonthly FeeBeginner2 per week£25.00£100.00Intermediate3 per week£30.00£120.00Elite5 per week£35.00£140.00


Private coaching: £9.50/hr, max 5 hrs/week
Competition entry: £22.00 each (Intermediate and Elite only)
Month = 4 weeks



Weight Categories

CategoryUpper LimitFlyweight66 kgLightweight73 kgLight-Middleweight81 kgMiddleweight90 kgLight-Heavyweight100 kgHeavyweightNo limit


Features


Register athletes with name, plan, weight and category
Calculate monthly fees with full itemised breakdown
Compare current weight to competition category limit
View summary of all athletes with grand total
Handles all invalid input with re-prompting
Beginners cannot enter competitions (enforced automatically)



Programming Paradigms Used

ParadigmWhere in the CodeObject-OrientedAthlete class – can_compete(), weight_status()Proceduralcalc_*, ask_*, choose_*, print_* functionsEvent-Drivenmain() – dispatch table + while True loop


Code Structure

main.py (296 lines)
├── Constants        – PLANS, CATEGORIES, COACHING_RATE, COMP_FEE, WEEKS, MAX_COACHING
├── Athlete class    – OOP: stores all athlete data and behaviour
├── calc_* functions – Procedural: fee calculations
├── ask_* functions  – Procedural: input validation
├── choose_*         – Procedural: menu selection helpers
├── print_*          – Procedural: display functions
├── handle_*         – Event-Driven: one handler per menu option
└── main()           – Event-Driven: dispatch table + event loop


Development History

This project was built in 6 Git commits, one per development stage:

HashCommit Message124d0f3Added Event handlers and main loopd7b0beaAdded Display functions3a64ecaAdded input validationsc9fec1fAdded calculation functions75eb17fAdded constants and Athlete classes3689cafInitial commit-README


Coding Standards

This project follows PEP 8 (Python Style Guide):


snake_case for all function and variable names
UPPER_CASE for all constants
Descriptive names – calc_training() not ct()
Single responsibility – each function does one thing
Lines kept within ~79 characters