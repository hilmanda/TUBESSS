import numpy as np


def gaussJordan(a,b):
    a=np.array(a,float)
    b=np.array(b,float)
    n=len(b)

    for i in range(n):
        if np.fabs(a[i,i]) == 0:
            for j in range(i+1,n):
                if np.fabs(a[j,i]) > np.fabs(a[i,i]):
                    for k in range(i,n):
                        a[i,k],a[j,k] = a[j,k],a[i,k]
                    b[i],b[j] = b[j],b[i]
                    break

        pivot = a[i,i]
        for j in range(i,n):
            a[i,j] /= pivot
        b[i] /= pivot

        for j in range(n):
            if j == i or a[j,i] == 0: continue
            factor = a[j,i]
            for k in range(i,n):
                a[j,k] -= factor * a[i,k]
            b[j] -= factor*b[i]
    return a,b

a= [[0,2,0,1],[2,2,3,2],[4,-3,0,1],[5,1,-6,-5]]
b= [0,-2,-7,6]

A,X = gaussJordan(a,b)

print("\nMatrix Eselon Baris Tereduksi : ")
print(A)

print()
print("Hasil Eliminasi Gauss-Jordan : ")
for i in range(len(X)):
    print("X%d = %0.1f" %(i+1,X[i]) , end='\n')