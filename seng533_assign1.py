import sys
import csv
from collections import defaultdict



def calculateAnswers(csv_file, txt_file):
    columns = defaultdict(list) # each value in each column is appended to a list
    file = csv_file
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
    # print_averages(columns, app_process_cols)
    get_averages(columns, app_process_cols)

    print("\n__Utilization for DB Server__")
    db_process_cols = ["\Process(db2syscs)\% User Time", "\Process(db2syscs)\% Privileged Time"]
    print_averages(columns, db_process_cols)

    #5 A) part 1
    print("\n__________5) A.1___________")
    input_file = open(txt_file,"r")
    line_count = -1
    total_resp_time = 0
    total_conn_time = 0
    total_firstbyte_time = 0
    total_lastbyte_time = 0
    for line in input_file:
        if line_count == -1:
            line_count = 0
            continue      
        line_count+=1
        line = line.split(",")
        #[2]Time taken to open connection with server (ms) + [3]Time taken to receive first byte of reply (ms) + 
        #[4]Time taken to receive last byte of reply (ms)
        total_conn_time += float(line[2])
        total_firstbyte_time += float(line[3])
        total_lastbyte_time += float(line[4])
        total_resp_time += (float(line[2]) + float(line[3]) + float(line[4])) 

    mean_resp_time = total_resp_time/line_count
    avg_conn_time = total_conn_time/line_count
    avg_firstbyte_time = total_firstbyte_time/line_count
    avg_lastbyte_time = total_lastbyte_time/line_count
    print("Avg Conn Time: " + str(avg_conn_time))
    print("Avg First Byte Time: " + str(avg_firstbyte_time))
    print("Avg Last Byte Time: " + str(avg_lastbyte_time))
    print("\nMean Response Time: " + str(mean_resp_time))


    # 5 A) part 2
    req_per_sec = (line_count/11139282.538)*1000
    print("Requests/sec: " + str(req_per_sec))

    # 5 B)
    print("\n__________5) B___________")
    do5B()

    #6 B)
    print("\n__________6) B___________")
    total_time = None
    num_requests = None
    if txt_file == "case1-httperf-detailed-output.txt" and csv_file == "case1-perfmon-data.csv":
        total_time = 11064
        num_requests = 89602
    elif txt_file == "case2-httperf-detailed-output.txt" and csv_file == "case2-perfmon-data.csv":
        total_time = 12026
        num_requests = 90400
    else:
        raise Exception("Invalid File Names! Make sure you are using matching CSV and TXT files.")

    print("\n__Demand for Web Process__")
    get_demands(columns, wa_process_cols, total_time, num_requests)

    print("\n__Demand for App Processes__")
    get_demands_app(columns, app_process_cols, total_time, num_requests)

    print("\n__Demand for DB Process__")
    get_demands(columns, db_process_cols, total_time, num_requests)
    

def print_averages(columns, col_names):
    col_total = 0
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
        col_total = col_total + (total/count)        
        print(col + ": " + str(total/count))
    print("Sum: " + str(col_total))

def get_averages(columns, col_names):

    prev_col = None
    for col in col_names:
        total = 0
        count = 0
    
        for value in columns[col]:
            if value == "":
                count += 1
                continue
            total += float(value)
            count += 1
        if prev_col == None:
            prev_col = total/count
        else:
            cur_col = total/count
            print(col)
            print (str(prev_col + cur_col))
            prev_col = None

def get_demands(columns, col_names, total_time, num_requests):
    col_total = 0
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
        col_total = col_total + (total/count)        
        # print(col + ": " + str(total/count))
    utilization = col_total/100
    demand = ((utilization*total_time)/num_requests)*1000
    print("Demand: " + str(demand)) 

def get_demands_app(columns, col_names, total_time, num_requests):

    prev_col = None
    for col in col_names:
        total = 0
        count = 0
    
        for value in columns[col]:
            if value == "":
                count += 1
                continue
            total += float(value)
            count += 1
        if prev_col == None:
            prev_col = total/count
        else:
            cur_col = total/count
            # print(col)
            # print (str(prev_col + cur_col))

            utilization = (prev_col + cur_col)/100
            demand = ((utilization*total_time)/num_requests)*1000
            print(str(demand)) 

            prev_col = None

def do5B():
    filenameCase1 = "case1-httperf-detailed-output.txt"
    filenameCase2 = "case2-httperf-detailed-output.txt"

    input_file = open(filenameCase1,"r")
    min_bytes_per_ms = float('inf')
    total_bytes_per_ms = 0
    line_count = -1
    total_resp_time = 0
    for line in input_file:
        if line_count == -1:
            line_count = 0
            continue      
        line_count+=1
        line = line.split(",")
        resp_time = (float(line[2]) + float(line[3]) + float(line[4]))
        total_resp_time += resp_time
        total_bytes_per_ms += float(line[6])/resp_time
        if float(line[6])/resp_time < min_bytes_per_ms:
            min_bytes_per_ms = float(line[6])/resp_time

    mean_resp_time = total_resp_time/line_count
    print("\nMean Response Time Case1: " + str(mean_resp_time))
    print("Mean KB/Sec Case1: " + str(total_bytes_per_ms/line_count))
    print("Min KB/Sec Case1: " + str(min_bytes_per_ms))
    print("Total Requests: " + str(line_count))

    min_bytes_per_ms = float('inf')
    mean_bytes_per_ms = 0
    input_file = open(filenameCase2,"r")
    line_count = -1
    total_resp_time = 0
    for line in input_file:
        if line_count == -1:
            line_count = 0
            continue      
        line_count+=1
        line = line.split(",")
        resp_time = (float(line[2]) + float(line[3]) + float(line[4]))
        total_resp_time += resp_time 
        total_bytes_per_ms += float(line[6])/resp_time
        if float(line[6])/resp_time < min_bytes_per_ms:
            min_bytes_per_ms = float(line[6])/resp_time

    mean_resp_time = total_resp_time/line_count
    print("\nMean Response Time Case2: " + str(mean_resp_time))
    print("Mean KB/Sec Case2: " + str(total_bytes_per_ms/line_count))
    print("Min KB/Sec Case2: " + str(min_bytes_per_ms))
    print("Total Requests: " + str(line_count))
            

def main():
    if len(sys.argv) < 3:
        print('Usage: ' + sys.argv[0] + ' <csv_file> <txt_file>')
        sys.exit(1)

    csv_file = sys.argv[1]
    txt = sys.argv[2]
    calculateAnswers(csv_file, txt)


if __name__ == '__main__':
    main()