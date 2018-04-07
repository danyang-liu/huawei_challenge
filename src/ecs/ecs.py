# coding=utf-8
import sys
import os
import predictor


def main():
    print 'main function begin.'
    if len(sys.argv) != 4:
        print 'parameter is incorrect!'
        print 'Usage: python esc.py ecsDataPath inputFilePath resultFilePath'
        exit(1)
    # Read the input files
    ecsDataPath = sys.argv[1]
    inputFilePath = sys.argv[2]
    resultFilePath = sys.argv[3]

    # ecsDataPath = '../../data/TrainData_2015.1.1_2015.2.19.txt'
    # inputFilePath = '../../data/input_5flavors_cpu_7days.txt'
    # resultFilePath = '../../data/result.txt'
    # testFilePath = '../../data/TestData_2015.2.20_2015.2.27.txt'

    # ecsDataPath = '../../data/train_2016_1.txt'
    # inputFilePath = '../../data/input_2.txt'
    # resultFilePath = '../../data/result.txt'
    # testFilePath = '../../data/test_2016_1.txt'

    ecs_infor_array = read_lines(ecsDataPath)
    input_file_array = read_lines(inputFilePath)
    # implementation the function predictVm
    predic_result = predictor.predict_vm(ecs_infor_array, input_file_array)
    # write the result to output file
    if len(predic_result) != 0:
        write_result(predic_result, resultFilePath)
    else:
        predic_result.append("NA")
        write_result(predic_result, resultFilePath)

    # #test
    # test_infor_array = read_lines(testFilePath)
    # testresult = predictor.test_vm(test_infor_array,input_file_array,predic_result)
    # print testresult


    print 'main function end.'


def write_result(array, outpuFilePath):
    with open(outpuFilePath, 'w') as output_file:
        for item in array:
            output_file.write("%s\n" % item)


def read_lines(file_path):
    if os.path.exists(file_path):
        array = []
        with open(file_path, 'r') as lines:
            for line in lines:
                array.append(line)
        return array
    else:
        print 'file not exist: ' + file_path
        return None


if __name__ == "__main__":
    main()
