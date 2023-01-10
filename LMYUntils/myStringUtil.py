import re

def getImgUrl(url:str)->str:
    for i in url:
        if (i == "\\"):
            url = url.replace('\\','/')
        else:
            pass
    return url

#将字符串中的数字变换成上标
def superscriptNumberWithString(string:str)->str:
    try:
        if re.findall('\d+', string):
            if re.findall('\-\d+', string):
                string = string.replace(re.findall('\-\d+', string)[0], ('$^{%-d}$') % int(re.findall('\-\d+', string)[0]))
                return string
            elif re.findall('\d+', string):
                string = string.replace(re.findall('\d+', string)[0], ('$^{%d}$') % int(re.findall('\d+', string)[0]))
                return string
            else:
                return string
        else:
            return string
    except IndexError:
        return string

    else:
        return string

def deleteBlankStringWithString(string:str)->str:
    try:
        if re.findall('\n', string):
            string = string.replace(re.findall('\n', string)[0], '')
            return string
        else:
            return string
    except IndexError:
        return string

    else:
        return string

def deleteBlankStringWithList(stringList:list)->list:
    newStringList = []
    for i in  stringList:
        try:
            if re.findall('\n', i):
                i = i.replace(re.findall('\n', i)[0], '')
                newStringList.append(i)
                #print(i)
            else:
                newStringList.append(i)

        except IndexError:

            pass

        else:

            pass

    return newStringList

def isChinese(string:str)->bool:
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def isNumber(string:str)->bool:
    """
    检查整个字符串是否都可以转换为数字
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u0030' <= ch <= u'\u0039':
            pass
        elif u'\u002e' == ch:
            pass
        else:
            return False
    return True