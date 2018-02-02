import csv
from collections import defaultdict

columns = defaultdict(list) # each value in each column is appended to a list
file = "case1-perfmon-data.csv"
reader = csv.DictReader(open(file, newline=""), dialect="excel")
for row in reader:
    for (k,v) in row.items(): # go over each column name and value 
        columns[k].append(v) # append the value into the appropriate list
# print(columns['Time'])                      # based on column name k

columns['Time'] = [int(i) for i in columns['Time']]
# print(columns['Time']) 
# # 4, Part 1
first_val = columns['Time'][0]
last_val = columns['Time'][len(columns['Time'])-1]

time = (last_val - first_val)
print("Total time taken to run tests: " + str(time) + " seconds")

# 4, part 2
prev_value = None
diff_array = []
for value in columns['Time']:
    if prev_value is None:
        prev_value = value
        continue
    else:
        diff_array.append(value - prev_value)
        prev_value = value
diff_array.append(value - prev_value)
print("Mean Sampling Rate:" +  str(sum(diff_array)/len(diff_array)))

#4, part 3
#TODO Calculate Utilization for Physical Disk and Processor columns????


#5 A) part 1
input_file = open("case1-httperf-detailed-output.txt","r")
line_count = -1
total_resp_time = 0
for line in input_file:
    if line_count == -1:
        line_count = 0
        continue      
    line_count+=1
    line = line.split(",")
    total_resp_time += (float(line[2]) + float(line[3]) + float(line[4])) 

mean_resp_time = total_resp_time/line_count
print("Mean Response Time: " + str(mean_resp_time))


# 5 A) part 2
req_per_sec = (line_count/11139282.538)*1000
print("Requests/sec: " + str(req_per_sec))
