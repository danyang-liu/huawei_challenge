# coding=utf-8

import datetime
import random
import math
import server

flavor_mem = [1,2,4,2,4,8,4,8,16,8,16,32,16,32,64]
flavor_cpu = [1,1,1,2,2,2,4,4,4,8,8,8,16,16,16]

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
            if item[1] == flavor_type[index] and item[2]+datetime.timedelta(predict_data_delta+1)>=predict_date_start and item[2]+datetime.timedelta(predict_data_delta+1)<=predict_data_end:
                predict_flavor_num[index] = predict_flavor_num[index] + 1

    for item in predict_flavor_num:
        total_flavors_num = total_flavors_num + item

    result.append(str(total_flavors_num))
    for index in range(flavor_type_num):
        result.append(str(flavor_type[index]) + ' ' + str(predict_flavor_num[index]))

    result.append('')

    # get flavor list
    flavor_list = []
    for f_type in range(len(flavor_type)):
        for i_f_type in range(predict_flavor_num[f_type]):
            flavor_list.append(int(flavor_type[f_type][6:]))


    # # put navie
    # result.append(str(total_flavors_num))
    # i_index = 1
    # for index in range(flavor_type_num):
    #     for type_index in range(predict_flavor_num[index]):
    #         result.append(str(i_index)+' '+flavor_type[index]+' '+str(1))
    #         i_index = i_index + 1


    # #put 首次适应
    # server_list = []
    #
    # server_ins = server.Server(server_infor[0],server_infor[1],server_infor[2])
    # server_list.append(server_ins)
    #
    # for f in range(len(flavor_list)):
    #     can_put_flavor = False
    #     for i in range(len(server_list)):
    #         if server_list[i].put_flavor(flavor_list[f],flavor_cpu[flavor_list[f]-1],flavor_mem[flavor_list[f]-1]):
    #             can_put_flavor = True
    #             break
    #     if can_put_flavor == False:
    #         server_ins = server.Server(server_infor[0], server_infor[1], server_infor[2])
    #         server_ins.put_flavor(flavor_list[f], flavor_cpu[flavor_list[f] - 1], flavor_mem[flavor_list[f] - 1])
    #         server_list.append(server_ins)
    #
    # result.append(str(len(server_list)))
    # for index in range(len(server_list)):
    #     flavor_result_list = ''
    #     for i in range(len(server_list[index].flavor_num)):
    #         if server_list[index].flavor_num[i] > 0:
    #             flavor_result_list = flavor_result_list + 'flavor' + str(i+1) + ' ' + str(server_list[index].flavor_num[i]) + ' '
    #     flavor_result_list = flavor_result_list[:-1]
    #     result.append(str(index+1)+' '+flavor_result_list)


    # put 模拟退火算法

    T = 100
    Tmin = 1
    r = 0.99
    minserver = total_flavors_num
    best_server_list = []
    flavor_dice = range(total_flavors_num)

    while T>Tmin:
        random.shuffle(flavor_dice)
        new_flavor_list = []
        for i in range(len(flavor_list)):
            new_flavor_list.append(flavor_list[i])
        new_flavor_list[flavor_dice[0]]=flavor_list[flavor_dice[1]]
        new_flavor_list[flavor_dice[1]]=flavor_list[flavor_dice[0]]

        server_list = []

        server_ins = server.Server(server_infor[0],server_infor[1],server_infor[2])
        server_list.append(server_ins)

        for f in range(len(new_flavor_list)):
            can_put_flavor = False
            for i in range(len(server_list)):
                if server_list[i].put_flavor(new_flavor_list[f],flavor_cpu[new_flavor_list[f]-1],flavor_mem[new_flavor_list[f]-1]):
                    can_put_flavor = True
                    break
            if can_put_flavor == False:
                server_ins = server.Server(server_infor[0], server_infor[1], server_infor[2])
                server_ins.put_flavor(new_flavor_list[f], flavor_cpu[new_flavor_list[f] - 1], flavor_mem[new_flavor_list[f] - 1])
                server_list.append(server_ins)

        score = len(server_list)

        if score < minserver:
            minserver = score
            flavor_list = new_flavor_list
            best_server_list = server_list
        else:
            if math.exp(minserver-score)/(T) > random.random():
                minserver = score
                flavor_list = new_flavor_list
                best_server_list = server_list
        T = T * r

    result.append(str(len(best_server_list)))
    for index in range(len(best_server_list)):
        flavor_result_list = ''
        for i in range(len(best_server_list[index].flavor_num)):
            if best_server_list[index].flavor_num[i] > 0:
                flavor_result_list = flavor_result_list + 'flavor' + str(i+1) + ' ' + str(best_server_list[index].flavor_num[i]) + ' '
        flavor_result_list = flavor_result_list[:-1]
        result.append(str(index+1)+' '+flavor_result_list)


    return result
