import os
import csv

voter_count = 0
voters_candidate_list = []
candidate_list = []
candidate_vote_count_list = []
candidate_pct_list = []
x = 0
candidate_0_vote_count = 0
candidate_1_vote_count = 0
candidate_2_vote_count = 0
candidate_3_vote_count = 0
winner = 0

election_data_loc = os.path.join("Resources", "election_data.csv")
with open (election_data_loc, "r", newline='') as election_data_open:
    election_data_reader = csv.reader(election_data_open, delimiter = ",")
    election_data_header = next(election_data_reader)

    #For voter count and each voter's candidate choice
    for each_voter in election_data_reader:
        voter_count += 1
        voters_candidate_list.append(each_voter[2])

    candidate_list = sorted(list(set(voters_candidate_list)))
    num_of_candidates = len(candidate_list)

election_data_loc2 = os.path.join("Resources", "election_data.csv")
with open (election_data_loc2, "r", newline='') as election_data_open2:
    election_data_reader2 = csv.reader(election_data_open2, delimiter = ",")
    election_data_header2 = next(election_data_reader2)

    #For count of each candidate
    for each_voter2 in election_data_reader2:
        if each_voter2[2] == candidate_list[0]:
            candidate_0_vote_count += 1
        elif each_voter2[2] == candidate_list[1]:
            candidate_1_vote_count += 1
        elif each_voter2[2] == candidate_list[2]:
            candidate_2_vote_count += 1
        elif each_voter2[2] == candidate_list[3]:
            candidate_3_vote_count += 1
    candidate_vote_count_list.append(candidate_0_vote_count)
    candidate_vote_count_list.append(candidate_1_vote_count)
    candidate_vote_count_list.append(candidate_2_vote_count)
    candidate_vote_count_list.append(candidate_3_vote_count)

#To find percentage of total votes for each candidate
candidate_0_pct = "{:.3%}".format(candidate_0_vote_count/voter_count)
candidate_pct_list.append(candidate_0_pct)
candidate_1_pct = "{:.3%}".format(candidate_1_vote_count/voter_count)
candidate_pct_list.append(candidate_1_pct)
candidate_2_pct = "{:.3%}".format(candidate_2_vote_count/voter_count)
candidate_pct_list.append(candidate_2_pct)
candidate_3_pct = "{:.3%}".format(candidate_3_vote_count/voter_count)
candidate_pct_list.append(candidate_3_pct)

#Combined lists to do final analysis on winner
combined_lists = zip(candidate_list, candidate_vote_count_list, candidate_pct_list)
highest_popular_vote = max(candidate_vote_count_list)
for each_candidate in combined_lists:
    if each_candidate[1] == highest_popular_vote:
        winner = each_candidate[0]

#Writing out analysis as txt file
pypoll_writer_loc = os.path.join("PyPoll_analysis.txt")
txt_writer = open(pypoll_writer_loc, "w")
txt_writer.write("Election Results\n")
txt_writer.write("----------------------\n")
txt_writer.write(f"Total Votes: {voter_count}\n")
txt_writer.write("----------------------\n")
txt_writer.write(f"{candidate_list[1]}: {candidate_1_pct} ({candidate_1_vote_count})\n")
txt_writer.write(f"{candidate_list[0]}: {candidate_0_pct} ({candidate_0_vote_count})\n")
txt_writer.write(f"{candidate_list[2]}: {candidate_2_pct} ({candidate_2_vote_count})\n")
txt_writer.write(f"{candidate_list[3]}: {candidate_3_pct} ({candidate_3_vote_count})\n")
txt_writer.write("----------------------\n")
txt_writer.write(f"Winner: {winner}\n")

