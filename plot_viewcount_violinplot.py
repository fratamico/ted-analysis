import datetime
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import xlrd
from pandas import *
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
    print year

    try:
        viewcount_dict[author_name + ":" + talk_title].append(year)
    except:
        #author/title not in dictionary (because it was one of the weirdly formatted pages)
        print row
        continue


print len(viewcount_dict)


year_viewcount_dict = {}
for year in range(2006,2016):
    #create a dictionary for each year due to the input of the violin plot 
    year_viewcount_dict[year] = {}
year_viewcount_dict["All"] = {} #also have one that includes all years

for key, value in viewcount_dict.iteritems():
    #print value
    try:
        year = value[1]
    except:
        continue
        #this means that it did not have a year, likely because that author/talk was not in the date file
    viewcount = value[0]
    year_viewcount_dict[year][len(year_viewcount_dict[value[1]])] = viewcount
    year_viewcount_dict["All"][len(year_viewcount_dict[value[1]])] = viewcount

list_of_counts = [Series(year_viewcount_dict[year]) for year in ["All"] + range(2006,2016)] #turn into data type required for violinplot


labels = ["All"] + [str(year) for year in range(2006, 2016)] #note that they started in June of 2006 and that this data only invludes up to april 2015
plt.rcParams['figure.subplot.bottom'] = 0.23  # keep labels visible
fig = plt.figure()
ax = fig.add_subplot(111)
sm.graphics.violinplot(list_of_counts, ax=ax, labels=labels,
                       plot_opts={'cutoff_val':5, 'cutoff_type':'abs',
                                  'label_fontsize':'small'})
ax.set_xlabel("Year")
ax.set_yscale("log") #set to log scale because the range of viewcounts
ax.set_ylabel("Viewcount of talks (log scale)")

#plt.show()
plt.savefig('violinplot_viewcounts.png', bbox_inches='tight')

