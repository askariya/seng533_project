import sys
import csv
from collections import defaultdict

def calculateAnswers(filename):
    columns = defaultdict(list) # each value in each column is appended to a list
    file = filename
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

    print("\n__Utilization for DB__")
    #list of disk and processor utilization columns
    dp_column_names = ["\PhysicalDisk(_Total)\% Disk Time", "\Processor(0)\% DPC Time", 
    "\Processor(0)\% Interrupt Time", "\Processor(0)\% Privileged Time", "\Processor(0)\% Processor Time", 
    "\Processor(0)\% User Time", "\Process(Idle)\% Processor Time"]

    print_averages(columns, dp_column_names)

    print("\n__Utilization for Web App Processes__")
    # print_averages(columns, dp_column_names)
    
    #4, part 4
    print("\n__Utilization for Web App Processes__")
    #list of Web Server utilization columns
    wa_process_cols = ["\\\\isp-01\Process(wHTTPg)\% Privileged Time", "\\\\isp-01\Process(wHTTPg)\% User Time"]
    print_averages(columns, wa_process_cols)

    print("\n__Utilization for App Processes__")
    app_process_cols = [
        "\\\\isp-01\Process(server#0)\% Privileged Time", "\\\\isp-01\Process(server#0)\% User Time", 
        "\\\\isp-01\Process(server#1)\% Privileged Time", "\\\\isp-01\Process(server#1)\% User Time", 
        "\\\\isp-01\Process(server#2)\% Privileged Time", "\\\\isp-01\Process(server#2)\% User Time", 
        "\\\\isp-01\Process(server#3)\% Privileged Time", "\\\\isp-01\Process(server#3)\% User Time",
        "\\\\isp-01\Process(server#4)\% Privileged Time", "\\\\isp-01\Process(server#4)\% User Time",
        "\\\\isp-01\Process(server#5)\% Privileged Time", "\\\\isp-01\Process(server#5)\% User Time",
        "\\\\isp-01\Process(server#6)\% Privileged Time", "\\\\isp-01\Process(server#6)\% User Time",
        "\\\\isp-01\Process(server#7)\% Privileged Time", "\\\\isp-01\Process(server#7)\% User Time",
        "\\\\isp-01\Process(server#8)\% Privileged Time", "\\\\isp-01\Process(server#8)\% User Time",
        "\\\\isp-01\Process(server#9)\% Privileged Time", "\\\\isp-01\Process(server#9)\% User Time",
        "\\\\isp-01\Process(server#10)\% Privileged Time", "\\\\isp-01\Process(server#10)\% User Time",
        "\\\\isp-01\Process(server#11)\% Privileged Time", "\\\\isp-01\Process(server#11)\% User Time",
        "\\\\isp-01\Process(server#12)\% Privileged Time", "\\\\isp-01\Process(server#12)\% User Time",
        "\\\\isp-01\Process(server#13)\% Privileged Time", "\\\\isp-01\Process(server#13)\% User Time",
        "\\\\isp-01\Process(server#14)\% Privileged Time", "\\\\isp-01\Process(server#14)\% User Time",
        "\\\\isp-01\Process(server#15)\% Privileged Time", "\\\\isp-01\Process(server#15)\% User Time"
    ]
    print_averages(columns, app_process_cols)

    print("\n__Utilization for DB Server__")
    db_process_cols = ["\Process(db2syscs)\% User Time", "\Process(db2syscs)\% Privileged Time"]
    print_averages(columns, db_process_cols)

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
    print("\nMean Response Time: " + str(mean_resp_time))


    # 5 A) part 2
    req_per_sec = (line_count/11139282.538)*1000
    print("Requests/sec: " + str(req_per_sec))


def print_averages(columns, col_names):
    for col in col_names:
        total = 0
        count = 0
        # try:
        #     columns[col] = [float(i) for i in columns[col]] #convert values to float
        # except Exception as e:
        #     print(e) 
        for value in columns[col]:
            if value == "":
                continue
            total += float(value)
            count += 1
        print(col + ": " + str(total/count))

def main():
    if len(sys.argv) < 2:
        print('Usage: ' + sys.argv[0] + ' <filename>')
        sys.exit(1)

    filename = sys.argv[1]
    calculateAnswers("case1-perfmon-data.csv")


if __name__ == '__main__':
    main()