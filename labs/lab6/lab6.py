from pyspark import SparkContext
import json
import time
from operator import add
import math
import re
from collections import defaultdict

print 'loading'
sc = SparkContext("spark://ec2-54-200-174-121.us-west-2.compute.amazonaws.com:7077", "Simple App")
# Replace `lay-k.json` with `*.json` to get a whole lot more data.
lay = sc.textFile('s3n://AKIAJFDTPC4XX2LVETGA:lJPMR8IqPw2rsVKmsSgniUd+cLhpItI42Z6DCFku@6885public/enron/lay-k.json')

json_lay = lay.map(lambda x: json.loads(x)).cache()



# calculate TF
sender_terms = json_lay.flatMap(lambda x: [(x['sender'],term.lower()) for term in x['text'].split()]).countByValue().items()
sender_terms_count = sc.parallelize(sender_terms)
print sender_terms_count.take(5)


total_number_emails = 51689

term_counts = defaultdict(int)
terms = json_lay.flatMap(lambda x: [term_counts[term.lower() +=1 ] for term in x['text'].split()])
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
# print senders_to_term_count.take(5)

def compute_tfidf(sender_list):
    for sender_term_count in sender_list[1]:
        print sender_term_count
        print sender_term_count[0]
        term = sender_term_count[0][1]
        tf = sender_term_count[1]
        tfidf = tf * idfs[term]
        return (sender_list[0], term, tfidf)

sender_term_idf = senders_to_term_count.map(compute_tfidf)
print 'sender_term_idf', sender_term_idf.take(5)

# grouped_idf = sender_term_idf.groupBy(lambda sender_term_idf: sender_term_idf[0])
# print 'grouped_idf', grouped_idf.take(5)

def filter_by(pattern):
    return sender_term_idf.filter(lambda x: re.match(pattern, x[0]))

filter_ken = filter_by('(ken.lay|kenneth.lay|lay.ken).*')
print 'ken', sorted(filter_ken.collect(), key=lambda x: x[2], reverse=True)[:10]

filter_jeff = filter_by('(jeff.skilling|jefferey.skilling|skilling.jeff).*')
print 'jeff', sorted(filter_jeff.collect(), key=lambda x: x[2], reverse=True)[:10]

filter_andrew = filter_by('(andrew.fastow|andy.fastow|fastow.andy).*')
print 'andrew', sorted(filter_andrew.collect(), key=lambda x: x[2], reverse=True)[:10]