dic = '114514'
points = [0,0,0,0,0,0]#分割字符串指针
aim_number = 0# = 521 #input('输入数字：')
def doit(deep,sum,equation,num):#穷举求和
    if(sum==aim_number):
            print(equation[2:],sum)
    if deep >= len(points):
        return
    else:
        for i,value in enumerate(num):
            doit(deep+1,sum+value,equation + '+' + str(value),num[1:])
            if(sum-value>0):
                doit(deep+1,sum-value,equation + '-' + str(value),num[1:])
            if sum*value != 0:
                doit(deep+1,sum*value,equation+ '*' + str(value),num[1:])
            if(sum/value == int(sum/value) and sum/value != 0):
                doit(deep+1,sum/value,equation + '/' + str(value),num[1:])


def rearrange(dic, points):
    for points[0] in range(5):
        for points[1] in range(5):
            for points[2] in range(5):
                for points[3] in range(5):
                    for points[4] in range(5):
                        for points[5] in range(5):
                            result = []
                            last_index=0
                            if 0 not in points:
                                    result.append(dic[0:points[0]])
                            for i in range(len(points)-1):
                                if points[i]>points[i+1]:
                                    break
                                if points[i]!=points[i+1]:
                                    last_index = i+1
                                    result.append(dic[points[i]:points[i+1]])
                            else:        
                                if 5 not in points:
                                    result.append(dic[points[last_index]:])
                                    int_result = []
                                    for i in result:
                                        int_result.append(int(i))
                                    doit(0,0,' ',int_result)
aim_number = int(input("输入数字："))
rearrange(dic, points)
