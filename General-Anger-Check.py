
# coding: utf-8

# Takes as input an XLSX file or a folder of XLSX files. The column with tweet text must have the heading “TEXT”

# Outputs a CSV showing number and percent of anger keywords to provide a relative measure of anger in Twitter data.

# The anger keywords are: liar(s), lying, lies, hypocrite(s), hypocrisy, hypocritical, asshole(s), bullshit, fuck AND off, “fuck you”, disgrace(s), disgraced, disgraceful, “piece of shit”, “the fuck up”, piss(ed) AND off, STFU, disgusting, disgusted, disgusts, “go fuck yourself”, scum, infuriate(s), infuriating, infuriated.

#The occurrence of these keywords in baseline data collected for neutral keywords was about 1.4% of total tweets.





import pandas as pd
import numpy as np
from collections import Counter
from cytoolz import concat
import re
import os


def anger_(l):
    x = [w for w in re.findall(r'\bliar\b|\bliars\b|\blying\b|\blies\b|\bhypocrite\b|\bhypocrites\b|\bhypocrisy\b|\bhypocritical\b|\basshole\b|\bassholes\b|\bbullshit\b|\bdisgrace\b|\bdisgraces\b|\bdisgraced\b|\bdisgraceful\b|\bstfu\b|\bdisgusting\b|\bdisgusted\b|\bdisgusts\b|\bscum\b|\binfuriate\b|\binfuriates\b|\binfuriating',l)]
    a = [w for w in re.findall(r'\bfuck you\b|\bthe fuck up\b|\bpiece of shit\b|\bgo fuck yourself\b',l)]
    b = [w for w in re.findall(r'\b(piss)\b.*off',l)]
    c = [w for w in re.findall(r'\boff\b.*\b(piss)\b',l)]
    d = [w for w in re.findall(r'\b(pissed)\b.*\boff\b',l)]
    e = [w for w in re.findall(r'\boff\b.*\b(pissed)\b',l)]
    f = [w for w in re.findall(r'\b(fuck)\b.*\boff\b',l)]
    g = [w for w in re.findall(r'\boff\b.*\b(fuck)\b',l)]
    z = []
    lists = [x,a,b,c,d,e,f,g]
    for q in lists:
        for s in q:
            z.append(s)
    return z


def angertopic(filepath):
    df = pd.read_excel(filepath)
    df['bow'] = df['TEXT'].str.lower().str.replace(r'(https?://.+|[^\w#@]+|\d+)+',' ').str.split()
    df3 = df[df['bow'].isnull()==False].copy()
    df2 = df3[df3['TEXT'].str.contains('HDMA')==False].copy()
    df2['anger words'] = df2['TEXT'].str.lower().apply(anger_)
    words = list(concat(df2['anger words']))
    wordcounts = Counter(words)
    keywords = {'liar':0, 'liars':0,'lying':0, 'lies':0, 
                'hypocrite':0,'hypocrites':0, 'hypocrisy':0, 'hypocritical':0,
                'asshole':0, 'assholes':0, 'bullshit':0, 
                'fuck off':0, 'fuck you':0, 
                'disgrace':0, 'disgraces':0, 'disgraced':0, 'disgraceful':0, 
                'piece of shit':0, 'the fuck up':0, 
                'piss off':0, 'pissed off':0, 'STFU':0,
                'disgusting':0, 'disgusted':0, 'disgusts':0, 
                'go fuck yourself':0, 'scum':0, 
                'infuriate':0, 'infuriates':0, 'infuriating':0, 'infuriated':0}
    kw = pd.DataFrame.from_dict(keywords, orient='index')
    wc = pd.DataFrame.from_dict(wordcounts, orient='index')
    if 'fuck' in wc.index:
        wc.index.set_value(wc.index, 'fuck', 'fuck off')
    if 'piss' in wc.index:
        wc.index.set_value(wc.index, 'piss', 'piss off')
    if 'pissed' in df.index:
        wc.index.set_value(wc.index, 'pissed', 'pissed off')
    counts = kw.join(wc, how='left', lsuffix = 'kw', rsuffix = 'wc').fillna(0)
    counts['Counts'] = counts['0kw'] + counts['0wc']
    del counts['0kw']
    del counts['0wc']
    counts.loc['~Total'] = counts.sum()
    counts.loc['~Tweet Count'] = len(df2)
    counts['Percent'] = (counts['Counts']/len(df2))*100
    name = os.path.basename(filepath).split('.')[0] + ' anger.csv'
    counts.sort_index(axis=0, ascending=True).to_csv(os.path.join(os.path.dirname(filepath),name))

def angertopics(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx"):
            angertopic(os.path.join(directory, filename))
            continue
        else:
            continue


print('Type angertopic(file) or angertopics(folder)to process XLSX files.')



