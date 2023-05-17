import sys
opcodes={"add":"00000","sub":"00001","mov1":"00010","mov2":"00011","ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"11100","jgt":"11101","je":"11111","hlt":"11010"}
register={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}

def dectobinary(number):
    if(number==" "):
        return " "
    a=int(number)
    b=bin(a)
    c=str(b)[2:]
    numberofdig=len(c)
    d=""
    for i in range(0,7-numberofdig):
        d=d+"0"
    d=d+c
    return d
#inputfil=open('input.txt','r')
l=sys.stdin.readlines()
l1=[ele.split() for ele in l]
l3proper=[]
for i in range(len(l1)):
    if(l1[i]!=['\n']):
        l3proper.append(l1[i])
#l3proper=[ele for ele in l3proper]
for i in range(len(l3proper)):
    if(l3proper[i][-1][-1]=='\n'):
        temp=l3proper[i][-1][:-1]
        l3proper[i][-1]=temp
#print(l3proper)

j=0
ldecimaddr=[]
for k in range(len(l3proper)):
    if(l3proper[k][0]!="var"):
        ldecimaddr.append(str(j))
        j+=1
    else:
        ldecimaddr.append(" ")
lbinaryaddress=[dectobinary(ele) for ele in ldecimaddr ]
def simplearithemetic(l):
    opcode1=opcodes[l[0]]
    d=""
    if(l[0]=="cmp" or l[0]=="not" or l[0]=="div"):
        reg1=register[l[1]]
        reg2=register[l[2]]
        d=opcode1+"00000"+reg1+reg2
    else:
        reg1=register[l[1]]
        reg2=register[l[2]]
        reg3=register[l[3]]
        d=opcode1+"00"+reg1+reg2+reg3
    return d
def movshift(l):
    d=""
        
    if(l[0]=="rs" or l[0]=="ls"):
        opcode1=opcodes[l[0]]
        reg1=register[l[1]]
        imme=dectobinary(l[2][1:])
        d=opcode1+"0"+reg1+imme
    else:
        if(l[2][0]=="$" and l[2][1:].isnumeric()==True):
            opcode1=opcodes["mov1"]
            reg1=register[l[1]]
            imme1=dectobinary(l[2][1:])
            d=opcode1+"0"+reg1+imme1
        else:
            opcode1=opcodes["mov2"]
            reg1=register[l[1]]
            reg2=register[l[2]]
            d=opcode1+"00000"+reg1+reg2
    return d
#print(lbinaryaddress)
#print(j)
varname={}
def assignvarname(l):
    global j
    global varname
    varname[l[1]]=dectobinary(j)
    j=j+1
def ldstr(l):
    d=""
    opcode1=opcodes[l[0]]
    reg1=register[l[1]]
    varn=varname[l[2]] 
    d=opcode1+"0"+reg1+varn
    return d
assignedlable={}
def assignlabel(l):#works only for elements with :
    global assignedlable
    
    n=l3proper.index(l)
    assignedlable[(l[0])[:-1]]=lbinaryaddress[n]
def jumpsta(l):
    if(l[1] not in assignedlable):
        return -1
    opcode1=opcodes[l[0]]
    dest=assignedlable[l[1]]
    d=""
    d=opcode1+"0000"+dest
    return d
def convmachinecode(l):
    if(l[0]=="add" or l[0]=="sub" or l[0]=="mul" or l[0]=="xor" or l[0]=="or" or l[0]=="and" or l[0]=="cmp" or l[0]=="not" or l[0]=="div"):
        print(simplearithemetic(l))
    if(l[0]=="rs" or l[0]=="ls" or l[0]=="mov"):
        print(movshift(l))
    if(l[0]=="var"):
        assignvarname(l)
    if(l[0]=="ld" or l[0]=="st"):
        print(ldstr(l))
for k in l3proper:
    if(":" in k[0]):
        assignlabel(k)
def numoperandcheck(l):
    if(l[0] in ["add","sub","mul","xor","or","and"]):
        if(len(l[1:])!=3):
            return 1
    if(l[0] in ["mov","ld","st","div","rs","ls","not","cmp"]):
        if(len(l[1:])!=2):
            return 1
    if(l[0] in ["jmp","jlt","jgt","je"]):
        if(len(l[1:])!=1):
            return 1
    if(l[0] in ["hlt"]):
        if(len(l[1:])!=0):
            return 1
    return 0
def registercheck(l):
    if(l[0] in ["add","sub","mul","xor","or","and"]):
        if(l[1] not in register or l[2] not in register or l[3] not in register):
            return 1
    if(l[0] in ["div","not","cmp"]):
        if(l[1] not in register or l[2] not in register):
            return 1
    if(l[0] in ["ld","st","rs","ls"]):
        if(l[1] not in register):
            return 1
    if(l[0] in ["mov"]):
        if(l[2][0]=="$" and l[2][1:].isnumeric()==True):
            if(l[1] not in register):
                return 1
        else:
            if(l[1] not in register or l[2] not in register):
                return 1
    return 0
def operandcheck(l):
    if(l[0] not in opcodes):
        return 1
    return 0
def overflowcheck(l):
    if(l[0] in ["rs","ls"]):
        if(int(l[2][1:])>127 or int(l[2][1:])<0):
            return 1
    if(l[0] in ["mov"]):
        if(l[2][0]=="$" and l[2][1:].isnumeric()==True):
            if(int(l[2][1:])>127 or int(l[2][1:])<0):
                return 1
    return 0
def lablecheck(l):
    if(l[0] in ["jmp","jlt","jgt","je"]):
        if(l[1] not in assignedlable):
            return 1
    return 0
def varcheck(l):
    if(l[0] in ["ld","st"]):
        if(l[2] not in varname):
            return 1
    return 0
def invalidimm(l):
    if(l[0] in ["rs","ls"]):
        if((l[2][1:]).isnumeric()==False):
            return 1
    if(l[0] in ["mov"]):
        if(l[2][0]=="$"):
            if((l[2][1:]).isnumeric()==False):
                return 1
    return 0

def errorgen(l):
    le=[]
    if(":" in l[0]):
        if(l[1]=="var"):
            return le
        if(overflowcheck(l[1:])==1):
            le.append(-1)
        if(registercheck(l[1:])==1):
            le.append(-2)
        if(numoperandcheck(l[1:])==1):
            le.append(-3)
        if(lablecheck(l[1:])==1):
            le.append(-4)
        if(varcheck(l[1:])==1):
            le.append(-5)
        if(invalidimm(l[1:])==1):
            le.append(-6)
        if(operandcheck(l[1:])==1 and l[1]!="mov"):
            le.append(-7) 
    else:
        if(l[0]=="var"):
            return le
        if(overflowcheck(l)==1):
            le.append(-1)
        if(registercheck(l)==1):
            le.append(-2)
        if(numoperandcheck(l)==1):
            le.append(-3)
        if(lablecheck(l)==1):
            le.append(-4)
        if(varcheck(l)==1):
            le.append(-5)
        if(invalidimm(l)==1):
            le.append(-6)
        if(operandcheck(l)==1 and l[0]!="mov"):
            le.append(-7)
    return le
