import nltk
import re
import pandas as pd
from IPython.display import display
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
    for token in prog_tokens:
        if(re.findall(reg_statements,token)):
            ttype = 'Statement'
        elif(re.findall(reg_op,token)):
            ttype = 'operator'
        elif(re.findall(reg_nums,token)):
            ttype = 'Number'
        elif(re.findall(reg_id,token)):
            ttype = 'identifier'
        elif(re.findall(reg_sc,token)):
            ttype = 'specialCharacter'
        else:
            ttype = 'Unknown'
        df.loc[len(df)] = [token,ttype]
    display(df)
    return prog_tokens

class Node:
    def __init__(self,data,children):
        self.data = data
        self.children = children

#fileDirec = input('inter file directory')
prog_tokens = lexAnalyzer('code.cplg')#(fileDirectory=fileDirec)
tokens_stack = []
for token in prog_tokens:
    tokens_stack.append(token)
letterRule = []
for x in range (65,91):
    letterRule.append(chr(x))
for x in range (97,123):
    letterRule.append(chr(x))
letterRule.append('_')
letter = Node(data ='letter',children=letterRule)
digitRule = []
for x in range(48,58):
    digitRule.append(chr(x))
print(digitRule)
digit = Node(data='digit',children=digitRule)
#id1 = Node(data = 'id1',children=[digit,id1])
#print(tree.children[len(tree.children)-1])
