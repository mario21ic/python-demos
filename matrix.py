matrix1 = [
[1, 0, 2],
[3, 1, 0],
[5, -1, 2]
]

matrix2 = [
[2, -1, 0],
[5, 1, -1],
[-2, 0, 0]
]

#y=0
first = matrix1[0][0]*matrix2[0][0] + matrix1[0][1]*matrix2[1][0] + matrix1[0][2]*matrix2[2][0]
print(first)

#y=1
second = matrix1[0][0]*matrix2[0][1] + matrix1[0][1]*matrix2[1][1] + matrix1[0][2]*matrix2[2][1]
print(second)
