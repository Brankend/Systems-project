import nltk
import re
import pandas as pd
from IPython.display import display
from binarytree import Node
from binarytree import build

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

#updateRule = [['id','=',line2,operator,'id'],['id','=',line2,operator,'num'],['id','++'],['id','--']]
update = CP("update")

body2Rule = [['id','=',line2,operator,'id'],['id','=',line2,operator,'num'],['id','++'],['id','--']]
body2 = CP('body2')
#body = Node(data='body',children=bodyRule)
body = CP("body")
bodyRule = [[body,body2,';'],[]]


cmpopRule = [['>'],['<'],['>='],['<='],['=='],['!='],['!>'],['!<']]
#cmpop = Node(data='cmpop',children=cmpopRule)
cmpop = CP("cmpop")


cmpRule = [['id',cmpop,'id'],['id',cmpop,'num']]
#cmp = Node(data='cmp',children=cmpRule)
cmp = CP("cmp")


initRule = [['id','=','id'],['id','=','num']]
#init = Node(data='init',children=initRule)
init = CP("init")


condRule = [[init,';',cmp,';',update]]
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
    #update : updateRule,
    update : body2Rule,
    body2 : body2Rule,
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
            if(len(x) == 0):
                break
            elif(str(x[len(x)-1]) == str(tokens_dic[current_token]) or str(x[len(x)-1]) == current_token):
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





#################################################################################################################################
#FUN STARTS HEREEEEEEEEEEEEEE



#this function splits matched body list into nested list each list for statemnt in the body block wasnot eassyyyyy to be honest :)

#region functions declaraion
def grp_ele(test_list):
    statement = []
    for i in test_list: 
        if(str(i)==";"):
            if statement:  
                #statement.append(None)
                #statement.append(None)
                yield statement 
                statement = []
            #yield i  
        else: 
            statement.append(i)
    if statement: 
        #statement.append(None)
        #statement.append(None)
        yield statement

def handle(tohandle_list):
    if(len(tohandle_list)<4):
     if(str(tohandle_list[1])=="++"):
            tohandle_list[1]='='
            tohandle_list.append(tohandle_list[0])
            tohandle_list.append('+')
            tohandle_list.append(1)

     elif(str(tohandle_list[1])=="--"):
            tohandle_list[1]='='
            tohandle_list.append(tohandle_list[0])
            tohandle_list.append('-')
            tohandle_list.append(1)

def arrange(list):
    swaped=[]
    swaped.append(list[1])
    swaped.append(list[0])
    if(len(list)>3):
        swaped.append(list[3])
     # swaped.append(list[5])
     # swaped.append(list[5])

        swaped.append(list[2])
        swaped.append(list[4])
    else:  
      swaped.append(list[2])  

        
    return swaped


def statments_to_string(list): #converting every statment to string
    strr=' ('
    brcflag=0
    for x in list:
        if(x=='+' or x=='-'or x=='*' or x=='/'):
                strr+=' ' + '('
                brcflag=1
        strr+=' '+str(x)

    
    strr+=')'
    if(brcflag==1):
     strr+=')'
    return strr
            

#endregion


#region getting matched non terminals into lists,, abdo is list of the parsed source code (tokens )
matchedinitial=[]
matchedcondition=[]
matchedupdate=[]
matchedbody=[]      
brckindex=0  
#endregion
for x in range(2,5):
     matchedinitial.append(abdo[x])

for x in range(6,9):
     matchedcondition.append(abdo[x])
for x in range(10,len(abdo)):
    if(abdo[x]!=")"):
     matchedupdate.append(abdo[x])
    else:
        brckindex=x
        break

for x in range((brckindex+2),len(abdo)-1):
       matchedbody.append(abdo[x])

#region printing_matched_list
# print("matched initializer ")
# for x in matchedinitial:
#     print(x)

# print("matched cond ")
# for x in matchedcondition:
#     print(x)    

# print("matched upd ")
# for x in matchedupdate:
#     print(x)    

# print("matched body ")
# for x in matchedbody:
#     print(x)     
#endregion

#region handling_unary_operations 
handle(matchedupdate)

statements=list(grp_ele(matchedbody))

for x in statements:
    if(len(x)<=4):
        #del x[-1]
        #del x[-1]
        handle(x)
        #x.append(None)
        #x.append(None)


#endregion
#region plotting syntax tree if one statment no proplems
if(len(statements)==1): # to use binary tree only
    
    semicln ='' # lw fshlna 
    root = Node(abdo[0])
    #left subtree
    root.left = Node('Init_Condition')

    #setting inizialization subtree and link to main tree
    initroot = Node(matchedinitial[1])
    initroot.left =Node(matchedinitial[0])
    initroot.right =Node(matchedinitial[2])
    root.left.left=initroot
    root.left.right = Node('Condition_Body')

    #setting condition subtree and link to main tree
    condroot = Node(matchedcondition[1])
    condroot.left= Node(matchedcondition[0])
    condroot.right = Node(matchedcondition[2])
    root.left.right.left=condroot

    root.left.right.right = Node(semicln)
    #setting body subtree and link to main tree

    bodyroot=Node(statements[0][1])
    bodyroot.left = Node(statements[0][0])
    bodyroot.right = Node(statements[0][3])
    bodyroot.right.left = Node(statements[0][2])
    bodyroot.right.right = Node(statements[0][4])
    root.left.right.right = bodyroot
    #right subtreee
    updroot=Node(matchedupdate[1])
    updroot.left = Node(matchedupdate[0])
    updroot.right = Node(matchedupdate[3])
    updroot.right.left = Node(matchedupdate[2])
    updroot.right.right = Node(matchedupdate[4])
    root.right=Node('Update')
    root.right.left = updroot
    print('For loop abstract syntax tree :', root)

#endregion

    


#region printing every syntax tee alone

# print("Abstract Syntax Tree for Initialization: ",initroot)
# print("Abstract Syntax Tree for Condition: ",condroot)
# print("Abstract Syntax Tree for Update: ",updroot)
# for x in range(0,len(statements)):
#     print("Abstract Syntax Tree for Body statement: ",x+1)
#     statmenttree=build(statements[x])
#     print(statmenttree)
#endregion  





#region arranging list then put into strings fo nltk tree
matchedcondition=arrange(matchedcondition)
matchedinitial=arrange(matchedinitial)
matchedupdate=arrange(matchedupdate)

condition_str=statments_to_string(matchedcondition)
update_str=statments_to_string(matchedupdate)
init_str=statments_to_string(matchedinitial)
statments_str=''




for x in range(0,len(statements)): #arranging each statement to be able to pass it to build()
    statements[x]=arrange(statements[x])
    statements[x]=statments_to_string(statements[x])
    statments_str+=statements[x]
#print(statments_str)

#endregion


# (for (left (init init_str) (cond cond_str)) (right (body body_str) (update upd_str)))

# The Last Dance ->
Tree_Str="(for (Initialization"
Tree_Str+=init_str
Tree_Str+=") (Condition"
Tree_Str+=condition_str
Tree_Str+=") (Body"
Tree_Str+=statments_str
Tree_Str+=") (Update"
Tree_Str+=update_str
Tree_Str+="))"

from nltk.tree import Tree
import nltk.draw
from nltk.draw.tree import TreeView
prog_Tree=Tree.fromstring(Tree_Str)
prog_Tree.draw()
#print(Tree_Str)





 
