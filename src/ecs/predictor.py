# coding=utf-8

import datetime

def predict_vm(ecs_lines, input_lines):
    # Do your work from here#
    result = []
    if ecs_lines is None:
        print 'ecs information is none'
        return result
    if input_lines is None:
        print 'input file information is none'
        return result

    esc_data = []
    for item in ecs_lines:
        item_split = item.split('\t')
        item_split[2] = item_split[2].split()[0]
        item_split[2] = datetime.date(int(item_split[2].split('-')[0]),int(item_split[2].split('-')[1]),int(item_split[2].split('-')[2]))
        esc_data.append(item_split)

    server_infor = []
    server_infor.append(int(input_lines[0].split()[0]))
    server_infor.append(int(input_lines[0].split()[1]))
    server_infor.append(int(input_lines[0].split()[2]))

    flavor_type_num = int(input_lines[2])
    flavor_type = []

    for i in range(flavor_type_num):
        flavor_type.append(input_lines[3+i].split()[0])

    resource_type = input_lines[flavor_type_num+4].split()[0]

    date_start_split = input_lines[flavor_type_num+6].split()[0]
    date_end_split = input_lines[flavor_type_num+7].split()[0]
    predict_date_start = datetime.date(int(date_start_split.split('-')[0]),int(date_start_split.split('-')[1]),int(date_start_split.split('-')[2]))
    predict_data_end = datetime.date(int(date_end_split.split('-')[0]),int(date_end_split.split('-')[1]),int(date_end_split.split('-')[2]))


    #predict
    total_flavors_num = 0

    predict_data_delta = (predict_data_end - predict_date_start).days
    predict_flavor_num = []
    for index in range(flavor_type_num):
        predict_flavor_num.append(0)
        for item in esc_data:
            if item[1] == flavor_type[index] and item[2]+datetime.timedelta(predict_data_delta)>predict_date_start and item[2]+datetime.timedelta(predict_data_delta)<predict_data_end:
                predict_flavor_num[index] = predict_flavor_num[index] + 1

    for item in predict_flavor_num:
        total_flavors_num = total_flavors_num + item

    result.append(str(total_flavors_num))
    for index in range(flavor_type_num):
        result.append(str(flavor_type[index]) + ' ' + str(predict_flavor_num[index]))

    result.append('\n')
    # put

    result.append(str(total_flavors_num))
    i_index = 1
    for index in range(flavor_type_num):
        for type_index in range(predict_flavor_num[index]):
            result.append(str(i_index)+' '+flavor_type[index]+' '+str(1))
            i_index = i_index + 1


    return result
