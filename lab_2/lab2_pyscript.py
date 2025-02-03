
# first question: multiply items together
part1 = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
result1 = 1

for i in part1:
    result1 = result1 * i 

print('The result of the first question is:', result1)

# second question: add items together
part2 = [-1, 23, 483, 8573, -13847, -381569, 1652337, 718522177]
result2 = 0

# as a while loop
# i = 0
# while i < len(part2):
#   result2 = result2 + part2[i]
#   i = i + 1

for i in part2:
    result2 = result2 + i

print('The result of the second question is:', result2)

# third question: add only even items together
part3 = [146, 875, 911, 83, 81, 439, 44, 5, 46, 76, 61, 68, 1, 14, 38, 26, 21] 
result3 = 0

for i in part3:
    # check if i is even
    if i % 2 == 0:
        result3 = result3 + i 

print('The result of the third question is:', result3)
