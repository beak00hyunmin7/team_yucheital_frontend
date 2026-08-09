# ipt = input()
# croatia_alp = ["c=", "c-", "dz=", "d-", "lj", "nj", "s=", "z="]
# for i in croatia_alp:
#     ipt = ipt.replace(i, '*')
# print(len(ipt))


# cost = 15
# a = int(input("Number of coal A = "))
# b = int(input("Number of coal B = "))
# c = int(input("Number of coal C = "))

# print(f"Number of coal in A = {a}")
# print(f"Number of coal in B = {b}")
# print(f"Number of coal in C = {c}")
# print(f"savings = {15*(a*2 + b*3 + c*4)}")

# a = int(input())
# lst = []
# for x in range(a):
#     ipt = input()
#     lst.append(ipt)

# ans = 0
# for x in lst:
#     aph = list(x)
#     aph_list = list(x)
#     aph = list(set(aph))
#     for y in aph:
#         judge = []
#         if aph_list.count(y) <= 1:
#             pass
#         else:
#             for z in range(len(aph_list)):
#                 if aph_list[z] == y:
#                     judge.append(z)
#         for i in range(len(judge) - 1):
#             if judge[i+1] - judge[i] > 1:
#                 pass
#             else:
#                 ans += 1

# print(ans)


# N, A = map(int, input().split())

# def additive_inverse(N, A):
#     return (N-A) % N

# def multiplicative_inverse(N, A):
#     def gcd(a, b):
#         if b == 0:
#             return a, 1, 0
#         g, x1, y1 = gcd(b, a % b)
#         return g, y1, x1 - (a // b) * y1

#     g, x, _ = gcd(A, N)
#     if g != 1:
#         return -1
#     else:
#         return x % N



# print(f"{additive_inverse(N, A)} {multiplicative_inverse(N, A)}")


# def judge(a):
#     lst = []
#     for x in a:
#         if x in lst:
#             if lst[-1] != x:
#                 return 0
#             else:
#                 pass
#         else:
#             lst.append(x)
#     return 1

# a = int(input())
# ans = 0
# for x in range(a):
#     ipt = str(input())
#     ans += judge(ipt)
# print(ans)

# def money(a):
#     print(a // 25, end = ' ')
#     a %= 25
#     print(a // 10, end = ' ')
#     a %= 10
#     print(a // 5, end = ' ')
#     a %= 5
#     print(a // 1)

# N = int(input())
# for x in range(N):
#     ipt = int(input())
#     money(ipt)


# N = int(input())
# print((2**N+1)**2)


# N = int(input())

# if N == 1:
#     print("1")
# else:
#     count = 1
#     depth = 1
#     while count < N:
#         count += 6 * depth
#         depth += 1
#     print(depth)


# cnt = 1
# a = int(input())
# while True:
#     if a - cnt > 0:
#         a -= cnt
#     else:
#         break
#     cnt += 1

# if cnt == 1:
#     print("1/1")
# else:
#     if cnt % 2 == 1:
#         print(f"{cnt - a + 1}/{a}")
#     else:
#         b, c = cnt-a, 1+a
#         print(f"{a}/{cnt - a + 1}")


# a, b, c = map(int, input().split())

# import math
# b, a, v = map(int, input().split())

# if b > v:
#     print("1")
# else:
#     h = math.ceil((v-b) / (b-a)) + 1
#     print(h)

# while True:
#     a, b = map(int, input().split())
#     if a == 0 and b == 0:
#         break;
#     if b % a == 0:
#         print("factor")
#     elif a % b == 0:
#         print("multiple")
#     else:
#         print("neither")


# lst = []
# N, K = map(int, input().split())
# for x in range(1, (N//2)+1):
#     if N % x == 0:
#         lst.append(x)
# lst.append(N)


# try:
#     print(lst[K-1])
# except IndexError:
#     print("0")


# while True:
#     a = int(input())
#     if a == -1:
#         break

#     b = 0
#     lst = []
#     for x in range(1, a//2 + 1):
#         if a % x == 0:
#             b += x
#             lst.append(x)

#     if a == b:
#         print(f"{a} = ", end = '')
#         print(*lst, sep = ' + ')

#     else:
#         print(f"{a} is NOT perfect.")


# a = int(input())
# ans = 0
# ipt = list(map(int, input().split()))
# for x in range(a):
#     judge = 0
#     if ipt[x] < 2:
#         continue
#     for y in range(2, ipt[x] // 2 + 1):
#         if ipt[x] % y == 0:
#             judge = 1 #소수아님
#             break
#     if judge == 0:
#         ans += 1
# print(ans)


# sum = 0
# min = 0
# a = int(input())
# b = int(input())
# for x in range(a, b+1):
#     judge = 1
#     if x < 2:
#         continue
#     for y in range(2, x//2+1):
#         if x % y == 0:
#             judge = 0
#     if judge == 1       : 
#         sum += x
#         if min == 0 or min > x:
#             min = x

# if sum == 0 and min == 0:
#     print("-1")
# else:
#     print(sum)
#     print(min)
        

# a = int(input())
# lst = []
# while a > 1:
#     for x in range(2, a+1):
#         if a % x == 0:
#             lst.append(x)
#             break
#     a //= x
# print(*lst, sep = '\n')

# a = int(input())
# sum = 0
# while a > 0:
#     sum += a % 10
#     a //= 10
# print(sum)

# a = int(input())
# b = int(input())
# c = int(input())

# d = a * 100 + b * 10 + c
# judge = 1
# for x in range(2, d-1):
#     if d % x == 0:
#         judge = 0
#         break
# if judge == 0:
#     print("Lose")
# else:
#     print("Win")

# n = int(input())
# for i in range(1, n + 1):
#     ns, ew = int(input()), int(input())
#     diff = abs(ns - ew)
#     a, b = 60, 60
#     if diff >= 50:
#         adj = 20
#     elif diff >= 20:
#         adj = 10
#     else:
#         adj = 0
#     if ns > ew:
#         a += adj; b -= adj
#     elif ew > ns:
#         b += adj; a -= adj
#     print(f"Intersection {i} : {a} sec, {b} sec")


# def solution(numbers, hand):
#     global lst
#     lst = [[1, 2, 3], [4, 5, 6], [7, 8, 9], ['*', 0, '#']]
#     ans = ''
#     left = [3, 0]
#     right = [3, 2]

#     for x in range(len(numbers)):
#         for y in range(4):
#             for z in range(3):
#                 if lst[y][z] == numbers[x]:
#                     col, row = y, z
#                     break
#         if judge(left, right, col, row, hand) == 1: #오른손이면
#             ans += 'R'
#             right = [col, row]
#         else:
#             ans += 'L'
#             left = [col, row]

#     return ans



# def judge(left, right, col, row, hand):
#     left_distance = abs(left[0] - col) + abs(left[1] - row)
#     right_distance = abs(right[0] - col) + abs(right[1] - row)

#     if left_distance > right_distance:
#         return 1 #오른손
#     elif left_distance < right_distance:
#         return 2 #왼손
#     else:
#         if hand == "right":
#             return 1
#         else:
#             return 2


# def solution(k, m, score):
#     score.sort(reverse=True)
#     n = len(score)
#     total = 0
#     for i in range(0, n - n % m, m):
#         box = score[i:i+m]
#         total += min(box) * m
#     return total


def solution(s):
    answer = ''
    s = s.split(",")
    lst = []
    for x in s:
        if x == ',':
            pass
        else:
            lst.append(int(x))
    answer += str(min(lst)) + ' ' + str(max(lst))
    return answer

print(solution("-1, -2, -3, -4"))