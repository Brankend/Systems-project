import nltk
import re
import pandas as pd
from IPython.display import display
from binarytree import Node
# from anytree import Node, RenderTree
# from anytree.exporter import DotExporter
#import graphviz
class CP:
    def __init__(self,data):
        self.data = data
    def __str__(self):
        return str(self.data)
    def __repr__(self):
        return self.data



flagerror=0
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


cmpopRule = [['>'],['<'],['>='],['<='],['=='],['!='],['!>'],['!<']]
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
matchrule=[initRule[1]]
print(" walaa    aaal;la;a;a;la")
for e in matchrule :
    print(e[1])



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
matchee=[]
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
            exit()
            
           
    elif(len(cfg[current]) == 1):
        for c in cfg[current][0]:
            rmd.append(c)
        print(rmd)
    else:
        for x in cfg[current]:
            if(str(x[len(x)-1]) == str(tokens_dic[current_token]) or str(x[len(x)-1]) == current_token):
                print("Found correct")
                #matchee.push(x)
                for c in x:
                    rmd.append(c)
                break
        print(rmd)
resstr = ""
abdo=[]
for x in range(0,len(result)):
   abdo.append(result.pop())
# for x in range(0,len(result)):
#     resstr += result.pop() + " "
#print(resstr)
for x in abdo:
     resstr+= x + " "
#    print(x)
   
print(resstr)



#region failed tree(udo) 


# udo = Node("Udo")
# marc = Node("Marc", parent=udo)
# lian = Node("Lian", parent=marc)
# dan = Node("Dan", parent=udo)
# jet = Node("Jet", parent=dan)
# jan = Node("Jan", parent=dan)
# joe = Node("Joe", parent=dan)
# print(udo)


# for pre, fill, node in RenderTree(udo):
#     print("%s%s" % (pre, node.name))
# DotExporter(udo).to_picture("udo.png")
#endregion


# getting matched non terminals into arrays

matchedinitial=[]
matchedcondition=[]
matchedupdate=[]
matchedbody=[]   
for x in range(2,5):
     matchedinitial.append(abdo[x])

for x in range(6,9):
     matchedcondition.append(abdo[x])
for x in range(10,12):
     matchedupdate.append(abdo[x])

for x in range(14,len(abdo)-1):
       matchedbody.append(abdo[x])

print("matched initializer ")
for x in matchedinitial:
    print(x)

print("matched cond ")
for x in matchedcondition:
    print(x)    

print("matched upd ")
for x in matchedupdate:
    print(x)    

print("matched body ")
for x in matchedbody:
    print(x)     

if(len(matchedupdate)==2):
  if(str(matchedupdate[1])=="++"):
    matchedupdate[1]='='
    matchedupdate.append(matchedupdate[0])
    matchedupdate.append('+')
    matchedupdate.append(1)

  elif(str(matchedupdate[1])=="--"):
    matchedupdate[1]='='
    matchedupdate[2]=matchedupdate[0]
    matchedupdate[3]='-'
    matchedupdate[4]=1

 
#plotting syntax tree     
semicln =';' # lw fashlna 
from binarytree import Node
root = Node(abdo[0])
#left subtree
root.left = Node(semicln)
root.left.left = Node(matchedinitial[1])
root.left.left.left =Node(matchedinitial[0])
root.left.left.right =Node(matchedinitial[2])
root.left.right = Node(semicln)
root.left.right.left = Node(matchedcondition[1])
root.left.right.left.left = Node(matchedcondition[0])
root.left.right.left.right = Node(matchedcondition[2])
root.left.right.right = Node(semicln)
root.left.right.right.left = Node(matchedbody[1])
root.left.right.right.left.left = Node(matchedbody[0])
root.left.right.right.left.right = Node(matchedbody[3])
root.left.right.right.left.right.left = Node(matchedbody[2])
root.left.right.right.left.right.right = Node(matchedbody[4])
#right subtreee
root.right = Node(matchedupdate[1])
root.right.left = Node(matchedupdate[0])



print('for loop abstract syntax tree :', root)

    # nodes=[abdo[0],';',matchedupdate[1],matchedinitial[1],';',matchedupdate[0],None,matchedinitial[0],matchedinitial[2],matchedcondition[1],';',None,None,None,None,matchedcondition[0],matchedcondition[2],matchedbody[1]]
    # binary_tree = build(nodes)
    # print('Binary tree from list :\n',
    #       binary_tree)


