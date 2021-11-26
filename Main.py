import numpy as np
import sys

#input matrix dari file, edit file inputA.txt dan inputB.txt jika ingin mengganti matrix
def inputFile():
    a= np.loadtxt("inputA.txt", dtype='f', delimiter=' ')
    b= np.loadtxt("inputB.txt", dtype='f', delimiter=' ')
    return a,b

##input matrix dari console
def inputManual():
    n=int(input("Masukkan ukuran Matriks : "))
    a=np.zeros((n,n),float)
    b=np.zeros(n,float)

    print("Masukkan Matriks A : ")
    for i in range (n):
        for j in range(n):
            a[i][j]=float(input("a[%d][%d] = " %(i,j)))

    print("Masukkan Matriks B : ")
    for i in range (n):
        b[i]=float(input("b[%d] = " %(i)))

    return a,b

#eliminasi gauss:TODO:belum selesai masih salah
def gauss():
    a,b=menuInput()
    n=len(b)
    A=np.column_stack((a,b))
    x=np.zeros(n,float)

    #PIVOTING
    for i in range(0, n):
       # Mencari kolom dengan nilai tertinggi
       maxE1 = abs(A[i][i])
       maxRow = i
       for k in range(i+1, n):
           # membandingkan baris-baris, baris pertama tidak boleh 0
           if abs(A[k][i]) < maxE1 or maxE1 == 0:
               maxE1 = abs(A[k][i])
               maxRow = k
       # Tukar baris akhir dengan baris yang mengandung 0 (kolom demi kolom)
       for k in range(i, n+1):
           tmp = A[maxRow][k]
           A[maxRow][k] = A[i][k]
           A[i][k] = tmp
       # buat semua baris dibawah 1 jadi 0
       for k in range(i+1, n):
           c = -A[k][i]/A[i][i]
           for j in range(i, n+1):
               if i == j:
                   A[k][j] = 0
               else:
                   A[k][j] += c * A[i][j]

    # subtitusi mundur
    x = [0 for i in range(n)]
    for i in range(n - 1, -1, -1):
        if A[i][i] == 0:
            return [0 for i in range(n)]
        else:
            x[i] = A[i][n]/A[i][i]
            for k in range(i-1, -1, -1):
                A[k][n] -= A[k][i]*x[i]
    a,b=np.hsplit(A,[n])
    return a,x

#eliminasi gauss-Jordan sudah fix
def gaussJordan():
    a,b=menuInput()
    n=len(b)

    for i in range(n):
        #PARTIAL PIVOTING
        if np.fabs(a[i,i]) == 0:
            for j in range(i+1,n):
                if np.fabs(a[j,i]) > np.fabs(a[i,i]):
                    for k in range(i,n):
                        a[i,k],a[j,k] = a[j,k],a[i,k]
                    b[i],b[j] = b[j],b[i]
                    break

        #pembagian baris-baris pivot
        pivot = a[i,i]
        #counter pembagi 0 jika ingin digunakan tapi fungsi encounterHasil() jadi useless
        # if pivot==0:
        #     pivot=1
        for j in range(i,n):
            a[i,j] /= pivot
        b[i] /= pivot

        #subtitusi
        for j in range(n):
            if j == i or a[j,i] == 0: continue
            factor = a[j,i]
            for k in range(i,n):
                a[j,k] -= factor * a[i,k]
            b[j] -= factor*b[i]
    return a,b


#untuk cek solusi apakah dia tidak ada solusi atau memiliki solusi banyak
#JIKA TIDAK ADA SOLUSI/MEMILIKI SOLUSI BANYAK MAKA PROGRAM AKAN MENAMPILKAN PESAN
def encounterHasil(A,B):
    #cek tidak memiliki solusi atau solusi banyak
    i=len(B)-1

    #encounter hasil yang bukan solusi tunggal/unik
    if np.all(np.isinf(B)):
        print('#Hasil Eliminasi :\nTidak ada Solusi')
        #simpan output kedalam file
        with open('output.txt', 'a') as out:
            print('#Hasil Eliminasi :\nTidak ada Solusi',file=out)
            print('---------------------------------------------',file=out)
        return
    
    elif np.all(np.isnan(B)):
        print('#Hasil Eliminasi :\nMemiliki Solusi Banyak')
        #simpan output kedalam file
        with open('output.txt', 'a') as out:
            print('#Hasil Eliminasi :\nMemiliki Solusi Banyak',file=out)
            print('---------------------------------------------',file=out)
        return

    #berjalan jika matrix memiliki solusi dan tidak memiliki solusi banyak
    print("\nMatrix setelah OBE : ")
    print(A)
    print()
    print("Hasil Eliminasi  : ")
    for j in range(len(B)):
        print("X%d = %0.1f" %(j+1,B[j]) , end='\n')
    
    #save hasil ke file output.txt
    with open('output.txt', 'ab') as out:
        np.savetxt(out,A,fmt='%0.1f',delimiter=' ',header='Matrix A Setelah OBE')
        np.savetxt(out,B,fmt='%0.1f',delimiter='\n',header='Hasil Eliminasi',footer='---------------------------------------------')


#MENU PEMILIHAN METODE
def menuUtama():
    print('===== MENU UTAMA =====')
    print('1. SPL Eliminasi Gauss-Jordan')
    print('2. SPL Eliminasi Gauss')
    print('0. Stop Program')
    opsi=int(input('Pilih : '))
    
    if opsi==0:
        print('Program Dihentikan!')
        sys.exit()
    elif opsi==1 :
        a,b = gaussJordan()
    elif opsi==2 :
        a,b = gauss()
    else:
        print('Input Salah !! ')
        menuUtama()
    return a,b

#MENU PEMILIHAN CARA INPUT
def menuInput():
    print('===== MENU INPUT =====')
    print('1. Input Manual')
    print('2. Input dari File')
    print('0. Kembali Ke Menu Utama')
    opsi=int(input('Pilih : '))
    
    if opsi==0:
        menuUtama()
    elif(opsi==1):
        a,b = inputManual()
    elif(opsi==2):
        a,b = inputFile()
    else:
        print('Input Salah !! ')
        menuUtama()
    return a,b

#START PROGRAM
A,X = menuUtama()
encounterHasil(A,X)
