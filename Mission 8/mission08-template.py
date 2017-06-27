#
# CS1010X --- Programming Methodology
#
# Mission 8 Template
#
# Note that written answers are commented out to allow us to run your
# code easily while grading your problem set.

from ippt import *
import csv


##########
# Task 1 #
##########

# Function read_csv has been given to help you read the csv file.
# The function returns a tuple of tuples containing rows in the csv
# file and its entries.

# Alternatively, you may use your own method.

def read_csv(csvfilename):
    rows = ()
    with open(csvfilename) as csvfile:
        file_reader = csv.reader(csvfile)
        for row in file_reader:
            rows += (tuple(row), )
    return rows

def read_data(filename):
    rows = read_csv(filename)
    data = tuple([tuple([int(x) for x in y[1:]]) for y in rows[1:]])
    age_title = tuple([int(x[0]) for x in rows[1:]])
    rep_title = tuple([int(x) for x in rows[0][1:]])
    return create_table(data, age_title, rep_title)

pushup_table = read_data("pushup.csv")
situp_table = read_data("situp.csv")
run_table = read_data("run.csv")

ippt_table = make_ippt_table(pushup_table, situp_table, run_table)

print("## Q1 ##")
##Situp score of a 24 year old who did 10 situps.
#print(access_cell(situp_table, 24, 10))    # 0

# Pushup score of a 18 year old who did 30 pushups.
#print(access_cell(pushup_table, 18, 30))   # 16

# Run score of a 30 year old who ran 12 minutes (720 seconds)
#print(access_cell(run_table, 30, 720))     # 35

# Since our run csv file does not have data for 725 seconds, we should
# get None if we tried to access that cell
#print(access_cell(run_table, 30, 725))     # None



##########
# Task 2 #
##########
#assumption: score brackets multiple of 10s

def pushup_score(pushup_table, age, pushup):
    if pushup > 60: pushup = 60
    if pushup < 1: pushup = 1
    return access_cell(pushup_table, age, pushup)

def situp_score(situp_table, age, situp):
    if situp > 60: situp = 60
    if situp < 1: situp = 1
    return access_cell(situp_table, age, situp)

def run_score(run_table, age, run):
    if run > 1100: run = 1100
    if run < 510: run = 510
    i = run
    while access_cell(run_table, age, i) == None:
        i += 1
    return access_cell(run_table, age, i)

# print("## Q2 ##")
#print(pushup_score(pushup_table, 18, 61))   # 25
#print(pushup_score(pushup_table, 18, 70))   # 25
#print(situp_score(situp_table, 24, 0))      # 0

#print(run_score(run_table, 30, 720))        # 35
#print(run_score(run_table, 30, 725))        # 35
#print(run_score(run_table, 30, 735))        # 34
#print(run_score(run_table, 30, 500))        # 50
#print(run_score(run_table, 30, 1300))       # 0


##########
# Task 3 #
##########

def ippt_award(score):
    if score > 80:
        return 'G'
    elif score > 70:
        return 'S'
    elif score > 60:
        return 'P$'
    elif score > 50:
        return 'P'
    else:
        return 'F'

##print("## Q3 ##")
##print(ippt_award(50))     # F
##print(ippt_award(51))     # P
##print(ippt_award(61))     # P$
##print(ippt_award(71))     # S
##print(ippt_award(81))     # G


##########
# Task 4 #
##########

def ippt_results(ippt_table, age, pushup, situp, run):
    p_score = pushup_score(get_pushup_table(ippt_table), age, pushup)
    s_score = situp_score(get_situp_table(ippt_table), age, situp)
    r_score = run_score(get_run_table(ippt_table), age, run)
    total = p_score + s_score + r_score
    return (total, ippt_award(total))

##print("## Q4 ##")
##print(ippt_results(ippt_table, 25, 30, 25, 820))      # (53, 'P')
##print(ippt_results(ippt_table, 28, 56, 60, 530))      # (99, 'G')
##print(ippt_results(ippt_table, 38, 18, 16, 950))      # (34, 'F')
##print(ippt_results(ippt_table, 25, 34, 35, 817))      # (61, 'P$')
##print(ippt_results(ippt_table, 60, 70, 65, 450))      # (100, 'G')


##########
# Task 5 #
##########
def make_training_program(rate_pushup, rate_situp, rate_run):
    def training_program(ippt_table, age, pushup, situp, run, days):
        improved_p = pushup + days // rate_pushup
        improved_s = situp + days // rate_situp
        improved_r = run - days // rate_run
        score = ippt_results(ippt_table, age, improved_p, improved_s, improved_r)
        return (improved_p, improved_s, improved_r, score)
    return training_program

#print("## Q5 ##")
tp = make_training_program(7, 3, 10)
#print(tp(ippt_table, 25, 30, 25, 820, 30))        # (34, 35, 817, (61, 'P$'))

##########
# Bonus  #
##########

def make_tp_bonus(rate_pushup, rate_situp, rate_run):
    def tp_bonus(ippt_table, age, pushup, situp, run, days):
        lst = [[pushup, rate_pushup, 0], [situp, rate_situp, 1], [run, rate_run, 2]]
        # sort by smallest
        srt = sorted(lst, key=lambda x: x[1])
        i = 0
        while days > 0 and i < len(lst):
              stn = srt[i]
              if stn[2] == 3: #if run
                  stn[0] = stn[0] - days // stn[1]
              else:
                  stn[0] = stn[0] + days // stn[1]
              days = days % stn[1]
              i += 1
        pushup, situp, run = lst[0][0], lst[1][0], lst[2][0]
        score = ippt_results(ippt_table, age, pushup, situp, run)
        return (pushup, situp, run, score)
    return tp_bonus

tp_bonus = make_tp_bonus(7, 3, 10)

# Note: Your solution might not match the sample output exactly. There might
# be difference in the situp, pushup, and run count, but your IPPT result
# should be the same

#print(ippt_results(ippt_table, 25, 20, 30, 800))
print(tp_bonus(ippt_table, 25, 20, 30, 800, 30))      # (20, 40, 800, (58, 'P'))
print(tp_bonus(ippt_table, 25, 20, 30, 800, 2))       # (20, 30, 800, (52, 'P'))
