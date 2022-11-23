import pandas as pd
import os
import logging
import re
import numpy as np
logger = logging.getLogger()


def process_task2(f):
    valid_lines = []
    id_pattern = re.compile(r"^N\d{8}")
    total_lines_cnt = 0
    for line in f:
        total_lines_cnt += 1
        if len(line.split(",")) != 26:
            print("Invalid line of data: does not contain exactly 26 values:")
            print(line)
        elif re.fullmatch(id_pattern, line.split(',')[0]) is None:
            print("Invalid line of data: N# is invalid")
            print(line)
        else:
            valid_lines.append(line)
    
    return valid_lines, total_lines_cnt


def process_task3(lines):
    answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D".split(",")
    
    # init output
    scores = dict()
    skip_ones = {i: 0 for i in range(1, 26)}
    wrong_ones = {i: 0 for i in range(1, 26)}
    
    for line in lines:
        temp = [s.strip() for s in line.split(",")]
        student_id, selections = temp[0], temp[1:]
        # print(selections)
        score = 0
        for i in range(len(answer_key)):
            # print(i)
            if selections[i] == '':
                skip_ones[i+1] += 1
            elif selections[i] != answer_key[i]:
                wrong_ones[i+1] += 1
                score -= 1
            else:
                score += 4
                continue
        scores[student_id] = score
    
    # statistic
    highest_skip = sorted(skip_ones.values(), reverse=True)[0]
    highest_wrong = sorted(wrong_ones.values(), reverse=True)[0]
    most_skip_ones = [(k, v, round(v / len(lines), 3)) for k, v in skip_ones.items() if v == highest_skip]
    most_wrong_ones = [(k, v, round(v / len(lines), 3)) for k, v in wrong_ones.items() if v == highest_wrong]
    most_skip_ones = ", ".join([" - ".join([str(i) for i in m]) for m in most_skip_ones])
    most_wrong_ones = ", ".join([" - ".join([str(i) for i in m]) for m in most_wrong_ones])
    
    return scores, most_skip_ones, most_wrong_ones


if __name__ == "__main__":

    folder_path = "../data"
    while True:
        try:
            file_name = input("Enter a class file to grade (i.e. class1 for class1.txt): ")
            if file_name == 'q':
                break
            file_path = f"{folder_path}/{file_name}"
            with open(file_path) as f:
                print(f"Successfully opened {file_name}")
                print("**** ANALYZING ****")
                
                # task 2
                valid_lines, total_lines_cnt = process_task2(f)
                if len(valid_lines) == total_lines_cnt:
                    print("No errors found!")
                
                # task 3
                scores, most_skip_ones, most_wrong_ones = process_task3(valid_lines)
                highest_score = sorted(scores.values(), reverse=True)[0]
                lowest_score = sorted(scores.values(), reverse=False)[0]
                range_score = highest_score - lowest_score
                mean_score = np.mean(list(scores.values()))
                median_score = np.median(list(scores.values()))
                
                # task 4
                scores_df = pd.DataFrame(scores.items(), columns=['student_id', 'score'])
                scores_df.to_csv(f"{file_name.split('.')[0]}_grades.csv", index=False, header=False)
                
                # report
                print("**** REPORT ****")
                print(f"Total valid lines of data: {len(valid_lines)}")
                print(f"Total invalid lines of data: {total_lines_cnt - len(valid_lines)}")
                print(f"Mean (average) score: {mean_score}")
                print(f"Highest score: {highest_score}")
                print(f"Lowest score: {lowest_score}")
                print(f"Range of scores: {range_score}")
                print(f"Median score: {median_score}")
                print(f"Question that most people skip: {most_skip_ones}")
                print(f"Question that most people answer incorrectly: {most_wrong_ones}")

        except FileNotFoundError:
            print("Sorry, I can't find this filename")
        except Exception as e:
            logger.exception(e)
