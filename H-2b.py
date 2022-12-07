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
    prog_tokens = nltk.wordpunct_tokenize(prog)

    reg_statements = "for"
    reg_op = "(\++)|(--)|(-)|(\+)|(=)|(==)|(\*)|(\/)|(%)|(<=)|(<)|(>)|(>=)|(\^)"
    reg_nums = "\d+"
    reg_id = "^[a-zA-Z_]+[a-zA-Z0-9_]*"
    reg_sc = ",|\(|\)|;|(\{)|(\})"
    df = pd.DataFrame(columns=['Token','Type'])
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
        #df2 = pd.DataFrame({token:ttype},index=[0])
        df.loc[len(df)] = [token,ttype]
        #df = df.append({token:ttype},ignore_index = True)
    display(df)
    return df

fileDirec = input('inter file directory')
df = lexAnalyzer(fileDirectory=fileDirec)