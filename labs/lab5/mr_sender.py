import sys
from mrjob.protocol import JSONValueProtocol
from mrjob.job import MRJob
from term_tools import get_terms
import math, copy, itertools
import operator

class MRSender(MRJob):

	INPUT_PROTOCOL = JSONValueProtocol
	OUTPUT_PROTOCOL = JSONValueProtocol

	def mapper1(self, key, email):
		for term in get_terms(email['text']): #terms is a list of terms
			yield {'sender': email['sender'], 'term': term}, 1

	def reducer1(self, sender_term, counts):
		yield sender_term, sum(counts)

	def mapper2(self, sender_term, count):
		yield sender_term['term'], {'sender': sender_term['sender'], 'count': count}


	def reducer2(self, term, sender_counts):
		total_number_emails = 516893
		sender_counts1, sender_counts2 = itertools.tee(sender_counts) # hack to get generator to be itereated on 2x
		number_emails_with_term = sum(1 for _ in sender_counts1)
		idf = math.log(total_number_emails / number_emails_with_term)

		for sender_count in sender_counts2:
			tf = sender_count['count']
			tfidf = tf * idf
			yield sender_count['sender'], {'term': term, 'tfidf': tfidf}

	def mapper3(self, sender, term_tfidf):
		yield sender, term_tfidf

	def reducer3(self, sender, term_tfidfs):
		term_tfidfs_dict = {}
		for term_tfidf in term_tfidfs:
			term_tfidfs_dict[term_tfidf['term']] = term_tfidf['tfidf']
		if sender == 'kenneth.lay@enron.com' or sender == 'jeff.skilling@enron.com' or sender == 'andrew.fastow@enron.com':
			vals = term_tfidfs_dict.values()
			vals.sort()
			vals.reverse()
			i = 0
			min_value = 1000
			while i < min(5, len(vals)):
				min_value = vals[i]
				i+=1
			rtn_dict = {}
			for term, value in term_tfidfs_dict.iteritems():
				if value > min_value:
					rtn_dict[term] = value
			yield None, {'sender': sender, 'tfidfs' : rtn_dict}

	def steps(self):
		return [self.mr(mapper=self.mapper1,
			reducer=self.reducer1),
			self.mr(mapper=self.mapper2,
				reducer=self.reducer2),
			self.mr(mapper=self.mapper3,
				reducer=self.reducer3)]

if __name__ == '__main__':
		MRSender.run()