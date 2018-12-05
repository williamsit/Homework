import os
import csv

count_of_months = 0
sum_of_prof_loss = 0
sum_of_change = 0
count_of_prof_loss = 0
count_of_diff = -1
list_of_each_prof_loss = []
list_of_change_prof_loss = [0,]
greatest_increase_prof = [0]
greatest_decrease_loss = [0]
greatest_increase_prof_date = []
greatest_decrease_loss_date = []
each_month = []
each_profit_loss = []

pybank_loc = os.path.join("Resources", "budget_data.csv")
with open (pybank_loc, newline="") as pybank_open:
    pybank_reader = csv.reader(pybank_open, delimiter = ",")
    pybank_header = next(pybank_reader)

    #For total number of months and net profit/loss
    for eachline in pybank_reader:
        each_month.append(eachline[0])
        each_profit_loss.append(eachline[1])
        count_of_months += 1
        sum_of_prof_loss += float(eachline[1])
        list_of_each_prof_loss.append(float(eachline[1]))

    format_net = "${:,.2f}".format(sum_of_prof_loss)

    #For average change in profit/loss
    for each_value in list_of_each_prof_loss:
        count_of_prof_loss += 1
        if count_of_prof_loss < count_of_months:
            change = -each_value + list_of_each_prof_loss[count_of_prof_loss]
            list_of_change_prof_loss.append(change)

    #For greatest increase in profits/greatest decrease in losses
    for diff in list_of_change_prof_loss:
        count_of_diff += 1
        sum_of_change += diff
        if count_of_diff < count_of_months - 1:
            if list_of_change_prof_loss[count_of_diff] > greatest_increase_prof[0]:
                del greatest_increase_prof[0]
                greatest_increase_prof.append(list_of_change_prof_loss[count_of_diff])
            if list_of_change_prof_loss[count_of_diff] < greatest_decrease_loss[0]:
                del greatest_decrease_loss[0]
                greatest_decrease_loss.append(list_of_change_prof_loss[count_of_diff])

    format_inc = "${:,.2f}".format(greatest_increase_prof[0])
    format_dec = "${:,.2f}".format(greatest_decrease_loss[0])
    average_change = (sum_of_change / count_of_diff)
    format_avg_change = "${:,.2f}".format(average_change)

new_list = zip(each_month, each_profit_loss, list_of_change_prof_loss)

pybanknew_loc = os.path.join("Resources", "budget_data_new.csv")
with open (pybanknew_loc, "w", newline='') as pybanknew_open:
    pybankwriter = csv.writer(pybanknew_open, delimiter=",")
    pybankwriter.writerow(["Date", "Profit/Loss", "Change in Prof/Loss"])
    pybankwriter.writerows(new_list)

pybank_new_rd_loc = os.path.join("Resources", "budget_data_new.csv")
with open (pybank_new_rd_loc, newline='') as pybank_new_rd_open:
    pybank_new_reader = csv.reader(pybank_new_rd_open, delimiter = ",")
    pybank_new_reader_header = next(pybank_new_reader)
    for each_new_line in pybank_new_reader:
        if "${:,.2f}".format(float(each_new_line[2])) == format_inc:
            greatest_increase_prof_date.append(each_new_line[0])
        if "${:,.2f}".format(float(each_new_line[2])) == format_dec:
            greatest_decrease_loss_date.append(each_new_line[0])

pybank_txt_loc = os.path.join("budget_analysis.txt")
txt_writer = open(pybank_txt_loc, 'w')
txt_writer.write("Financial Analysis\n")
txt_writer.write("---------------------------\n")
txt_writer.write(f"Total Months: {count_of_months}\n")
txt_writer.write(f"Total: {format_net}\n")
txt_writer.write(f"Average Change: {format_avg_change}\n")
txt_writer.write(f"Greatest Increase in Profits: {greatest_increase_prof_date}  ({format_inc})\n")
txt_writer.write(f"Greatest Decrease in Profits: {greatest_decrease_loss_date}  ({format_dec})\n")

