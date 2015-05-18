#scrape ted talks

from selenium import webdriver

outfile = open("ted_info.csv", 'a') #actually a tab separated file
outfile.write("\n")
#outfile.write("Name\turl\tJob\tTitle\tDate\tViewerCount\tLength\tAbstract\n")

driver = webdriver.Firefox()

for page_num in range(34,56):
    url = "https://www.ted.com/talks?page=" + str(page_num)
    driver.get(url)

    video_max_num = 36
    if page_num == 55:
        video_max_num = 18
    start_range = 1
    if page_num == 34:
        start_range = 11
    for video_num in range(start_range,video_max_num + 1):

        video_href = driver.find_element_by_xpath('//*[@id="browse-results"]/div[1]/div[' + str(video_num) + ']/div/div/div/div[2]/h4[2]/a').get_attribute("href")
        date = driver.find_element_by_xpath('//*[@id="browse-results"]/div[1]/div[' + str(video_num) + ']/div/div/div/div[2]/div/span[2]/span').text.encode('utf8')
        name = driver.find_element_by_xpath('//*[@id="browse-results"]/div[1]/div[' + str(video_num) + ']/div/div/div/div[2]/h4[1]').text.encode('utf8')
        title = driver.find_element_by_xpath('//*[@id="browse-results"]/div[1]/div[' + str(video_num) + ']/div/div/div/div[2]/h4[2]/a').text.encode('utf8')

        subdriver = webdriver.Firefox()
        subdriver.get(video_href)

        try:
            length = subdriver.find_element_by_xpath('//*[@id="player-hero"]/div[1]/div[2]/div/span[1]').text.encode('utf8')
        except:
            print url, title
            subdriver.quit()
            continue

        try:
            job = subdriver.find_element_by_xpath('//*[@id="talk-pusher"]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]').text.encode('utf8')
        except:
            job = subdriver.find_element_by_xpath('//*[@id="talk-pusher"]/div[1]/div[2]/div[1]/div[1]/div/div/div[2]').text.encode('utf8')
        viewerCount = subdriver.find_element_by_xpath('//*[@id="sharing-count"]/span[1]').text.encode('utf8')
        abstract = subdriver.find_element_by_xpath('//*[@id="talk-pusher"]/div[1]/div[2]/div[1]/p').text.encode('utf8')

        transcript = ""
        try:
            subdriver.get(video_href + "/transcript?language=en")

            paragraphs = subdriver.find_elements_by_class_name('talk-transcript__para__text')
            for paragraph in paragraphs:
                transcript += paragraph.text.encode('utf8') + "\n"
        except:
            print title

        subdriver.quit()

        transcript_file = open(title + ".txt", 'w')
        transcript_file.write(transcript)
        transcript_file.close()

        to_write = [name, url, job, title, viewerCount, length, abstract]
        outfile.write("\t".join(to_write) + "\n")

