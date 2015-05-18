#this file scrapes the names, titles, and dates of ted talks (the stuff available on the https://www.ted.com/talks pages)

from selenium import webdriver

outfile = open("ted_info_name_title_date.csv", 'w') #actually a tab separated file
outfile.write("Name\tTitle\tDate\n")

driver = webdriver.Firefox()

for page_num in range(1,56):
    url = "https://www.ted.com/talks?page=" + str(page_num)
    driver.get(url)

    video_max_num = 36
    if page_num == 55: #page 55, the last page, has fewer videos on it
        video_max_num = 35
    
    start_range = 1
    for video_num in range(start_range,video_max_num + 1):

        #get the date, author name, and ted talk title by xpath
        date = driver.find_element_by_xpath('//*[@id="browse-results"]/div[1]/div[' + str(video_num) + ']/div/div/div/div[2]/div/span[2]/span').text.encode('utf8')
        name = driver.find_element_by_xpath('//*[@id="browse-results"]/div[1]/div[' + str(video_num) + ']/div/div/div/div[2]/h4[1]').text.encode('utf8')
        title = driver.find_element_by_xpath('//*[@id="browse-results"]/div[1]/div[' + str(video_num) + ']/div/div/div/div[2]/h4[2]/a').text.encode('utf8')

        to_write = [name, title, date]
        outfile.write("\t".join(to_write) + "\n")