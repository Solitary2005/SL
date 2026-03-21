import sys
input = sys.stdin.readline

n = int(input())
aph = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
       'a', 'b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
num = ['0','1','2','3','4','5','6','7','8','9']
spe = ['*','#']
for i in range(n):
    pwd = input()
    aph_check = False
    num_check = False
    spe_check = False
    same_check = False
    char_dict = {}
    if len(pwd) >= 6:
        for aph_i in aph:
            if aph_i in pwd:
                aph_check = True
                break
        for num_i in num:
            if num_i in pwd:
                num_check = True
                break
        for spe_i in spe:
            if spe_i in pwd:
                spe_check = True
                break
        for char in pwd:
            counter = char_dict.get(char, 0)
            char_dict[char] = counter + 1
            if char_dict[char] > 2:
                same_check = True # 不符合要求
                break
        
        if aph_check and num_check and spe_check and (not same_check):
            print(2)
        elif aph_check and num_check and spe_check:
            print(1)
        else:
            print(0)
    else:
        raise ValueError