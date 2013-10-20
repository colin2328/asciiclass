from pyspark import SparkContext
import json
import time
from operator import add
import math

print 'loading'
sc = SparkContext("spark://ec2-54-200-174-121.us-west-2.compute.amazonaws.com:7077", "Simple App")
# Replace `lay-k.json` with `*.json` to get a whole lot more data.
lay = sc.textFile('s3n://AKIAJFDTPC4XX2LVETGA:lJPMR8IqPw2rsVKmsSgniUd+cLhpItI42Z6DCFku@6885public/enron/lay-k.json')

json_lay = lay.map(lambda x: json.loads(x)).cache()



# calculate TF
senders = {"kenneth":"kenneth.lay", "lay":"kenneth.lay", "j.skilling":"jeff.skilling", "skilling":"jeff.skilling", "fastow":"andrew.fastow",  "a.fastow":"andrew.fastow",  "andrew.f":"andrew.fastow",  "rebecca.mark":"rebecca.mark", "r.mark":"rebecca.mark", "rebecca.m":"rebecca.mark", "rebeccam":"rebecca.mark", "stephen.cooper": "stephen.cooper",".stephen": "stephen.cooper", "s.cooper": "stephen.cooper", "cooper": "stephen.cooper"}

# def sent_by_executive(email):
#     return email['sender'].lower() in senders

# executive_emails = json_lay.filter(sent_by_executive)
# senders = json_lay.map(lambda x: x['sender']).distinct()

sender_terms = json_lay.flatMap(lambda x: [(x['sender'],term.lower()) for term in x['text'].split()]).countByValue().items()
sender_terms_count = sc.parallelize(sender_terms)
print sender_terms_count.take(5)


total_number_emails = 516893

terms = json_lay.flatMap(lambda x: [term.lower() for term in x['text'].split()]).countByValue().items()
terms_count = sc.parallelize(terms)
idfs = {}
for term_count in terms_count.collect():
    term = term_count[0]
    number_emails_with_term = term_count[1]
    idf = math.log(total_number_emails / number_emails_with_term)
    idfs[term] = idf

print terms_count.take(5)

#loop through each sender_terms_count. calculate tf idf for each
senders_to_term_count = sender_terms_count.groupBy(lambda sender_term_count: sender_term_count[0][0])

def compute_tfidf(sender_term_counts):
    for sender_term_count in sender_term_counts:
        term = sender_term_count[0][1]
        tf = sender_term_count[1]
        tfidf = tf * idfs[term]
        return (sender, term, tfidf)
        
sender_term_idf = senders_to_term_count.map(compute_tfidf).groupBy(lambda sender_term_count: sender_term_count[0][0])



print sender_term_idf.take(5)



exit()
filtered_emails = json_lay.filter(email_by_executive)

def edit_sender(email):
    sender = ""
    for s in senders:
        if s in email['sender'].lower():
            sender = senders[s]
    return (sender, email["text"])

#edits the name of the sender for each email so they can then be aggregated
emails = filtered_emails.map(edit_sender)

#outputs (Sender, word),1
words = emails.flatMap(lambda x:[((x[0],i.lower()), 1) for i in x[1].split()])

import re
def my_filter(inp):
    word = inp[0][1]
    if len(word)>4 and re.match("^[A-Za-z]*$", word):
        return True
    else:
        return False

filtered_words = words.filter(my_filter)
a = filtered_words.reduceByKey(add)

#outputs (word, (user, frequency))
tf = a.map(lambda x: (x[0][1], (x[0][0], x[1])))


# OBTAIN INFORMATION TO CALCULATE IDF - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

email_texts = json_lay.map(lambda x: x['text'])

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

def my_filter2(inp):
    word = inp[0]
    if len(word)>4 and re.match("^[A-Za-z]*$", word):
        return True
    else:
        return False

idf = email_texts.flatMap(lambda x:  [(i.lower(), 1) for i in unique_list(x.split())])
filtered_idf = idf.filter(my_filter2)
idf2 = filtered_idf.reduceByKey(add)



# OBTAIN INFORMATION TO CALCULATE TF-IDF - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

join_res = tf.join(idf2)
tot_num_emails = json_lay.count()

#output: (word, user, tfidf)
tfidf = join_res.map(lambda x: (x[1][0][0],x[0], x[1][0][1]*math.log(tot_num_emails*1.0/x[1][1])))

#output: (user, (word, tfidf)) and aggregate by user
res = tfidf.map(lambda x: (x[0], (x[1],x[2]))).groupByKey()

def sorting(vals):
    d = {}
    for v in vals[1]:
        d[v[0]]=v[1]
    x = sorted(d, key=d.get, reverse=True)
    return (vals[0], [(x[0],d[x[0]]),(x[1],d[x[1]]),(x[2],d[x[2]]),(x[3],d[x[3]]),(x[4],d[x[4]])])
        
#sort words by tfidf    
top5 = res.map(sorting)
top5.collect()