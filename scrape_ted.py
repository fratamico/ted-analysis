#scrape ted talks
#this file takes multiple hours to run, but gets extensive information on each TED talk

from selenium import webdriver

outfile = open("ted_info.csv", 'a') #actually a tab separated file
outfile.write("\n")
#outfile.write("Name\turl\tJob\tTitle\tDate\tViewerCount\tLength\tAbstract\n") #uncomment this line and comment the one before it when starting from the beginning

driver = webdriver.Firefox()

#the start range in the following line should be 1 if you want to start scraping from the beginning
for page_num in range(34,56):
    url = "https://www.ted.com/talks?page=" + str(page_num)
    driver.get(url)

    video_max_num = 36
    if page_num == 55:
        video_max_num = 18

    #the following lines dictate which page and video to start scraping on. If wanting to get all videos, start_range should be 1
    start_range = 1
    if page_num == 34:
        start_range = 11
    for video_num in range(start_range,video_max_num + 1):

        #get video_href, date of video publication, author name, and video title by href
        video_href = driver.find_element_by_xpath('//*[@id="browse-results"]/div[1]/div[' + str(video_num) + ']/div/div/div/div[2]/h4[2]/a').get_attribute("href")
        date = driver.find_element_by_xpath('//*[@id="browse-results"]/div[1]/div[' + str(video_num) + ']/div/div/div/div[2]/div/span[2]/span').text.encode('utf8')
        name = driver.find_element_by_xpath('//*[@id="browse-results"]/div[1]/div[' + str(video_num) + ']/div/div/div/div[2]/h4[1]').text.encode('utf8')
        title = driver.find_element_by_xpath('//*[@id="browse-results"]/div[1]/div[' + str(video_num) + ']/div/div/div/div[2]/h4[2]/a').text.encode('utf8')

        #open a new window for each individual talk to scrape additional info
        subdriver = webdriver.Firefox()
        subdriver.get(video_href)

        try:
            #a few pages are formatted differently. Could add code here to scrape them differently, but I instead chose to ignore those pages (always videos with few views)
            length = subdriver.find_element_by_xpath('//*[@id="player-hero"]/div[1]/div[2]/div/span[1]').text.encode('utf8')
        except:
            print url, title
            subdriver.quit()
            continue

        try:
            #scrape the job of the talk giver. not always present
            job = subdriver.find_element_by_xpath('//*[@id="talk-pusher"]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]').text.encode('utf8')
        except:
            job = subdriver.find_element_by_xpath('//*[@id="talk-pusher"]/div[1]/div[2]/div[1]/div[1]/div/div/div[2]').text.encode('utf8')
        
        #get view count and abstract by xpath
        viewerCount = subdriver.find_element_by_xpath('//*[@id="sharing-count"]/span[1]').text.encode('utf8')
        abstract = subdriver.find_element_by_xpath('//*[@id="talk-pusher"]/div[1]/div[2]/div[1]/p').text.encode('utf8')

        transcript = ""
        try:
            #open a new page to get the talk transcript
            subdriver.get(video_href + "/transcript?language=en")

            paragraphs = subdriver.find_elements_by_class_name('talk-transcript__para__text')
            for paragraph in paragraphs:
                transcript += paragraph.text.encode('utf8') + "\n"
        except:
            print title

        #important to quit the subdriver window, otherwise you will end up with one open for each video (over 1900)
        subdriver.quit()

        #write the talk transcript to a file titled by the talk title
        transcript_file = open("transcripts/" + title + ".txt", 'w')
        transcript_file.write(transcript)
        transcript_file.close()

        #write all scraped info to a csv
        to_write = [name, url, job, title, date, viewerCount, length, abstract]
        outfile.write("\t".join(to_write) + "\n")

