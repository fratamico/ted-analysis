import numpy
import string

def termFrequency(term, document):
    document_punctuation_removed = document.translate(string.maketrans("",""), string.punctuation)
    normalized_document = document_punctuation_removed.lower().split()

    term_count = normalized_document.count(term.lower())
    num_words = len(normalized_document)
    return term_count / float(num_words)


def inverseDocumentFrequency(term, allDocuments):
    #idf = num_documents/documents_with_terms
    num_docs_with_term = 0
    for doc in allDocuments:
        document_punctuation_removed = doc.translate(string.maketrans("",""), string.punctuation)
        if term.lower() in document_punctuation_removed.lower().split():
            num_docs_with_term += 1
 
    if num_docs_with_term > 0:
        return numpy.log(float(len(allDocuments)) / num_docs_with_term)
    #else:  ## will never reach else if only calling function with words in document
    #    return 1.0


def tfidf(term, document, allDocuments):
	return termFrequency(term, document) * inverseDocumentFrequency(term, allDocuments)



doc1 = ""
f1 = open("top_transcripts.txt", 'r')
lines1 = f1.readlines()
for line in lines1:
    doc1 += " " + line

doc2 = ""
f2 = open("bottom_transcripts.txt", 'r')
lines2 = f2.readlines()
for line in lines2:
    doc2 += " " + line


allDocuments = [doc1.lower(), doc2.lower()]

all_tfidf = {}
docID = 0
for document in allDocuments:
	docID += 1
	document_punctuation_removed = document.translate(string.maketrans("",""), string.punctuation)
	for term in set(document_punctuation_removed.split()):
		if not docID in all_tfidf:
			all_tfidf[docID] = {}
		all_tfidf[docID][term] = tfidf(term, document, allDocuments)

print all_tfidf[1]
total_values = 20

print "doc1 - top"
print len(doc1.split())
t = sorted(all_tfidf[1].iteritems(), key=lambda x:-x[1])[:total_values]
for x in t:
    print "{0}: {1}".format(*x)
    print termFrequency(x[0], doc1)*len(doc1.split())

print "doc2 - bottom"
print len(doc2.split())
t = sorted(all_tfidf[2].iteritems(), key=lambda x:-x[1])[:total_values]
for x in t:
    print "{0}: {1}".format(*x)
    print termFrequency(x[0], doc2)*len(doc2.split())


#examples
#print termFrequency("hello", "hello, this is lauren")

#doc1 = "hello hello hello hello"
#doc2 = "hello hi hey"
#print inverseDocumentFrequency("hello", [doc1, doc2])

