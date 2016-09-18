#plots a histogram of the viewcounts 

import datetime
import numpy as np
import pylab as P
import xlrd

from xlrd import xldate


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
	print 'Row:', curr_row

	author_name = worksheet.cell_value(curr_row, 0)
	talk_title = worksheet.cell_value(curr_row, 3)
	viewcount = worksheet.cell_value(curr_row, 5)

	if author_name + ":" + talk_title in viewcount_dict:
		print author_name + ":" + talk_title
		raise "EWwe"

	viewcount_dict[author_name + ":" + talk_title] = [viewcount]

	#the following prints each cell value and cell type
	curr_cell = -1
	while curr_cell < num_cells:
		curr_cell += 1
		# Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
		cell_type = worksheet.cell_type(curr_row, curr_cell)
		cell_value = worksheet.cell_value(curr_row, curr_cell)
		print '	', cell_type, ':', cell_value


#to get the date
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

	try:
		viewcount_dict[author_name + ":" + talk_title].append(date_as_datetime)
	except:
		#author/title not in dictionary (because it was one of the weirdly formatted pages)
		print row
		continue


print len(viewcount_dict)


#plot the histogram
mu, sigma = 200, 25
x = mu + sigma*P.randn(10000)
#x = [1, 1, 1, 12, 2, 2, 3, 3, 4, 4, 2, 2, 3, 6, 7, 8, 9, 10]
x = [viewcount_dict[author_title][0] for author_title in viewcount_dict if viewcount_dict[author_title][0] > 5000000]
print x

# the histogram of the data with histtype='step'
n, bins, patches = P.hist(x, 500, normed=1, histtype='stepfilled')
P.setp(patches, 'facecolor', 'g', 'alpha', 0.75)


import matplotlib.pyplot as plt
from numpy.random import normal
gaussian_numbers = normal(size=1000)
plt.hist(x)
plt.title("Histogram of Viewcount of all TED videos")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()
