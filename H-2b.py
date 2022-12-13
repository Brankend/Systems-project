import nltk
import re
import pandas as pd
from IPython.display import display
class CP:
    def __init__(self,data):
        self.data = data
    def __str__(self):
        return str(self.data)
    def __repr__(self):
        return self.data
class Node:
    def __init__(self,data,children):
        self.data = data
        self.children = children


letter = CP('letter')
letterRule = []
for x in range (65,91):
    letterRule.append(chr(x))
for x in range (97,123):
    letterRule.append(chr(x))
letterRule.append('_')


#letter = Node(data ='letter',children=letterRule)


digitRule = []
innerDigitRule = []
for x in range(48,58):
    innerDigitRule.append(chr(x))
#digit = Node(data='digit',children=digitRule)
digit = CP('digit')
digitRule.append(innerDigitRule)

#id1 = Node(data = 'id1',children = [])
id1 = CP("id")
id1Rule = [ [id1,digit] , [id1,letter],None]
id1.children = id1Rule

idRule = [[letter,id1]]
#id = Node(data='id',children= idRule)
id = CP('id')

operatorRule = ['+','-','*','/','^','%']
#operator = Node(data='operator',children= operatorRule)
operator = CP("operator")

#num = Node(data='num',children=[])
num = CP("num")
numRule = [[num,0],[num,1],[num,2],[num,3],[num,4],[num,5],[num,6],[num,7],[num,8],[num,9],None]
num.children = numRule


line2Rule = [['num'],['id']]
#line2 = Node(data = 'line2',children=line2Rule)
line2 = CP('line2')
lineRule = [[line2,operator,'id'],[line2,operator,'num']]
#line = Node(data = 'line',children=lineRule)
line = CP("line")


bodyRule = [['id','=',line,';'],['id','++'],['id','--']]
#body = Node(data='body',children=bodyRule)
body = CP("body")


cmpopRule = ['>','<','>=','<=','==','!=','!>','!<']
#cmpop = Node(data='cmpop',children=cmpopRule)
cmpop = CP("cmpop")


cmpRule = [['id',cmpop,'id'],['id',cmpop,'num']]
#cmp = Node(data='cmp',children=cmpRule)
cmp = CP("cmp")


initRule = [['id','=','id'],['id','=','num']]
#init = Node(data='init',children=initRule)
init = CP("init")


condRule = [[init,';',cmp,';',body]]
#cond = Node(data='cond',children=condRule)
cond = CP("cond")


sRule = [['for','(',cond,')','{',body,'}']]
#s = Node(data='s',children=sRule)
s=CP('s')
tokens_dic = {}

cfg = {
    letter : letterRule,
    digit : digitRule,
    #id1 : id1Rule,
    #id : idRule,
    operator : operatorRule,
    #num : numRule,
    line2 : line2Rule,
    line : lineRule,
    body : bodyRule,
    cmpop : cmpopRule,
    cmp : cmpRule,
    init : initRule,
    cond : condRule,
    s : sRule
}


def lexAnalyzer(fileDirectory):
    f = open(fileDirectory)
    prog = ''
    for x in f:
        prog = prog + x + ' '
    f.close
    #tokens inside the read text file
    prog_tokens = nltk.wordpunct_tokenize(prog)
    #print(prog_tokens)
    #regex statements for statements,operators,numbers,identifiers and special characters to get the type of each token
    reg_statements = "for"
    # == < > not operators 3aizen nhotaha fhaga lwhdha
    reg_op = "(\++)|(--)|(-)|(\+)|(=)|(==)|(\*)|(\/)|(%)|(<=)|(<)|(>)|(>=)|(\^)"
    reg_nums = "\d+"
    reg_id = "^[a-zA-Z_]+[a-zA-Z0-9_]*"
    reg_sc = ",|\(|\)|;|(\{)|(\})"
    df = pd.DataFrame(columns=['Token','Type']) #dataframe that's going to contain each token and its type
    global tokens_dic
    for token in prog_tokens:
        if(re.findall(reg_statements,token)):
            ttype = 'Statement'
        elif(re.findall(reg_op,token)):
            ttype = operator
        elif(re.findall(reg_nums,token)):
            ttype = num
        elif(re.findall(reg_id,token)):
            ttype = id
        elif(re.findall(reg_sc,token)):
            ttype = 'specialCharacter'
        else:
            ttype = 'Unknown'
        tokens_dic[token] = ttype
        df.loc[len(df)] = [token,ttype]
    display(df)
    return prog_tokens

#fileDirec = input('inter file directory')
prog_tokens = lexAnalyzer('code.cplg')#(fileDirectory=fileDirec)
tokens_stack = []
for token in prog_tokens:
    tokens_stack.append(token)
rmd = []
result = []
print(cfg[s][0])
for x in cfg[s][0]:
    rmd.append(x)
current_token = tokens_stack.pop()
while(len(tokens_stack) > 0 or len(rmd) > 0):
    if(len(rmd)>0):
        current = rmd.pop()
    print(current)
    print(current_token)
    if(isinstance(current,str)):
        if(current[0] == current_token or current == current_token or current == str(tokens_dic[current_token])):
            result.append(current_token)
            print("matched")
            if(len(tokens_stack) > 0):
                current_token = tokens_stack.pop()
        else:
            #print(rmd)
            print("Didn't match with cfg")
            break
    elif(len(cfg[current]) == 1):
        for c in cfg[current][0]:
            rmd.append(c)
        print(rmd)
    else:
        for x in cfg[current]:
            if(str(x[len(x)-1]) == str(tokens_dic[current_token]) or str(x[len(x)-1]) == current_token):
                print("Found correct")
                for c in x:
                    rmd.append(c)
                break
        print(rmd)
resstr = ""
for x in range(0,len(result)):
    resstr += result.pop() + " "
print(resstr)