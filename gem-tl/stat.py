import os
import shutil



def copy_file(src_file, dest_file):
    shutil.copy2(src_file, dest_file)
    

def remove_last_comma(filename):
    with open(filename, 'r') as file:
        content = file.read()
    
    if ',' in content:
        last_comma_index = content.rfind(',')

        modified_content = content[:last_comma_index] + content[last_comma_index+1:]

        with open(filename, 'w') as file:
            file.write(modified_content)
    



def calculate_sum(filename):
    total_sum = 0

    with open(filename, 'r') as file:
        for line in file:
            data_list = line.rstrip().split(',')

            for data in data_list:
                total_sum += int(data)

    return total_sum

filename = '../tmp_result/cycle.txt'
remove_last_comma(filename)
sum_result = calculate_sum(filename)
print(f"The NPU execution time is : {sum_result}")

dest_file = '../tmp_result/backup_cycle.txt'

copy_file(filename, dest_file)
os.remove(filename)
