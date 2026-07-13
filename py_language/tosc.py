# #문제 1
# N = int(input())
# a = int(input())
# b = int(input())
# c = int(input())

# answer = 0

# while True:
#     N = N - a

#예상문제1

# a = int(input())
# b = int(input())

# c = 0
# d = 0
# if a == 1:
#     d = 60
# elif a == 2:
#     d = 100
# elif a == 3:
#     d = 120

# if b == 1:
#     c = 100
# elif 2<=b<=5:
#     c = 50
# elif 6<=b<=10:
#     c = 25
# elif 11<=b<=20:
#     c = 10
# else:
#     c = 5

# print(int(c*d/100))

#예상문제문제3 3급

# answer = 0
# lst = []
# while answer <= 300:
#     a = int(input())
#     b = int(input())

#     c = 0
#     d = 0
#     if a == 1:
#         d = 60
#     elif a == 2:
#         d = 100
#     elif a == 3:
#         d = 120

#     if b == 1:
#         c = 100
#     elif 2<=b<=5:
#         c = 50
#     elif 6<=b<=10:
#         c = 25
#     elif 11<=b<=20:
#         c = 10
#     else:
#         c = 5

#     lst.append(a)
#     answer += int(c*d*lst.count(a)/100)

# print(answer)


##문제 1번 3급문제

# a = int(input())
# first = int(input())
# sum = 0
# count = 0
# lst = []
# group = 0
# while sum < 24:
#     ipt = int(input())
#     sum += ipt
#     count += 1
#     if sum >= a:
#         if first == 1:
#             if count % 2 == 1:
#                 answer = "A"
#             else:
#                 answer = "B"
#         elif first == 2:
#             if count % 2 == 1:
#                 answer = "A"
#             else:
#                 answer = "B"
#     group += 1

# print(answer)
# print(group//2)


##문제 2번 3급문제
# lst = [0, 0, 0]
# def active_hour(active_num, person):
#     global lst
#     num = {1 : 60, 2 : 100, 3 : 120}
#     ratio = 0
#     if person == 1:
#         ratio = 1
#     elif 2 <= person <= 5:
#         ratio = 0.5
#     elif 6 <= person <= 10:
#         ratio = 0.25
#     elif 11 <= person <= 20:
#         ratio = 0.1
#     else:
#         ratio = 0.05
    
#     lst[active_num - 1] += 1
#     return num[active_num] * ratio * lst[active_num - 1]

# answer = 0
# while True:
#     a = int(input())
#     b = int(input())
#     answer += active_hour(a, b)
#     if answer > 300:
#         print(int(answer))
#         break


## 문제 3번 3급문제
# lst = []
# lst_del = []
# out = 0
# score = 0
# first = 0
# while out < 3:
#     ipt = int(input())
#     if ipt == 0:
#         out += 1
#     elif ipt == 5:
#         score += len(lst)
#         lst = []
#     else:
#         lst.append(ipt)
#         if first == 0:
#             first += 1
#             continue
#         else:
#             for x in range(len(lst)):
#                 lst[x] += ipt
#             for val in lst:
#                 if val >= 5:
#                     score += 1
                   
# print(score)


##문제 4번 3급문제
def elec_fee(time):
    if 0 <= time <= 3:
        return 80
    elif 4 <= time <= 7:
        return 100
    elif 8 <= time <= 11:
        return 200
    elif 12 <= time <= 15:
        return 300
    elif 16 <= time <= 19:
        return 150
    else:
        return 100
    
total_elec = int(input())
sum = 0
max = 0
total = 0
while total <= total_elec:
    a = int(input())
    b = int(input())
    fee = elec_fee(a) * 100
    if fee > max:
        max = a
    sum += fee
    total += b
print(max)
print(sum)
