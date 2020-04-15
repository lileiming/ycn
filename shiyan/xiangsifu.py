import difflib

def simialr(S1,S2):
    simialr_dict ={}
    def string_similar(s1, s2):
        return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

    for i in S2:
        now_ratio = string_similar(S1,i)
        simialr_dict[i] = now_ratio
    pass
    print(simialr_dict)
    simialr_dict = sorted(simialr_dict.items(), key=lambda simialr_dict: simialr_dict[1],reverse=True)
    return simialr_dict


A ="P2202A"
B =["6200PT2202A","6200PDT2202A","6200LIAC32001","6200PICA2201A"]
#C = ""
C = simialr(A,B)
print(C[0][0],C[1][0],C[2][0])
