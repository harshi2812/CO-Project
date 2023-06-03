registerfilebin={"000":"0000000000000000","001":"0000000000000000",
                 "010":"0000000000000000","011":"0000000000000000",
                 "100":"0000000000000000","101":"0000000000000000",
                 "110":"0000000000000000","111":"0000000000000000"}
ins={}
varname={}
PC=0
f1=open('inputsim.txt','r')
l=f1.readlines()
cnt=0
for i in l:
    ins[cnt]=i[0:16]
    cnt=cnt+1
def resetflag():
    registerfilebin["111"]="0000000000000000"
    

def dectobinary(number):
    if(number==" "):
        return " "
    a=int(number)
    b=bin(a)
    c=str(b)[2:]
    numberofdig=len(c)
    d=""
    for i in range(0,16-numberofdig):
        d=d+"0"
    d=d+c
    return d
def binary_to_decimal(binary):
    decimal = 0
    power = 0
    for bit in reversed(binary):
        if bit == '1':
            decimal=decimal+2**power
        power=power+1
    return decimal
def computenot(s):
    temp=""
    for i in s:
        if(i=="0"):
            temp=temp+"1"
        if(i=="1"):
            temp=temp+"0"
    return temp
def computeand(s1, s2):
    num1 = int(s1, 2)
    num2 = int(s2, 2)
    result = num1 & num2
    binary_str = bin(result)[2:] 
    return '0' * (16 - len(binary_str)) + binary_str  
def decimal_to_seven_bit_binary(decimal):
    binary = bin(decimal)[2:]  
    binary = binary.zfill(7)  
    return binary
def computeor(s1, s2):
    num1 = int(s1, 2)
    num2 = int(s2, 2)
    result = num1 | num2
    return format(result, '016b')
def computexor(s1, s2):
    num1 = int(s1, 2)
    num2 = int(s2, 2)
    result = num1 ^ num2
    return format(result, '016b')
def computels(s1, n):
    num = int(s1, 2)
    temp = num << n
    return format(temp, '0' + str(len(s1) + n) + 'b')
def computers(s1, n):
    num = int(s1, 2)
    temp = num >> n
    return format(temp, '016b')
def decimal_to_seven_bit_binary(decimal):
    binary = bin(decimal)[2:] 
    binary = binary.zfill(7)   
    return binary

def isadd(s):
    rs1=registerfilebin[s[10:13]]
    rs2=registerfilebin[s[13:]]
    if int(binary_to_decimal(rs1)+binary_to_decimal(rs2))>=653536:
        registerfilebin["111"]="0000000000001000"
        return
    registerfilebin[s[7:10]]=dectobinary(int(binary_to_decimal(rs1)+binary_to_decimal(rs2)))
    resetflag()
def ismul(s):
    rs1=registerfilebin[s[10:13]]
    rs2=registerfilebin[s[13:]]
    if int(binary_to_decimal(rs1)*binary_to_decimal(rs2))>=653536:
        registerfilebin["111"]="0000000000001000"
        return
    registerfilebin[s[7:10]]=dectobinary(int(binary_to_decimal(rs1)*binary_to_decimal(rs2)))
    resetflag()
def issub(s):
    rs1=registerfilebin[s[10:13]]
    rs2=registerfilebin[s[13:]]
    if int(binary_to_decimal(rs1)-binary_to_decimal(rs2))>=653536:
        registerfilebin["111"]="0000000000001000"
        return
    registerfilebin[s[7:10]]=dectobinary(int(binary_to_decimal(rs1)-binary_to_decimal(rs2)))
    resetflag()
def isdiv(s):
    rs1=registerfilebin[s[10:13]]
    rs2=registerfilebin[s[13:]]
    if int(binary_to_decimal(rs1)%binary_to_decimal(rs2))>=653536 or int(binary_to_decimal(rs1)//binary_to_decimal(rs2)):
        registerfilebin["111"]="0000000000001000"
        return
    registerfilebin["000"]=dectobinary(int(binary_to_decimal(rs1)//binary_to_decimal(rs2)))
    registerfilebin["001"]=dectobinary(int(binary_to_decimal(rs1)%binary_to_decimal(rs2)))
    resetflag()
def ismov(s):
    registerfilebin[s[10:13]]=registerfilebin[s[13:]]
    resetflag()
def isnot(s):
    registerfilebin[s[10:13]]=computenot(registerfilebin[s[13:]])
    resetflag()
def isand(s):
    registerfilebin[s[7:10]]=computeand(registerfilebin[s[10:13]],registerfilebin[s[13:]])
    resetflag()
def isor(s):
    registerfilebin[s[7:10]]=computeor(registerfilebin[s[10:13]],registerfilebin[s[13:]])
    resetflag()
def isxor(s):
    registerfilebin[s[7:10]]=computexor(registerfilebin[s[10:13]],registerfilebin[s[13:]])
    resetflag()
def isls(s):
    registerfilebin[s[6:9]]=computels(registerfilebin[s[6:9]],binary_to_decimal(s[9:]))[-16:]
    resetflag()
def isrs(s):
    registerfilebin[s[6:9]]=computers(registerfilebin[s[6:9]],binary_to_decimal(s[9:]))
    resetflag()
def iscmp(s):
    r1=binary_to_decimal(registerfilebin[s[10:13]])
    r2=binary_to_decimal(registerfilebin[s[13:]])
    if(r1>r2):
        registerfilebin["111"]="0000000000000010"
        
    if(r1<r2):
        registerfilebin["111"]="0000000000000100"
        
    if(r1==r2):
        registerfilebin["111"]="0000000000000001"
        
def isjmp(s):
    global PC
    PC=binary_to_decimal(s[9:])
    resetflag()
    return 1
def isjlt(s):
    if(registerfilebin["111"]=="0000000000000100"):
        global PC
        PC=binary_to_decimal(s[9:])
        resetflag()
        return 1
    resetflag()
    return 0
def isje(s):
    if(registerfilebin["111"]=="0000000000000001"):
        global PC
        PC=binary_to_decimal(s[9:])
        resetflag()
        return 1
    resetflag()
    return 0
def isjgt(s):
    if(registerfilebin["111"]=="0000000000000010"):
        global PC
        PC=binary_to_decimal(s[9:])
        resetflag()
        return 1
    resetflag()
    return 0
def ismovimm(s):
    a=binary_to_decimal(s[9:])
    a=dectobinary(a)
    registerfilebin[s[6:9]]=a
    resetflag()
def isld(s):
    if(s[9:] not in ins):
        ins[s[9:]]="0000000000000000"
    registerfilebin[s[6:9]]=ins[s[9:]]
    resetflag()
def isst(s):
    if(s[9:] not in ins):
        ins[s[9:]]="0000000000000000"
    ins[s[9:]]=registerfilebin[s[6:9]]
    resetflag()
def printreg():
    temppc=decimal_to_seven_bit_binary(PC)
    print(temppc+(" "*8)+registerfilebin["000"]+" "+registerfilebin["001"]+" "+registerfilebin["010"]+" "+registerfilebin["011"]+" "+registerfilebin["100"]+" "+registerfilebin["101"]+" "+registerfilebin["110"]+" "+registerfilebin["111"])
while(1):
    a=ins[PC]
    if a[0:5]=="11010":
        printreg()
        break
    elif a[0:5]=="00000":
        isadd(a)
        printreg()
    elif a[0:5]=="00001":
        issub(a)
        printreg()
    elif a[0:5]=="00010":
        ismovimm(a)
        printreg()
    elif a[0:5]=="00011":
        ismov(a)
        printreg()
    elif a[0:5]=="00100":
        isld(a)
        printreg()
    elif a[0:5]=="00101":
        isst(a)
        printreg()
    elif a[0:5]=="00110":
        ismul(a)
        printreg()
    elif a[0:5]=="00111":
        isdiv(a)
        printreg()
    elif a[0:5]=="01000":
        isrs(a)
        printreg()
    elif a[0:5]=="01001":
        isls(a)
        printreg()
    elif a[0:5]=="01010":
        isxor(a)
        printreg()
    elif a[0:5]=="01011":
        isor(a)
        printreg()
    elif a[0:5]=="01100":
        isand(a)
        printreg()
    elif a[0:5]=="01101":
        isnot(a)
        printreg()
    elif a[0:5]=="01110":
        iscmp(a)
        printreg()
    elif a[0:5]=="01111":
        isjmp(a)
        printreg()
        continue
    elif a[0:5]=="11100":
        t=isjlt(a)
        if t==1:
            printreg()
            continue
        printreg()
    elif a[0:5]=="11101":
        t=isjgt(a)
        if t==1:
            printreg()
            continue
        printreg()
    elif a[0:5]=="11111":
        t=isje(a)
        if t==1:
            printreg()
            continue
        printreg()
    PC=PC+1
memorydum=[]
for i in ins:
    memorydum.append(ins[i])
temp={}
for j in varname:
    a=int(binary_to_decimal(j))
    temp[a]=varname[j]
temp=dict(sorted(temp.items()))
for k in temp:
    memorydum.append(temp[k])
for t in range(0,128-len(memorydum)):
    memorydum.append("0000000000000000")
for y in memorydum:
    print(y)

