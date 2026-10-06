# coal = 20 * 3
# dia = 150 * 3

# dia_count = int(input("Number of diamond = "))
# coal_count = int(input("Number of coal = "))

# print(f"savings = {coal*coal_count + dia * dia_count}")


# dia = 100 * 3

# a = int(input("Number of diamond = "))
# print(f"{a} left")
# sold = 0
# while a > 0:
#     b = int(input("Number of diamond to buy = "))
#     if b > a:
#         continue
#     sold += b
#     a -= b
#     if a > 0:
#         print(f"{a} left")

# print(f"savings = {sold*dia}")


# sum = 0
# cnt = 0
# while cnt < 10:
#     a = int(input())
#     if a != 5:
#         sum += a
#         cnt += 1
#     else:
#         break

# print(f"Sum = {sum}")


# a = 0
# b = 0

# diamond = 100
# rate = 3

# a = int(input("Number of diamond = "))
# while a > 0:
#     print(a, "left")
#     c = int(input("Number of diamond to buy = "))
#     a = a - c
#     b = b + c * rate * diamond

# savings = b
# print("savings =", savings)

# num = 0
# total = 0

# while total < 100:
#     num = num + 7
#     total = total + num

# print(num)

##과제1 1번
# origin_fee = 30000
# age = int(input())
# time = int(input())
# rate = 1
# fee = 1
# if age < 8:
#     fee = 0
# elif 8 <= age <= 18:
#     rate = 0.8
# elif age >= 65:
#     rate = 0.5

# if time >= 17:
#     rate *= 0.7

# print(int(origin_fee * fee * rate))

##과제1 2번
# N = int(input())
# M = int(input())

# rate = 0
# if M == 1:
#     rate = 1
# elif 2 <= M <= 5:
#     rate = 0.5
# elif 6 <= M <= 10:
#     rate = 0.25
# elif 11 <= M <= 20:
#     rate = 0.1
# else:
#     rate = 0.05

# time = 0
# if N == 1:
#     time = 60
# elif N == 2:
#     time = 100
# else:
#     time = 120

# print(int(time*rate))

# cnt_dia = int(input("Number of diamond = "))
# money = 0

# while 1:
#     print(cnt_dia, "left")
#     sell = int(input("Number of diamond = "))
    
#     if sell > cnt_dia:
#         print("X")
#     elif sell <= cnt_dia:
#         cnt_dia -= sell
#         money += sell * 300
    
#     if cnt_dia == 0:
#         break

# print("savings = ", money)


# a = int(input("Number of diamond = "))
# dia_fee = 120 * 2
# for x in range(1, a+1):
#     print("now =", x)
# print("savings =", dia_fee*a)

# a = int(input())
# b = int(input())

# for x in range(a, b+1):
#     for y in range(1, 10):
#         print(x,"x",y,"=",x*y)


# a = 9860
# n = int(input())
# print(n * a)

# h = int(input())
# a = (h - 100) * 0.9
# print(int(a))

# a = int(input())
# b = int(input())
# a = a / 100
# b = b / 100
# c = a * b / 3.3
# print("Area = %.4f" %c)

# a = int(input())
# b = int(input())
# c = (a*a  + b*b)**0.5
# print("c = %.4f" %c)

# onion = 800000 / 1000
# carrot = 550000 / 1000
# pumpkin = 280000 / 1000

# a = int(input())
# b = int(input())
# c = int(input())
# print(int(a * onion + b * carrot + c * pumpkin))

# a = int(input())
# b = int(input())
# n = int(input())

# print("Result = %02d:%02d" %((a+n) % 12, b))

# a = int(input())
# b = int(input())
# print("> :", a > b)
# print("< :", a < b)
# print("== :", a == b)

# a = int(input())
# print(a >= 8 and a != 10)

# a = int(input())
# print("Buy Gift")
# if a - 3000 > 1500:
#     print("Buy Drink")
#     print("Money =", a - 3000 - 1500)
# else:
#     print("Money =", a - 3000)

# a = int(input())
# b = int(input())
# print("Sum =", a+b)
# if a == b:
#     print("Double!")

# a = int(input())
# b = int(input())
# c = int(input())
# d = int(input())
# print(a*8 + b * 4 + c * 2 + d)

# a, b, c = [int(input()) for _ in range(3)]
# lst = [a, b, c]
# lst = sorted(lst)
# print(lst[1])

# a = int(input())
# if a >= 20:
#     b = 3000
# else:
#     b = 2000
# print("Money =", b)

# a = int(input())
# b = int(input())
# c = int(input())
# if a**2 + b**2 == c**2:
#     print("OK")
# else: print("NO")

# a = int(input())
# b = int(input())
# c = int(input())
# score = a*0.1 + b * 0.2 + c * 0.7
# print("Score = %.1f" %score)
# if score >= 60: print("PASS")
# else: print("FAIL")

# a = int(input())
# if a == 0: print("0")
# elif a > 0: print("1")
# else: print("-1")

# lst1 = [3000, 4000, 5000]
# lst2 = [4000, 6000, 8000]
# lst3 = [2000, 3500, 5500]
# lst = [lst1, lst2, lst3]
# a = int(input())
# b = int(input())
# if b < 7: c = 0
# elif b < 14: c = 1
# else: c = 2
# print(lst[a-1][c])

# a = int(input())
# b = int(input())
# b /= 60
# speed = a / b
# print("Speed : %.3f km/h" %speed)
# if speed >= 80: print("Fast")
# elif speed <= 30: print("Slow")
# else: print("Normal")

# sum = 0
# while True:
#     a = int(input())
#     if a == -1:
#         break
#     sum += a
# print(sum)

# a = int(input())
# b = 0
# while a > 0:
#     a//=10
#     b += 1
# print(b)

# sum = 0
# cnt = 0
# while sum < 20:
#     a = int(input())
#     sum += a
#     cnt += 1
# print("Total =", sum)
# print("Count =", cnt)

# sum = 0
# cnt = 0
# while sum < 20:
#     a = int(input())
#     sum += a
#     cnt += 1
#     if a == 4:
#         break
# print("Total =", sum)
# print("Count =", cnt)

# a = int(input())
# cnt = 0
# for x in range(1, a+1):
#     if a % x == 0: cnt+=1
# print(cnt)

# sum = 0
# cnt = 0
# for x in range(5):
#     a = int(input())
#     sum += a
#     cnt += 1
#     if a % 2 == 0: break
# print("Total =", sum)
# print("Count =", cnt)

# a = int(input())
# b = int(input())
# cnt = 1
# while cnt % a != 0 or cnt % b != 0:
#     cnt+=1
# print(cnt)

# o = 0
# x = 0
# while True:
#     a = input()
#     if a == 'Finish': break
#     if a == 'O': o+=1
#     if a == 'X': x+=1
# print("O :", o)
# print("X :", x)
# print("Rate : %.2f%%" %(o / (o + x) * 100))

# n = int(input())
# sum = 0
# for x in range(1, n+1):
#     sum += x
# print(sum)

# a = int(input())
# b = int(input())
# for x in range(a, b+1):
#     if x % 2 == 0:
#         print(x, "EVEN")
#     else:
#         print(x, "ODD")

# n = int(input())
# sum = 0
# for x in range(n):
#     a = int(input())
#     sum += a
# print(sum * 5)

# a = int(input())
# b = int(input())
# for x in range(a, b+1):
#     if x % 3 == 0:
#         print("%02d:00 ALARM" %x)
#     else:
#         print("%02d:00" %x)

# n = int(input())
# total = 0
# for x in range(n):
#     a = int(input())
#     total += a
# print("Total :", total)

# n = int(input())
# total = 0
# for x in range(n):
#     a = int(input())
#     total += a
#     if a == 0: break
# print("Total :", total)

# n = int(input())
# for x in range(1, n+1):
#     for y in range(1, 10):
#         print(x, "x", y, "=", x*y)

# n = int(input())
# for x in range(1, n+1):
#     print("*" * x)

# n = int(input())
# m = int(input())
# a1 = int(input())
# a2 = int(input())
# b1 = int(input())
# b2 = int(input())
# c1 = int(input())
# c2 = int(input())

# for x in range(1, n+1):
#     for y in range(1, m+1):
#         if (x, y) == (a1, a2) or (x, y) == (b1, b2) or (x, y) == (c1, c2):
#             print("X", end ="")
#         else:
#             print("O", end = "")
#     print()

# N = int(input())
# for x in range(N, 0, -1):
#     print("*" * x)

# name = ['diamond', 'ruby', 'saphire', 'emerald']
# a = []
# cost = [100, 60, 80, 30]
# NUM_JEWEL = 4
# for x in range(NUM_JEWEL):
#     ipt = int(input())
#     a.append(ipt)

# sum = 3 * (cost[0] * a[0] + cost[1] * a[1] + cost[2] * a[2] + cost[3] * a[3])
# print("Total sales =", sum)

# def sign(n):
#     if n > 0: return 1
#     elif n < 0: return -1
#     else: return 0

# a = int(input())
# print(sign(a))

# def gcd(a, b):
#     if a < b:
#         min = a
#     else: min = b
#     for x in range(1, min+1):
#         if a % x == 0 and b % x == 0:
#            ans = x
#     return ans

# a = int(input())
# b = int(input())
# print(gcd(a, b))

# def abs(a):
#     if a < 0: return -a
#     return a

# n = int(input())
# sum = 0
# for x in range(n):
#     ipt = float(input())
#     sum += abs(ipt)
# print("Total : %.2f" %sum)

# lst = []
# sum = 0
# while len(lst) < 5:
#     a = int(input())
#     if a % 5 == 0: lst.append(a)
#     sum += a

# print(lst)
# print("Total : %d" %sum)

# def get_digit_sum(n):
#     sum = 0
#     while n > 0:
#         sum += n % 10
#         n = int(n / 10)
#     return sum

# a = int(input())
# b = int(input())

# a_ait = get_digit_sum(a)
# b_ait = get_digit_sum(b)

# if a_ait > b_ait:
#     print("Sejong Win")
# elif a_ait < b_ait:
#     print("Daeyang Win")
# else:
#     print("Draw")

# def isPrime(n):
#     if n < 2:
#         return 0
#     for x in range(2, n):
#         if n % x == 0:
#             return 0
#     return 1

# a = int(input())
# if isPrime(a) == 0:
#     print(a, "is not a prime number.")
# else:
#     print(a, "is a prime number.")

# def print_abs_max(a, b, c):
#     lst = [a, b, c]
#     mx = lst[0]
#     for x in lst:
#         if abs(x) > abs(mx):
#             mx = x
#     print(mx)

# def print_abs_min(a, b, c):
#     lst = [a, b, c]
#     mn = lst[0]
#     for x in lst:
#         if abs(x) < abs(mn):
#             mn = x
#     print(mn)

# a = int(input())
# b = int(input())
# c = int(input())
# print_abs_max(a, b, c)
# print_abs_min(a, b, c)

# def cnt(b, a):
#     bisonsu = [3, 4, 5, 6, 7, 10, 11, 12]
#     sonsu = [1, 2, 8, 9]
#     if a in bisonsu:
#         if b == 1:
#             return [5000, 500]
#         elif b == 2:
#             return [15000, 2000]
#         elif b == 3:
#             return [30000, 5000]
#     elif a in sonsu:
#         if b == 1:
#             return [8000, 500]
#         elif b == 2:
#             return [20000, 2000]
#         elif b == 3:
#             return [45000, 5000]

# n = int(input())
# sum = 0
# mile = 0
# for x in range(n):
#     a = int(input())
#     b = int(input())
#     ans = cnt(a, b)
#     sum += ans[0]
#     mile += ans[1]

# print(sum)
# print(mile)

# def cnt(a):
#     max = 0
#     length = 0
#     for x in range(len(a)-1):
#         if a[x] == a[x+1] == 'O':
#             length += 1
#         else:
#             if length >= max:
#                 max = length+1
#                 length = 0
#     if length > 0:
#         if length >= max:
#                 max = length+1
#                 length = 0
#     if max != 0:
#         return max+1
#     else: return max


# a = input()
# print(cnt(a))

# NUM_JEWEL = 3
# Name = ['diamond', 'ruby', 'emerald']
# Cost = [100, 60, 30]

# count = []
# input_name = []
# for x in range(3):
#     a = int(input())
#     count.append(a)
# for x in range(3):
#     a = input()
#     input_name.append(a)

# total_sale = 0
# total_cost = 0
# for x in range(3):
#     index = Name.index(input_name[x])
#     total_sale += count[index] * Cost[index] * (x + 2)
#     total_cost += count[index] * Cost[index]
# print("Total sales =", total_sale)
# print("Total costs =", total_cost)


# n = int(input())
# a = int(input())
# b = int(input())

# lst1 = []
# lst2 = []
# for x in range(1, n+1):
#     lst1.append(x)
# for x in range(a+1, b+2):
#     lst2.append(x)
# print(lst1)
# print(lst2)


# n = int(input())
# a = []
# b = []
# for x in range(1, n+1):
#     a.append(x*x)
#     if (x * x) % 3 == 0:
#         b.append(x*x)
# print(a)
# print(b)

# lst = []
# while True:
#     a = int(input())
#     if a == 0: break
#     lst.append(a)

# print(lst)

# x = max(lst)
# while x in lst:
#     lst.remove(max(lst))
# x = min(lst)
# while x in lst:
#     lst.remove(min(lst))
# print(lst)

# n = int(input())
# m = int(input())

# lst = []
# lst_temp = []
# for x in range(n):
#     for y in range(m):
#         ipt = int(input())
#         lst_temp.append(ipt)
#     lst.append(lst_temp)
#     lst_temp = []
# print(lst)

# n = int(input())
# m = int(input())
# lst = []
# for x in range(n):
#     ipt = list(map(int, input().split()))
#     lst.append(ipt)

# ans = 0
# for x in range(n):
#     for y in range(m):
#         if y == 0:
#             if m == 1:
#                 ans += 1
#             elif lst[x][y] > lst[x][y+1]:
#                 ans += 1
#         elif y == m-1:
#             if lst[x][y] > lst[x][y-1]:
#                 ans += 1
#         else:
#             if lst[x][y] > lst[x][y-1] and lst[x][y] > lst[x][y+1]:
#                 ans += 1
# print(ans)

# n = int(input())
# lst = []
# for x in range(n):
#     a = []
#     for y in range(n):
#         a.append((x + 1) * (y+1))
#     lst.append(a)
# print(lst)

# dic = {"OS": "Operating System", "CG": "Computer Graphics", "DB": "Data Base",
# "ML": "Machine Learning"}

# for x in range(3):
#     a = input()
#     if a in dic:
#         print(dic[a])
#     else:
#         print("NOT EXIST!")

# filename = input()
# N = int(input())
# M = int(input())

# f = open(filename, 'w')
# for x in range(N, M+1):
#     f.write(str(x) + ' ')
# f.close()

# f = open(filename, 'r')
# print(f.read())
# f.close()


# f = open("text.txt", 'w')
# f.write("Hello, This is Python Programming.")
# f.close()

# f = open("text.txt", 'r')
# ipt = int(input())
# print(f.read(ipt))
# f.close()

# lst = []
# for x in range(10):
#     a = input()
#     if a in lst:
#         lst.remove(a)
#     else:
#         lst.append(a)
# lst.sort()
# for x in lst:
#     print(x)

# N = int(input())
# info = {}
# for x in range(N):
#     key = input()
#     value = input()
    
#     info[key] = value

# s = input()
# print(info[s])

# dic = {}
# N = int(input())
# for x in range(N):
#     ipt = input().split()
#     key = ipt[0]
#     value = int(ipt[1])
#     if key in dic:
#         dic[key] += value
#     else:
#         dic[key] = value
# a = input()
# if a in dic:
#     print(dic[a])
# else:
#     print(0)


# N = int(input())
# count = 0
# dic = {}
# for x in range(N):
#     key = input()
#     value = input()
#     if key not in dic:
#         count += 1
#     dic[key] = value
# total = 0
# for key, value in dic.items():
#     total += int(value)
# print("Count :", count)
# print("Total :", total)

#2 0 // 6 3 // 10 5
# N = int(input())
# total = 0
# total_a = 0
# total_b = 0
# total_c = 0
# sum = 0
# for x in range(N):
#     a = int(input())
#     b = int(input())
#     c = int(input())

#     if sum > 30:
#         total += a * 1 + b * 3 + c * 5
#     else:
#         total += a * 2 + b * 6 + c * 10
#     sum += a + b + c
#     total_a += a
#     total_b += b
#     total_c += c
# if total_a + total_b + total_c > 30:
#     total += total_b * 3 + total_c * 5
# print(total)


# y = int(input())
# m = int(input())
# d = int(input())
# day_lst = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# standard = y * 365 + sum(day_lst[:m-1]) + d
# N = int(input())
# for x in range(N):
#     a = input()
#     if len(a) == 4:
#         a = int(a)
#         b = int(input())
#         c = int(input())
#     else:
#         b = int(a[4:6])
#         c = int(a[6:8])
#         a = int(a[0:4])

#     input_standard = a * 365 + sum(day_lst[:b-1]) + c
#     if input_standard < standard:
#         print("Error")
#     elif input_standard >= standard:
#         print(input_standard - standard)

# main = [5000, 5500, 6500, 7000, 6800]
# toping = [1000, 1200, 800, 1100, 1050, 1150, 900, 600, 750]
# dressing = [300, 300, 250, 500, 400, 500, 0]
# beverage = [2000, 1800, 500]

# N = int(input())
# total = 0
# for x in range(N):
#     main_ipt = int(input())
#     toping1_ipt = int(input())
#     toping2_ipt = int(input())
#     dressing_ipt = int(input())
#     beverage_ipt = int(input())
#     total += main[main_ipt-1] + toping[toping1_ipt-1] + toping[toping2_ipt-1] + dressing[dressing_ipt-1] + beverage[beverage_ipt-1]

# print("-----HongSalad-----")
# print("Salad Qty:" + str(N))
# print("-------------------")
# print("Total Price:%.0f" %(total * 10 / 11))
# print("Tax(10%%):%.0f" %(total / 11))
# print("-------------------")
# print("Total:", total)

# attendance = int(input("attendance = "))
# assignment = int(input("assignment = "))
# midterm = int(input("midterm = "))
# final = int(input("final = "))
# sum = attendance * 0.1 + assignment * 0.2 + midterm * 0.3 + final * 0.4
# print("Sum = %d" %sum)
# if sum >= 60:
#     print("PASS")
# else:
#     print("FAIL")

# filename = input()
# N = int(input())
# M = int(input())

# f = open(filename, 'w')
# for x in range(N, M+1):
#     f.write(str(x) + ' ')
# f.close()

# f = open(filename, 'r')
# print(f.read())
# f.close()

# dic = {"blue": 2000, "black": 3000, "yellow": 5000}
# a = int(input())
# ans = 0
# for x in range(a):
#     ipt = input()
#     if ipt in dic:
#         ans += dic[ipt]
# if ans >= 30000:
#     print(int(ans * 0.95))
# else: print(int(ans))

# a = int(input())
# lst = []
# lst2 = []
# for x in range(a):
#     ipt = int(input())
#     lst.append(ipt)
#     if ipt not in lst2:
#         lst2.append(ipt)
# print(lst)
# print(lst2)

# a = int(input())
# ans = 0
# for x in range(a):
#     ipt = input()
#     lst = list(ipt)
#     for y in range(int(len(lst)/2)):
#         if lst[y] != lst[-y - 1]:
#             ans += 1
#             break
# print(a - ans)

# lst = []
# judge = 0
# while True:
#     a = int(input())
#     if a == 5: break
#     if a == 1 and judge == 0:
#         ipt = input()
#         lst.append(ipt)
#     if a == 1 and judge == 1:
#         print("Waiting End")
#     if a == 2:
#         print(lst[0])
#         lst.pop(0)
#     if a == 3:
#         judge = 1
#     if a == 4:
#         print(lst)

# N = int(input())
# participants = []

# for _ in range(N):
#     data = input().split()
#     name = data[0]
#     s1, s2, s3 = int(data[1]), int(data[2]), int(data[3])
#     total = s1 + s2 + s3
#     participants.append([name, s1, s2, s3, total])

# participants.sort(key=lambda x: (- x[4], - x[1], -x[2], x[0]))

# for p in participants:
#     print(p[0], p[4])

# lst = []
# for x in range(6):
#     ipt = int(input())
#     lst.append(ipt)
# judge = 0
# probability = []
# for x in range(6):
#     probability.append(lst[x] / sum(lst) * 100)
#     if lst[x] / sum(lst) * 100 >= 30:
#         judge = 1
#     print("%d: %.3f" %(x+1, probability[x]))

# if judge == 1:
#     print("Problem at %d" % (probability.index(max(probability)) + 1))
#     print("Result: %.3f %%" %max(probability))

# else:
#     print("Fair")


# import random
# N = int(input())
# M = int(input())

# sum = 0;
# for x in range(50):
#     a = random.randint(N, M)
#     sum += a
#     print(a)
# print("Avg : %.2f" %(sum / 50))

# import webbrowser
# url = input("")
# webbrowser.open("https://www.google.com/search?q=" + url)

# print('"https://www.google.com/search?q=' + url + '"')


# import matplotlib.pyplot as plt

# N = int(input())
# x = [i for i in range(-N, N+1)]
# y = [i**2 for i in range(-N, N+1)]

# plt.plot(x, y, color='red')
# plt.title('y = x^2')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.show()


# import matplotlib.pyplot as plt
# a = int(input())
# b = int(input())
# x = [x for x in range(-10, 11)]
# y = [a * x + b for x in range(-10, 11)]

# plt.plot(x, y, color = 'red')
# plt.title('y = ax + b')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.show()

# time_lucidity = [10, 15, 20]
# time_rain = [15, 20, 25]
# course1 = [1, 2, 1]
# course2 = [3, 3, 2]
# total_distance = 0
# ans = 0
# N = int(input())
# for x in range(N):
#     mountain = int(input())
#     course = int(input())
#     weather = int(input())
#     distance = int(input())
#     if total_distance >= 20:
#         if weather == 1:
#             if course == 1:
#                 ans += ((time_lucidity[course1[mountain-1] - 1] - 2) * distance)
#             elif course == 2:
#                 ans += ((time_lucidity[course2[mountain-1] - 1] - 2) * distance)
#         elif weather == 2:
#             if course == 1:
#                 ans += ((time_rain[course1[mountain-1] - 1] - 2) * distance)
#             elif course == 2:
#                 ans += ((time_rain[course2[mountain-1] - 1] - 2) * distance)
#     else:
#         if weather == 1:
#             if course == 1:
#                 ans += (time_lucidity[course1[mountain-1] - 1] * distance)
#             elif course == 2:
#                 ans += (time_lucidity[course2[mountain-1] - 1] * distance)
#         elif weather == 2:
#             if course == 1:
#                 ans += (time_rain[course1[mountain-1] - 1] * distance)
#             elif course == 2:
#                 ans += (time_rain[course2[mountain-1] - 1] * distance)
    
#     total_distance += distance
# print(ans)


# def score(a, b, c, d):
#     lst = [a, b, c, d]
#     lst.sort()
#     lst_set = list(set(lst))
#     if (len(lst_set) == 1):
#         return 40
#     elif (lst[0] + 1 == lst[1] and lst[1] + 1 == lst[2] and lst[2] + 1 == lst[3]):
#         return 30
#     elif ((lst[0] + 1 == lst[1] and lst[1] + 1 == lst[2]) or
#           (lst[1] + 1 == lst[2] and lst[2] + 1 == lst[3])):
#         return 15
#     elif (len(lst_set) == 2):
#         if lst.count(lst[0]) == 2:
#             return 25
#         elif lst.count(lst[0]) == 1 or lst.count(lst[0]) == 3:
#             return 20
#     elif (len(lst_set) == 3):
#         return 10
#     else:
#         return 0
    
# a = int(input()); b = int(input()); c = int(input()); d = int(input())
# print(score(a, b, c, d))

# N = int(input())
# lst = []
# for x in range(N):
#     a = int(input())
#     lst.append(a)
# print(lst)
# lst.reverse()
# print(lst)

# N = int(input())
# lst = []
# for x in range(N):
#     a = int(input())
#     lst.append(a)
# print("Max =", max(lst))
# print("Pos =", lst.index(max(lst)))

# N = int(input())
# lst = []
# for x in range(2):
#     lst2 = []
#     for y in range(N):
#         a = int(input())
#         lst2.append(a)
#     lst.append(lst2)
# for x in range(N):
#     print("%.1f" %((lst[0][x] + lst[1][x]) / 2))

# N = int(input())
# lst = []
# for x in range(N):
#     a = int(input())
#     lst.append(a)
# lst.remove(max(lst))
# lst.remove(min(lst))
# print(lst)

# def sign(N):
#     if N > 0: return 1
#     elif N < -0: return -1
#     return 0
# a = int(input())
# print(sign(a))

# def gcd(a, b):
#     for x in range(a, 0, -1):
#         if a % x == 0 and b % x == 0: return x
# a = int(input())
# b = int(input())
# print(gcd(a, b))

# N = int(input())
# ans = 0
# for x in range(N):
#     a = float(input())
#     ans += abs(a)
# print("Total : %.2f" %ans)

# lst = []
# total = 0
# while (len(lst) < 5):
#     a = int(input())
#     if a % 5 == 0: lst.append(a)
#     total += a
# print(lst)
# print("Total : %d" %total)

# def get_digit_sum(a):
#     ans = 0
#     while a > 0:
#         ans += a % 10
#         a = int(a / 10)
#     return ans
# a = int(input())
# b = int(input())
# a2 = get_digit_sum(a)
# b2 = get_digit_sum(b)
# if a2 > b2: print("Sejong Win")
# elif a2 < b2: print("Daeyang Win")
# else: print("Draw")

# N = int(input())
# lst = [x+1 for x in range(N)]
# a = int(input())
# b = int(input())
# lst2 = [x+1 for x in range(a, b+1)]
# print(lst)
# print(lst2)

# N = int(input())
# lst = [(x+1)**2 for x in range(N)]
# lst2 = []
# for x in lst:
#     if x % 3 == 0:
#         lst2.append(x)
# print(lst)
# print(lst2)

# lst = []
# while True:
#     a = int(input())
#     if a == 0: break
#     lst.append(a)
# print(lst)
# a = max(lst)
# while a in lst:
#     lst.remove(max(lst))
# a = min(lst)
# while a in lst:
#     lst.remove(min(lst))
# print(lst)

# N = int(input())
# M = int(input())
# lst = [[0 for _ in range(M)] for _ in range(N)]
# for x in range(N):
#     for y in range(M):
#         a = int(input())
#         lst[x][y] = a
# print(lst)

# N = int(input())
# M = int(input())
# lst = []
# ans = 0
# for x in range(N):
#     a = list(map(int, input().split()))
#     lst.append(a)
# for x in range(N):
#     for y in range(M):
#         if M == 1:
#             ans += 1
#         elif y == 0:
#             if lst[x][0] > lst[x][1]:
#                 ans += 1
#         elif y == M - 1:
#             if lst[x][-1] > lst[x][-2]:
#                 ans += 1
#         elif lst[x][y] > max(lst[x][y - 1], lst[x][y+1]):
#             ans += 1
# print(ans)

# N = int(input())
# dic = {}
# for x in range(N):
#     a = input()
#     b = input()
#     dic[a] = b
# ipt = input()
# print(dic[ipt])

# lst = []
# for x in range(10):
#     a = input()
#     if a in lst:
#         lst.remove(a)
#     else:
#         lst.append(a)
# lst.sort()
# for x in lst:
#     print(x)

# dic = {}
# N = int(input())
# for x in range(N):
#     a, b = input().split()
#     b = int(b)
#     if a in dic:
#         dic[a] += b
#     else:
#         dic[a] = b
# ipt = input()
# if ipt not in dic:
#     print(0)
# else:
#     print(dic[ipt])

# N = int(input())
# lst = []
# for x in range(N):
#     a = input()
#     lst.append(a)
# ans = 0
# for x in lst:
#     if x == 'blue':
#         ans += 2000
#     elif x == 'black':
#         ans += 3000
#     elif x == 'yellow':
#         ans += 5000

# if ans >= 30000:
#     print("%d" %(ans * 0.95))
# else:
#     print(ans)

# N = int(input())
# lst = []
# for x in range(N):
#     a = int(input())
#     lst.append(a)
# print(lst)

# lst2 = []
# for x in lst:
#     if x not in lst2:
#         lst2.append(x)
# print(lst2)

# def asdf(a):
#     for x in range(len(a)):
#         if a[x] != a[len(a) - 1 - x]:
#             return 0
#     return 1

# a = int(input())
# ans = 0
# for x in range(a):
#     ipt = input()
#     ans += asdf(ipt)
# print(ans)

# lst = []
# judge = 1
# while True:
#     a = int(input())
#     if a == 5:
#         break
#     elif a == 1 and judge == 1:
#         ipt = input()
#         lst.append(ipt)
#     elif a == 2:
#         print(lst[0])
#         lst.pop(0)
#     elif a == 3:
#         judge = 0
#     elif a == 4:
#         print(lst)
#     elif a == 1 and judge == 0:
#         print("Waiting End")

# lst = []
# N = int(input())
# for x in range(N):
#     a, b, c, d = input().split()
#     b = int(b); c = int(c); d = int(d)
#     total = b + c + d
#     lst.append([a, b, c, d, total])

# lst.sort(key = lambda x:(-x[4], -x[1], -x[2], x[0]))
# for x in lst:
#     print(x[0], x[-1])


# a = int(input())
# cnt = 1
# while True:
#     if ((6 * cnt) % a) == 0:
#         print(cnt)
#         break
#     cnt+=1

# lst = []
# a = int(input())
# for x in range(a):
#     ipt = input()
#     lst.append(ipt)
# if lst.count("sejong") >= a - 2:
#     print("Yes")
# else:
#     print("No")

# a = int(input())
# for x in range(1, a+1):
#     for y in range(1, a+1):
#         if x == 1:
#             print("F", end = "")
#         elif x == 2:
#             print(".", end = "")
#         else:
#             print("M", end = "")
#     print()

# import sys
# a = list(input())
# lst = []
# if "E" in a and "A" in a and "S" in a and "Y" in a:
#     if (a.index("E") < a.index("A")) and (a.index("A") < a.index("S") and (a.index("S") < a.index("Y"))):
#         for x in range(a.index("E"), a.index("A")+1):
#             lst.append(a[x])
#         for x in range(a.index("A"), a.index("S")+1):
#             lst.append(a[x])
#         for x in range(a.index("S"), a.index("Y")+1):
#             lst.append(a[x])
#     lst2 = list(set(lst))
#     for x in lst2:
#         if lst.count(x) >= 2:
#             print("NO")
#             sys.exit()
#     print("YES")
# else:
#     print("NO")


# a1, a2 = map(int, input().split())
# b1, b2 = map(int, input().split())
# c1, c2 = map(int, input().split())

# if a1 + a2 == 7 or b1 + b2 == 7 or c1 + c2 == 7:
#     print("No")
# else:
#     print("Yes")

# N, K = map(int, input().split())
# a = list(map(int, input().split()))
# a.sort()
# #큰거 K고르면?... 1, 2, 3 -> 1, 2, 6
# #작은거 ... 1, 2, 3 -> 6, 2, 3 -->> 이게 정답
# #최대 = 큰 수 + 안고른거 합, 최소 = a[0]
# ans1 = a[N-1] + sum(a[:N-K]) - a[0]
# #최대 = a[K-1] + 안고른거 합, 최소 = a[K]
# ans2 = a[K-1] + sum(a[K:]) - a[K]
# print(min(ans1, ans2))

# n = int(input())
# a = [0] * (n + 1)
# b = [[] for _ in range(n + 1)]

# for x in range(n - 1):
#     u, v = map(int, input().split())
#     b[u].append(v); b[v].append(u)
#     a[u] += 1; a[v] += 1

# L = 0
# for v in range(1, n + 1):
#     if a[v] == 1:
#         L += 1

# out = []
# for i in range(1, n + 1):
#     r = L
#     if a[i] == 1:
#         r -= 1
#     for u in b[i]:
#         if a[u] == 1:
#             r -= 1
#         elif a[u] == 2:
#             r += 1
#     out.append(r)

# for x in out:
#     print(x)



# s = input()
# piece = [("", "EASY"), ("E", "ASY"), ("EA", "SY"), ("EAS", "Y"), ("EASY", "")]
# ans = "No"
# for p, q in piece:
#     if p == "":
#         locate = 0
#     elif p in s:
#         locate = s.find(p) + len(p)
#     else:
#         continue

#     if q == "":
#         locate2 = len(s)
#     elif q in s:
#         locate2 = s.rfind(q)
#     else:
#         continue
#     left = s[:locate]
#     right = s[locate2:]

#     if locate <= locate2 and "HARD" not in left and "HARD" not in right:
#         ans = "Yes"
#         break

# print(ans)


N = int(input())
lst = list(map(int, input().split()))

c1 = lst.count(1)
c2 = N - c1

if c1 >= c2 and (c1 - c2) % 3 == 0:
    print("Yes")
else:
    print("No")