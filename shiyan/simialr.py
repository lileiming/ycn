import math

def analysis (Tag):
    temp_char = list(Tag)
    for i in range(len(temp_char)):
        if i+1 <len(temp_char) and temp_char[i].isdigit() and temp_char[i+1].isalpha():
            temp_char.insert(i+1,'_')
        if temp_char[i] == '-' :
            temp_char.insert(i + 1, '_')
        if i+1 <len(temp_char) and temp_char[i].isalpha() and temp_char[i+1].isdigit():
            temp_char.insert(i+1,'_')
    var_New_Tag = ''.join(temp_char)
    return  var_New_Tag.split("_", 2)

def func_noBypass(char1,char2):
    result = False
    if char1 != char2 :
        result = True
    if (char1 =='T') and (char2 =='I') :
        result = False
    if (char1 =='I') and (char2 =='T') :
        result = False
    return result

def func_ratio(short,long):
    ratio = 1.0
    if len(short) > len(long):
        temp_short = list(long)
        temp_long = list(short)
    else:
        temp_short = list(short)
        temp_long = list(long)
    temp_short.extend(["0"] * (len(temp_long) - len(temp_short)))
    temp = (len(temp_long) + len(temp_short))/2
    for i in range(len(temp_long)):
        if func_noBypass(temp_short[i],temp_long[i]):
            ratio = math.sqrt(i/temp)
            print(temp_short[i], temp_long[i], ratio)
            break
    return ratio

def func_simialr(S1,S2):
    S1 = S1
    S2 = S2
    ratio = 1.0
    # print(analysis(S1))
    # print(analysis(S2))
    if analysis(S1)[0] != analysis(S2)[0]:
        ratio = 0.0
    ratio2 = func_ratio(analysis(S1)[1], analysis(S2)[1])
    ratio3 = func_ratio(analysis(S1)[2], analysis(S2)[2])
    print(ratio * ratio2 * ratio3)
    pass

func_simialr("601PICA3456","601PT3456A")
