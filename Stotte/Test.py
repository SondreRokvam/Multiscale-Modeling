import numpy as np

a = np.ones(3)
a[1] =2
a[2] =3
b = np.ones([3,6])
b[1][5]=0
b[2][5]=10

a = np.arange(9.0).reshape((3, 3))
b = np.arange(3.0)
print (a,'\n\n', b,'\n\n')
a=  np.multiply(a, b)


print(a)
a=np.multiply(a,b)
