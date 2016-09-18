#this file calculates all the statistics reported in my blog post

import datetime
import matplotlib.pyplot as plt
import numpy as np
import operator
import re
import statsmodels.api as sm
import tfidf
import xlrd
from pandas import *
from xlrd import xldate
from wordcloud import WordCloud


#since I messed up when first scraping the data, I have the dates and viewcounts in separate files

#need to create a dictionary of 'author-title':[viewcount, date]
viewcount_dict = {}


#to get the viewcount
workbook = xlrd.open_workbook('ted_info.xlsx')
worksheet = workbook.sheet_by_name('Sheet1')
num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row = 0
while curr_row < num_rows:
    curr_row += 1
    row = worksheet.row(curr_row)
    #print 'Row:', curr_row

    author_name = worksheet.cell_value(curr_row, 0)
    talk_title = worksheet.cell_value(curr_row, 3)
    viewcount = int(worksheet.cell_value(curr_row, 5))

    if author_name + ":" + talk_title in viewcount_dict:
        #print author_name + ":" + talk_title
        raise "error in datafile, there is a duplicate"

    viewcount_dict[author_name + ":" + talk_title] = [viewcount]

    #the following prints each cell value and cell type
    #curr_cell = -1
    #while curr_cell < num_cells:
        #curr_cell += 1
        # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
        #cell_type = worksheet.cell_type(curr_row, curr_cell)
        #cell_value = worksheet.cell_value(curr_row, curr_cell)
        #print ' ', cell_type, ':', cell_value

#get the value of the least watched talk
least_watched_talk = min(viewcount_dict, key=viewcount_dict.get)

#to get the year
workbook = xlrd.open_workbook('ted_info_name_title_date.xlsx')
worksheet = workbook.sheet_by_name('Sheet1')
num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row = 0
while curr_row < num_rows:
    curr_row += 1
    row = worksheet.row(curr_row)

    author_name = worksheet.cell_value(curr_row, 0)
    talk_title = worksheet.cell_value(curr_row, 1)
    date = worksheet.cell_value(curr_row, 2)
    date_as_datetime = xldate.xldate_as_tuple(date, workbook.datemode)
    year, month, day, hour, minute, second = date_as_datetime

    try:
        viewcount_dict[author_name + ":" + talk_title].append(year)
    except:
        #author/title not in dictionary (because it was one of the weirdly formatted pages)
        #print row
        continue

print "least watched talk:"
print least_watched_talk, viewcount_dict[least_watched_talk]
print 

#to get the top 15 talks
print "top 15 talks:"
top15 = dict(sorted(viewcount_dict.iteritems(), key=operator.itemgetter(1), reverse=True)[:15])
for key, value in sorted(top15.iteritems(), key=operator.itemgetter(1), reverse=True):
    print key, value
print

#to get the bottom 15 talks
print "bottom 15 talks:"
bottom15 = dict(sorted(viewcount_dict.iteritems(), key=operator.itemgetter(1), reverse=False)[:20])
for key, value in sorted(bottom15.iteritems(), key=operator.itemgetter(1), reverse=True):
    print key, value
print

#to get the total number of talks (as of the date collected)
print "total talks:"
print len(viewcount_dict)



#to perform analysis on what the TED talk was about

#to get the agregate transcript of all x files
def get_transcript(dictionary, range_of_vals, top_or_bottom):
    #takes in the dictionary of viewcounts, range_of_vals is the number of talks together, top_or_bottom specifies weather you want to pull from top or bottom talks
    transcripts_string = ""
    titles = "\n"
    if top_or_bottom == "top":
        order = True
    elif top_or_bottom == "bottom":
        order = False
    else:
        raise "incorrect argument"

    count = 0
    item_to_get = 0
    while count < range_of_vals:
        print sorted(viewcount_dict.iteritems(), key=operator.itemgetter(1), reverse=order)[2]
        key, value = sorted(viewcount_dict.iteritems(), key=operator.itemgetter(1), reverse=order)[item_to_get]        
        item_to_get += 1 #will get the next item next iteration
        #for key in dict(sorted(viewcount_dict.iteritems(), key=operator.itemgetter(1), reverse=True)):
        print key
        title = key.split(":")[1]
        try:
            f = open("transcripts/" + title + ".txt", 'r')
        except:
            f = open('transcripts/"' + title + '".txt', 'r')
        lines = f.readlines()
        f.close()
        if len(lines) < 10: #if the transcript is too short, don't include it
            print "wwewwe"
            continue
        else:
            titles += title + "\n"
        for line in lines:
            transcripts_string += line
        count += 1
    #print transcripts_string
    #print key
    print titles
    raise "SSS"
    return transcripts_string

def plot_wordcloud(text, name):
    wordcloud = WordCloud(font_path='/Library/Fonts/Verdana.ttf').generate(text)
    # Open a plot of the generated image.
    #plt.clf()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(name + '_wordcloud.png', bbox_inches='tight')
    #plt.show()

def get_surrounding_words(word, body_of_text):
    #gets the surrounding +- 2 words in body_of_text around word
    surrounding_words = ""
    sub = r"([A-Za-z]+('[A-Za-z]+)?)(\W*)([A-Za-z]+('[A-Za-z]+)?)\W*(people)\W*([A-Za-z]+('[A-Za-z]+)?)\W*([A-Za-z]+('[A-Za-z]+)?)" #% word #refind string and get surrounding += 2 words
    surrounding_text = re.findall(sub, body_of_text, re.IGNORECASE)
    for word in surrounding_text:
        surrounding_words += " " + " ".join(word)
    surrounding_words = surrounding_words.lower().replace("people", "")
    #surrounding_words.replace("people", "")
    surrounding_words = ' '.join(word for word in surrounding_words.split() if len(word)>3) #remove 1 and 2 letter words
    return surrounding_words


#top_transcripts = get_transcript(viewcount_dict, 15, "top")
bottom_transcripts = get_transcript(viewcount_dict, 15, "bottom")


plot_wordcloud(top_transcripts, "top15")
plot_wordcloud(bottom_transcripts, "bottom15")


plot_wordcloud(get_surrounding_words("people", top_transcripts), "top15_around_people")




#save top and bottom transcript compolations to files
top_transcript = open("top_transcripts.txt", "w")
top_transcript.write(top_transcripts)

bottom_transcript = open("bottom_transcripts.txt", "w")
bottom_transcript.write(bottom_transcripts)


my_tfidf = tfidf.TfIdf("top_transcripts.txt")

