fruits = ['사과','배','배','감','수박','귤','딸기','사과','배','수박']

cnt = 0
for fruit in fruits:
    if fruit == '사과':
        cnt += 1
print('사과는 '+str(cnt)+'개.')

def countFruit(target) :
    cnt2 = 0
    for fruit in fruits:
        if fruit == target:
            cnt2 += 1
    return cnt2
print(countFruit('배'))