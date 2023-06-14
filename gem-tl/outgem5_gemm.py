#invoking numpy for computation
import os
#TODO: read weight
#os.system("python test.py")

#=============================
#           STAGE2           #
#=============================

#generating params for timeloop emulating
# command1: timeloop-model $arch $prob $map
# TODO: command2: timeloop-mapper $arch $prob $mapper $constraints
# TODO: arch? PE & memory hierarchy, not specified, default
# TODO: map? not specified, default
#prob
import yaml

def get_yaml_data(yaml_file):
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    #print(file_data)
 
    data = yaml.safe_load(file_data)
    #print(data)
    return data

def get_params():
    file = open('/home/gem5/tmp_result/config.txt', 'r')
    lines = []
    for line in file:
        lines.append(int(line.strip()))
    return lines

def generate_yaml_doc(data, yaml_file):
    file = open(yaml_file, 'w', encoding='utf-8')
    yaml.dump(data, file)
    file.close()

def modify_data_dict(dic, params):
    dic['problem']['instance']['C'] = params[2]
    dic['problem']['instance']['M'] = params[3]
    dic['problem']['instance']['P'] = params[1]
    dic['problem']['instance']['Q'] = params[1]
    dic['problem']['instance']['R'] = params[1]
    dic['problem']['instance']['S'] = params[1]

    return dic

def generate_new_yaml():
    old_yaml_file = "/home/yangnan/gtloopg/gtimeloop/conv1d.prob.yaml"
    data_dict = get_yaml_data(old_yaml_file)

    params = get_params()
    dic = modify_data_dict(data_dict, params)

    new_yaml_file = "/home/yangnan/gtloopg/gtimeloop/prob/gemm.yaml"
    generate_yaml_doc(dic, new_yaml_file)

generate_new_yaml()
#os.system("timeloop-model $arch apollo.yaml $map")

