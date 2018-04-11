# coding=utf-8

import datetime
import random
import math
import server
import utils

flavor_mem = [1,2,4,2,4,8,4,8,16,8,16,32,16,32,64]
flavor_cpu = [1,1,1,2,2,2,4,4,4,8,8,8,16,16,16]

holiday = [datetime.datetime(2015,1,1),datetime.datetime(2015,1,2),datetime.datetime(2015,1,3),datetime.datetime(2015,2,18),
           datetime.datetime(2015,2,19),datetime.datetime(2015,2,20),datetime.datetime(2015,2,21),datetime.datetime(2015,2,22),
           datetime.datetime(2015,2,23),datetime.datetime(2015,2,24),datetime.datetime(2015,4,5),datetime.datetime(2015,5,1),
           datetime.datetime(2015,6,20),datetime.datetime(2015,9,27),datetime.datetime(2015,10,1),datetime.datetime(2015,10,2),
           datetime.datetime(2015,10,3),datetime.datetime(2015,10,4),datetime.datetime(2015,10,5),datetime.datetime(2015,10,6),
           datetime.datetime(2015,10,7),

           datetime.datetime(2016,1,1),datetime.datetime(2016,2,7),datetime.datetime(2016,2,8),datetime.datetime(2016,2,9),
           datetime.datetime(2016,2,10),datetime.datetime(2016,2,11),datetime.datetime(2016,2,12),datetime.datetime(2016,2,13),
           datetime.datetime(2016,4,4), datetime.datetime(2016,5,1),datetime.datetime(2016,6,9), datetime.datetime(2016,6,10),
           datetime.datetime(2016,6,11),datetime.datetime(2016,10,1), datetime.datetime(2016,10,2),datetime.datetime(2016,10,3),
           datetime.datetime(2016,10,4),datetime.datetime(2016,10,5),datetime.datetime(2016,10,6),datetime.datetime(2016,10,7),

           datetime.datetime(2017,1,1),datetime.datetime(2017,1,27),datetime.datetime(2017,1,28),datetime.datetime(2017,1,29),
           datetime.datetime(2017,1,30),datetime.datetime(2017,1,31),datetime.datetime(2017,2,1),datetime.datetime(2017,2,2),
           datetime.datetime(2017,4,2), datetime.datetime(2017,4,3),datetime.datetime(2017,4,4), datetime.datetime(2017,5,28),
           datetime.datetime(2017,5,29), datetime.datetime(2017,5,30),datetime.datetime(2017,10,1),
           datetime.datetime(2017,10,2),datetime.datetime(2017,10,3),datetime.datetime(2017,10,4),datetime.datetime(2017,10,5),
           datetime.datetime(2017,10,6),datetime.datetime(2017,10,7),datetime.datetime(2017,10,8),

           datetime.datetime(2018,1,1),datetime.datetime(2018,2,15),datetime.datetime(2018,2,16),datetime.datetime(2018,2,17),
           datetime.datetime(2018,2,18),datetime.datetime(2018,2,19),datetime.datetime(2018,2,20),datetime.datetime(2018,2,21),
           ]


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

    #要预测的vm数
    flavor_type_num = int(input_lines[2])
    #要预测的vm种类 e.g. ['flavor1','flavor3'...]
    flavor_type = []

    for i in range(flavor_type_num):
        flavor_type.append(input_lines[3+i].split()[0])
    # CPU or MEM
    resource_type = input_lines[flavor_type_num+4].split()[0]

    date_start_split = input_lines[flavor_type_num+6].split()[0]
    date_end_split = input_lines[flavor_type_num+7].split()[0]
    predict_date_start = datetime.date(int(date_start_split.split('-')[0]),int(date_start_split.split('-')[1]),int(date_start_split.split('-')[2]))
    predict_date_end = datetime.date(int(date_end_split.split('-')[0]),int(date_end_split.split('-')[1]),int(date_end_split.split('-')[2]))
    train_date_start = esc_data[0][2]
    train_date_end = esc_data[-1][2]
    predict_data_delta = (predict_date_end - predict_date_start).days

    #存放每种vm的预测结果
    predict_flavor_num = []

    # #predict 取前一星期数据
    # for index in range(flavor_type_num):
    #     predict_flavor_num.append(0)
    #     for item in esc_data:
    #         if item[1] == flavor_type[index] and item[2]+datetime.timedelta(predict_data_delta+1)>=predict_date_start and item[2]+datetime.timedelta(predict_data_delta+1)<=predict_date_end:
    #             predict_flavor_num[index] = predict_flavor_num[index] + 1

#     #predict 权重法
# #    train_days_delta = (esc_data[-1][2]-esc_data[0][2]).days+1
#     train_days_delta = 6
#     for index in range(flavor_type_num):
#         predict_flavor_num.append(0)
#         for item in esc_data:
#             if item[1] == flavor_type[index] and item[2]+datetime.timedelta(train_days_delta)>=predict_date_start:
#                 predict_flavor_num[index] = predict_flavor_num[index] + 1
# #                predict_flavor_num[index] = predict_flavor_num[index] + 2-1.9*float((predict_date_start-item[2]).days-1)/float(train_days_delta)
#                 test_date = item[2]
#                 test1 = float((predict_date_start - item[2]).days)
#                 test = float((predict_date_start-item[2]).days)/float(train_days_delta)
#                 pass
#     for index in range(flavor_type_num):
#         predict_flavor_num[index] = int((predict_flavor_num[index]*float(predict_data_delta+1))/train_days_delta)


#     #predict 统计周末周中权重
#
#     train_days_delta = 6
#     #统计predict中周中周末数
#     predict_weekday_count = 0
#     predict_weekend_count = 0
#     train_weekday_count = 0
#     train_weekend_count = 0
#     for i in range(predict_data_delta+1):
#         if (predict_date_start+datetime.timedelta(i)).isoweekday()<6:
#             predict_weekday_count += 1
#         else:
#             predict_weekend_count += 1
#     #统计train中周中周末数
#     for i in range(train_days_delta+1):
#         if (predict_date_start-datetime.timedelta(train_days_delta+1-i)).isoweekday()<6:
#             train_weekday_count += 1
#         else:
#             train_weekend_count += 1
#
#     #目前 1.4效果最佳
#     predict_weekday_weekend_index = float(predict_weekend_count+1.4*predict_weekday_count)/float(predict_weekend_count+predict_weekday_count)
#     train_weekday_weekend_index = float(train_weekend_count + 1.4 * train_weekday_count) / float(train_weekend_count + train_weekday_count)
#
#     for index in range(flavor_type_num):
#         predict_flavor_num.append(0)
#         for item in esc_data:
#             if item[1] == flavor_type[index] and item[2] + datetime.timedelta(train_days_delta) >= predict_date_start:
#                 predict_flavor_num[index] = predict_flavor_num[index] + 1
#                 #                predict_flavor_num[index] = predict_flavor_num[index] + 2-1.9*float((predict_date_start-item[2]).days-1)/float(train_days_delta)
#                 test_date = item[2]
#                 test1 = float((predict_date_start - item[2]).days)
#                 test = float((predict_date_start - item[2]).days) / float(train_days_delta)
#                 pass
#     for index in range(flavor_type_num):
#         predict_flavor_num[index] = (predict_flavor_num[index] * float(predict_data_delta + 1)) / train_days_delta
# #        predict_flavor_num[index] = int(predict_flavor_num[index] * (float(predict_weekday_count)/(float(predict_weekday_count+predict_weekend_count))) / (float(train_weekday_count)/(float(train_weekday_count+train_weekend_count))))
#         predict_flavor_num[index] = int(predict_flavor_num[index]*predict_weekday_weekend_index/train_weekday_weekend_index)


    # #predict 线性回归
    # flavor_num = []
    # for i in range(flavor_type_num):
    #     flavor_num.append([])
    #     for j in range((train_date_end - train_date_start).days + 1):
    #         flavor_num[i].append(0)
    #
    # for i in range(len(esc_data)):
    #     ith_date = esc_data[i][2]
    #     ith_date_delta = (ith_date - train_date_start).days
    #     for j in range(len(flavor_type)):
    #         if esc_data[i][1] == flavor_type[j]:
    #             flavor_num[j][ith_date_delta] = flavor_num[j][ith_date_delta] + 1
    #
    # #简单去噪
    # for i in range(flavor_type_num):
    #     avarage_num = float(sum(flavor_num[i]))/float(len(flavor_num[i]))
    #     for j in range(len(flavor_num[i])):
    #         if flavor_num[i][j] > 10*avarage_num and (predict_date_start+datetime.timedelta(j)).isoweekday()<6:
    #             flavor_num[i][j] = 5*avarage_num
    #         if flavor_num[i][j] > 10*avarage_num and (predict_date_start+datetime.timedelta(j)).isoweekday()>=6:
    #             flavor_num[i][j] = avarage_num
    #         if avarage_num > 10*flavor_num[i][j] and (predict_date_start+datetime.timedelta(j)).isoweekday()<6:
    #             flavor_num[i][j] = avarage_num
    #         if avarage_num > 10 * flavor_num[i][j] and (predict_date_start+datetime.timedelta(j)).isoweekday()>=6:
    #             flavor_num[i][j] = 3*flavor_num[i][j]
    #
    #
    # date_index = []
    # for i in range((train_date_end-train_date_start).days+1):
    #     date_index.append(i)
    #
    # date_index_predict = []
    # for i in range((predict_date_end-predict_date_start).days+1):
    #     date_index_predict.append(len(date_index)+i)
    #
    # num_predict = []
    # for index in range(flavor_type_num):
    #     predict_flavor_num.append(0)
    #
    #     w0,w1 = utils.cal_simple_linear_regression_coefficients(date_index,flavor_num[index])
    #     num_predict.append([])
    #     for i in range(len(date_index_predict)):
    #         num_predict[index].append(w1*date_index_predict[i]+w0)
    #     predict_flavor_num[index] = int(sum(num_predict[index]))
    # for i in range(len(predict_flavor_num)):
    #     if predict_flavor_num[i]<0:
    #         predict_flavor_num[i] = 0


    # #predict 一次指数平滑
    # flavor_num = []
    # s_pinghua_flavor_num_predict = []
    # for i in range(flavor_type_num):
    #     flavor_num.append([])
    #     s_pinghua_flavor_num_predict.append([])
    #     for j in range((train_date_end - train_date_start).days + 1):
    #         flavor_num[i].append(0)
    #
    # for i in range(len(esc_data)):
    #     ith_date = esc_data[i][2]
    #     ith_date_delta = (ith_date - train_date_start).days
    #     for j in range(len(flavor_type)):
    #         if esc_data[i][1] == flavor_type[j]:
    #             flavor_num[j][ith_date_delta] = flavor_num[j][ith_date_delta] + 1
    #
    #             # 简单去噪
    # for i in range(flavor_type_num):
    #     avarage_num = float(sum(flavor_num[i])) / float(len(flavor_num[i]))
    #     for j in range(len(flavor_num[i])):
    #         if flavor_num[i][j] > 10 * avarage_num and (
    #             predict_date_start + datetime.timedelta(j)).isoweekday() < 6:
    #             flavor_num[i][j] = 5 * avarage_num
    #         if flavor_num[i][j] > 10 * avarage_num and (
    #             predict_date_start + datetime.timedelta(j)).isoweekday() >= 6:
    #             flavor_num[i][j] = avarage_num
    #         if avarage_num > 10 * flavor_num[i][j] and (
    #             predict_date_start + datetime.timedelta(j)).isoweekday() < 6:
    #             flavor_num[i][j] = avarage_num
    #         if avarage_num > 10 * flavor_num[i][j] and (
    #             predict_date_start + datetime.timedelta(j)).isoweekday() >= 6:
    #             flavor_num[i][j] = 3 * flavor_num[i][j]
    #
    # #求指数平滑初始值
    # pinghua_flavor_num_predict_init = []
    # for i in range(flavor_type_num):
    #     pinghua_flavor_num_predict_init.append(float(sum(flavor_num[i][0:3]))/float(3))
    #
    # a = 0.6
    #
    # #求指数平滑预测序列
    # for i in range(flavor_type_num):
    #     s1 = pinghua_flavor_num_predict_init[i]
    #     for j in range((train_date_end-train_date_start).days+1+predict_data_delta+1):
    #         if j <(train_date_end-train_date_start).days+1:
    #             s_pinghua_flavor_num_predict[i].append(a*float(flavor_num[i][j])+(1-a)*s1)
    #             s1 = s_pinghua_flavor_num_predict[i][-1]
    #         else:
    #             flavor_num[i].append(a*float(flavor_num[i][j-1])+(1-a)*s1)
    #             s_pinghua_flavor_num_predict.append(a * float(flavor_num[i][j]) + (1 - a) * s1)
    #             s1 = s_pinghua_flavor_num_predict[i][-1]
    #         pass
    #
    # predict_flavor_num = []
    # for i in range(flavor_type_num):
    #     predict_flavor_num.append(int(sum(flavor_num[i][-(predict_data_delta+1):])))
    #     pass

    # #predict 二次指数平滑
    # flavor_num = []
    # s_pinghua_flavor_num_predict = []
    # for i in range(flavor_type_num):
    #     flavor_num.append([])
    #     s_pinghua_flavor_num_predict.append([])
    #     for j in range((train_date_end - train_date_start).days + 1):
    #         flavor_num[i].append(0)
    #
    # for i in range(len(esc_data)):
    #     ith_date = esc_data[i][2]
    #     ith_date_delta = (ith_date - train_date_start).days
    #     for j in range(len(flavor_type)):
    #         if esc_data[i][1] == flavor_type[j]:
    #             flavor_num[j][ith_date_delta] = flavor_num[j][ith_date_delta] + 1
    #
    # # 求指数平滑初始值
    # pinghua_flavor_num_predict_init = []
    # for i in range(flavor_type_num):
    #     pinghua_flavor_num_predict_init.append(float(sum(flavor_num[i][0:3])) / float(3))
    #
    # a = 0.2
    #
    # for i in range(flavor_type_num):
    #     s1 = []
    #     s2 = []
    #     at = []
    #     bt = []
    #     s1.append(a * float(flavor_num[i][0]) + (1 - a) * float(pinghua_flavor_num_predict_init[i]))
    #     s2.append(a * s1[0] + (1 - a) * float(pinghua_flavor_num_predict_init[i]))
    #     at.append(2 * s1[0] - s2[0])
    #     bt.append((a / (1 - a)) * (s1[0] - s2[0]))
    #
    #     for j in range(1, (train_date_end - train_date_start).days + 1):
    #         s1.append(a * float(flavor_num[i][j]) + (1 - a) * float(s1[j - 1]))
    #         s2.append(a * s1[j] + (1 - a) * float(s2[j - 1]))
    #         at.append(2 * s1[j] - s2[j])
    #         bt.append((a / (1 - a)) * (s1[j] - s2[j]))
    #
    #     for j in range(predict_data_delta + 1):
    #         flavor_num[i].append(at[-1] + bt[-1] * (j + 1))
    #
    # predict_flavor_num = []
    # for i in range(flavor_type_num):
    #     predict_flavor_num.append(int(1.021 * sum(flavor_num[i][-(predict_data_delta + 1):])))
    #     pass
    # for i in range(flavor_type_num):
    #     if predict_flavor_num[i] < 0:
    #         predict_flavor_num[i] = 0


    #predict 三次指数平滑
    flavor_num = []
    s_pinghua_flavor_num_predict = []
    for i in range(flavor_type_num):
        flavor_num.append([])
        s_pinghua_flavor_num_predict.append([])
        for j in range((train_date_end - train_date_start).days + 1):
            flavor_num[i].append(0)

    for i in range(len(esc_data)):
        ith_date = esc_data[i][2]
        ith_date_delta = (ith_date - train_date_start).days
        for j in range(len(flavor_type)):
            if esc_data[i][1] == flavor_type[j]:
                flavor_num[j][ith_date_delta] = flavor_num[j][ith_date_delta] + 1


    # 简单去噪
    for i in range(flavor_type_num):
        avarage_num = float(sum(flavor_num[i])) / float(len(flavor_num[i]))
        for j in range(len(flavor_num[i])):
            if flavor_num[i][j] > 10 * avarage_num and (
                predict_date_start + datetime.timedelta(j)).isoweekday() < 6:
                flavor_num[i][j] = 5 * avarage_num
            if flavor_num[i][j] > 10 * avarage_num and (
                predict_date_start + datetime.timedelta(j)).isoweekday() >= 6:
                flavor_num[i][j] = avarage_num
            if avarage_num > 10 * flavor_num[i][j] and (
                predict_date_start + datetime.timedelta(j)).isoweekday() < 6:
                flavor_num[i][j] = avarage_num
            if avarage_num > 10 * flavor_num[i][j] and (
                predict_date_start + datetime.timedelta(j)).isoweekday() >= 6:
                flavor_num[i][j] = 3 * flavor_num[i][j]

    #求指数平滑初始值
    pinghua_flavor_num_predict_init = []
    for i in range(flavor_type_num):
        pinghua_flavor_num_predict_init.append(float(sum(flavor_num[i][0:3]))/float(3))

    a = 0.05

    for i in range(flavor_type_num):
        s1 = []
        s2 = []
        s3 = []
        at = []
        bt = []
        ct = []
        s1.append(a*float(flavor_num[i][0])+(1-a)*float(pinghua_flavor_num_predict_init[i]))
        s2.append(a * s1[0] + (1 - a) * float(pinghua_flavor_num_predict_init[i]))
        s3.append(a * s2[0] + (1 - a) * float(pinghua_flavor_num_predict_init[i]))
        at.append(3*s1[0]-3*s2[0]+s3[0])
        bt.append((a*a/(2*(1-a)*(1-a)))*((6-5*a)*s1[0]-(10-8*a)*s2[0]+(4-3*a)*s3[0]))
        ct.append((a*a/((1-a)*(1-a))*(s1[0]-2*s2[0]+s3[0])))

        for j in range(1,(train_date_end-train_date_start).days+1):
            s1.append(a * float(flavor_num[i][j]) + (1 - a) * float(s1[j-1]))
            s2.append(a * s1[j] + (1 - a) * float(s2[j-1]))
            s3.append(a * s2[j] + (1 - a) * float(s3[j-1]))
            at.append(3 * s1[j] - 3 * s2[j] + s3[j])
            bt.append((a * a / (2 * (1 - a) * (1 - a))) * ((6 - 5 * a) * s1[j] - (10 - 8 * a) * s2[j] + (4 - 3 * a) * s3[j]))
            ct.append((a * a / ((1 - a) * (1 - a)) * (s1[j] - 2 * s2[j] + s3[j])))

        for j in range(predict_data_delta+1):
            flavor_num[i].append(at[-1]+bt[-1]*(j+1)+ct[-1]*ct[-1]*(j+1)*(j+1))

    predict_flavor_num_3_zhishu = []
    for i in range(flavor_type_num):
        #predict_flavor_num.append(int(1.02*sum(flavor_num[i][-(predict_data_delta+1):])))
        predict_flavor_num_3_zhishu.append(sum(flavor_num[i][-(predict_data_delta + 1):]))
        pass
    for i in range(flavor_type_num):
        if predict_flavor_num_3_zhishu[i]<0:
            predict_flavor_num_3_zhishu[i] = 0


    #predict 局部加权线性回归
    flavor_num = []
    s_pinghua_flavor_num_predict = []
    for i in range(flavor_type_num):
        flavor_num.append([])
        s_pinghua_flavor_num_predict.append([])
        for j in range((train_date_end - train_date_start).days + 1):
            flavor_num[i].append(0)

    for i in range(len(esc_data)):
        ith_date = esc_data[i][2]
        ith_date_delta = (ith_date - train_date_start).days
        for j in range(len(flavor_type)):
            if esc_data[i][1] == flavor_type[j]:
                flavor_num[j][ith_date_delta] = flavor_num[j][ith_date_delta] + 1

    # 简单去噪
    for i in range(flavor_type_num):
        avarage_num = float(sum(flavor_num[i])) / float(len(flavor_num[i]))
        for j in range(len(flavor_num[i])):
            if flavor_num[i][j] > 10 * avarage_num and (
                predict_date_start + datetime.timedelta(j)).isoweekday() < 6:
                flavor_num[i][j] = 5 * avarage_num
            if flavor_num[i][j] > 10 * avarage_num and (
                predict_date_start + datetime.timedelta(j)).isoweekday() >= 6:
                flavor_num[i][j] = avarage_num
            if avarage_num > 10 * flavor_num[i][j] and (
                predict_date_start + datetime.timedelta(j)).isoweekday() < 6:
                flavor_num[i][j] = avarage_num
            if avarage_num > 10 * flavor_num[i][j] and (
                predict_date_start + datetime.timedelta(j)).isoweekday() >= 6:
                flavor_num[i][j] = 3 * flavor_num[i][j]


    for index in range(flavor_type_num):
        epsilon = 0.001  # 收敛阈值
        alpha = 0.00002  # 学习率
        tao = 6  # 波长
        testNum = predict_data_delta + 1  # 测试样本个数
        n = 1  # 特征数
        m = (train_date_end - train_date_start).days + 1  # 训练样本个数
        w = []
        for i in range((train_date_end - train_date_start).days + 1):
            w.append(0)

        for i in range(testNum):
            for j in range(m):
                w[j] = math.exp(-float(m + i - j) * float(m + i - j) / float(2 * tao * tao))
            theta = 0
            theta_new = 0

            while 1:
                sum_w_x2 = 0
                sum_w_x_y = 0
                for j in range(m):
                    sum_w_x2 = sum_w_x2 + w[j]*j*j
                    sum_w_x_y = sum_w_x_y + w[j]*j*flavor_num[index][j]
                    pass
                theta_new = (1-alpha*sum_w_x2)*theta + alpha*sum_w_x_y

                if (theta_new - theta) < epsilon:
                    theta = theta_new;
                    break
                else:
                    theta = theta_new;
            flavor_num[index].append((m+i)*theta)
    pass
    predict_flavor_num_jubu = []
    for i in range(flavor_type_num):
        #predict_flavor_num.append(int(1.02*sum(flavor_num[i][-(predict_data_delta+1):])))
        predict_flavor_num_jubu.append(sum(flavor_num[i][-(predict_data_delta + 1):]))
        pass
    for i in range(flavor_type_num):
        if predict_flavor_num_jubu[i]<0:
            predict_flavor_num_jubu[i] = 0

    for i in range(flavor_type_num):
        predict_flavor_num.append(int(1*predict_flavor_num_3_zhishu[i]+0*predict_flavor_num_jubu[i]))

    #predict 输出
    total_flavors_num = 0
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
    r = 0.995
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


def test_vm(test_infor_array,input_lines,predic_result):

    test_data = []
    for item in test_infor_array:
        item_split = item.split('\t')
        item_split[2] = item_split[2].split()[0]
        item_split[2] = datetime.date(int(item_split[2].split('-')[0]), int(item_split[2].split('-')[1]),
                                      int(item_split[2].split('-')[2]))
        test_data.append(item_split)

    server_infor = []
    server_infor.append(int(input_lines[0].split()[0]))
    server_infor.append(int(input_lines[0].split()[1]))
    server_infor.append(int(input_lines[0].split()[2]))

    flavor_type_num = int(input_lines[2])
    flavor_type = []

    for i in range(flavor_type_num):
        flavor_type.append(input_lines[3 + i].split()[0])

    resource_type = input_lines[flavor_type_num + 4].split()[0]

    #统计test里 真实服务器数量
    flavor_num_ground_truth = []
    for i in range(len(flavor_type)):
        flavor_num_ground_truth.append(0)
    for i in range(len(flavor_type)):
        for j in range(len(test_data)):
            if flavor_type[i] == test_data[j][1]:
                flavor_num_ground_truth[i] = flavor_num_ground_truth[i]+1;

    # 解析predict_result 函数
    predict_total_vm = int(predic_result[0])
    predict_flavor_type = []
    predict_flavor_num = []
    for i in range(len(flavor_type)):
        predict_flavor_type.append(predic_result[i+1].split()[0])
        predict_flavor_num.append(int(predic_result[i+1].split()[1]))

    #计算score
    y_score_error = []
    y_score_truth = []
    y_score_predict = []
    for i in range(len(flavor_type)):
        y_score_error.append(0.0)
        y_score_truth.append(0.0)
        y_score_predict.append(0.0)
    for i in range(len(flavor_type)):
        y_score_error[i] = y_score_error[i] + math.pow((flavor_num_ground_truth[i]-predict_flavor_num[i]),2)
        y_score_truth[i] = y_score_truth[i] + math.pow(flavor_num_ground_truth[i],2)
        y_score_predict[i] = y_score_predict[i] + math.pow(predict_flavor_num[i],2)
        pass

    predict_score = 1-(math.sqrt(math.fsum(y_score_error)/len(flavor_type))/(math.sqrt(math.fsum(y_score_truth)/len(flavor_type))+math.sqrt(math.fsum(y_score_predict)/len(flavor_type))))

    put_score = 0.0
    if resource_type == 'CPU':
        total_cpu_resource = server_infor[0]*int(predic_result[len(flavor_type)+2])
        total_cpu_usage = 0
        for i in range(len(flavor_type)):
            total_cpu_usage = total_cpu_usage + flavor_cpu[int(predict_flavor_type[i][6:])-1]*predict_flavor_num[i]
        put_score = float(total_cpu_usage)/float(total_cpu_resource)
    else:
        total_mem_resource = server_infor[0] * int(predic_result[len(flavor_type) + 2])
        total_mem_usage = 0
        for i in range(len(flavor_type)):
            total_mem_usage = total_mem_usage + flavor_mem[int(predict_flavor_type[i][6:])-1] * predict_flavor_num[i]
        put_score = float(total_mem_usage) / float(total_mem_resource)

    final_score = predict_score*put_score*100
    return final_score
