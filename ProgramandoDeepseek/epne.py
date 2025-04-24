#Encontrar el primer numero entero que no sea parte de la lista
a = [ -1 , 2 , 4 , 6 , 1 , 5 ]
#a = [ -1 , 1 , 2 , 6 , 4 , 5 ]
#output: 3

b = [ 4 , 0 , 2 , 7 , 1 , 3 , 5 ]
#b = [ 0 , 1 , 2 , 3 , 4 , 5 , 7 ]
#output: 6

c = [ 2 , 0 , 4 , -2 , -1 , 3 ]
#c = [ -2 , -1 , 0 , 2 , 3 , 4 ]
#output: 1

def hallar(list):
    print(list)
    list.sort()
    print(list)
    i = 1
    for item in list:
        if item > 0:
            if i != item:                
                print(i)                
                break
            else:
                i +=1
                continue
        else:            
            continue    

hallar(a)
hallar(b)
hallar(c)