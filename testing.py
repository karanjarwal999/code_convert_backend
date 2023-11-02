def checkPrime(num):
    ind=2
    if num==1:print('prime')
    elif num==2:print('not prime')
    else :
        while ind<math.floor(num/2):
            if num%ind == 0:
                print("not prime")
                return 
            ind += 1
        print("prime")
    return 
# checkPrime(19)

def listGenerator():
    myList = []
    index = 0
    while index < 9:
        myList.append(index + 1)
        index += 1 
    print(f"generated list : {myList}")
    myList.append(4)
    print(f"after adding 4 : {myList}")
    myList.pop()
    print(f"after popping : {myList}")
    myList.sort()  
    print(f"sorted list : {myList}")

#listGenerator()