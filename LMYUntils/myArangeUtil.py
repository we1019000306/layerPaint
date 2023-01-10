import math

#------------------------计算等差数列的公差-------------------------------------
def caculateUnitStep(maxNum:int,minNum:int)->int:
    # maxNum = int(maxNum)
    # minNum = int(minNum)
    if (maxNum / 1000) % 10 > 1:
        return math.trunc((maxNum / 1000) % 10)*100
    else:
        if (maxNum / 100) % 10 > 1:
            return 50
        else:
            if (maxNum / 10) % 10 > 1:
                if 0 <=maxNum - minNum <10:
                    if 0 <= maxNum <10:
                        return 1
                    elif 10 <=maxNum <20:
                        return 2
                    elif 20 <=maxNum <30:
                        return 5
                    elif 30 <=maxNum <50:
                        return 10
                    elif 50 <=maxNum <100:
                        return 20
                    elif 100 <=maxNum <1000:
                        return 100
                    else:
                        return 10
                elif 10 <= maxNum - minNum <20:
                    return 2
                elif 20 <= maxNum - minNum <30:
                    return 15
                elif 30 <= maxNum - minNum <40:
                    return 10
                elif 40 <= maxNum - minNum < 50:
                    return 10
                elif 50 <= maxNum - minNum < 60:
                    return 10
                elif 60 <= maxNum - minNum < 70:
                    return 20
                elif 70 <= maxNum - minNum < 80:
                    return 20
                elif 80 <= maxNum - minNum < 90:
                    return 20
                elif 90 <= maxNum - minNum < 100:
                    return 10
                elif 100 <= maxNum - minNum < 500:
                    return 10
                elif 500 <= maxNum - minNum < 1000:
                    return 10
            else:
                return 1