from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import glob
import os
import json


teams = {}
splits = {}

def dictionary_loader():
    with open("teams") as f:
        for line in f:
            (key,val) = line.split()
            teams[key] = val
    with open("splits") as q:
        for line in q:
            (key,val) = line.split()
            splits[key] = val

def renamer(i, j):

    i,j = str(i), str(j)
    team = teams.get(i)
    split = splits.get(j)
    time.sleep(3)
    list_of_files = glob.glob('/home/piotr/Downloads/*.csv')
    latest_file = max(list_of_files, key=os.path.getctime)
    old_file = os.path.join("/home/piotr/Downloads/", latest_file)
    new_file = os.path.join("./files", team+"_"+split+".csv")
    os.rename(old_file,new_file)

def main():
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)

    screen_name = config_data["screen_name"]
    passw0rd= config_data["password"]

    browser.get('https://www.fangraphs.com/blogs/wp-login.php?redirect_to=https%3a%2f%2fwww.fangraphs.com%2findex.aspx')
    time.sleep(3)
    username = browser.find_element_by_id("user_login")
    password = browser.find_element_by_id("user_pass")

    username.send_keys(screen_name)
    password.send_keys(passw0rd)
    browser.find_element_by_name("wp-submit").click()

    browser.get("https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=80&type=c,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,34,35,37,38,39,40,41,50,51,52,54&season=2017&month=57&season1=2013&ind=0&team=1&rost=1&age=0&filter=&players=0")

    i = 0 #team counter
    j = 0 #split counter

    while i<30:

        if i==0:
            browser.find_element_by_id("LeaderBoard1_cmdCSV").click() #first download already in place
            time.sleep(5)
            renamer(i,j)
            j+=1

        for j in range(j,4):
            Hand_element = browser.find_element_by_name("LeaderBoard1$rcbMonth") #find split label, go down one, press enter
            Hand_element.click()
            Hand_element.send_keys(Keys.ARROW_DOWN+Keys.RETURN)
            browser.find_element_by_id("LeaderBoard1_cmdCSV").click()
            time.sleep(5)
            renamer(i,j)

        Team_element = browser.find_element_by_name("LeaderBoard1$rcbTeam") #find team label, go down one, press enter
        Team_element.click()
        Team_element.send_keys(Keys.ARROW_DOWN + Keys.RETURN)

        Hand_element = browser.find_element_by_name("LeaderBoard1$rcbMonth")  # find split label, go up 4 times to reset handedness
        Hand_element.click()
        Hand_element.send_keys(Keys.ARROW_UP + Keys.ARROW_UP + Keys.ARROW_UP + Keys.RETURN)

        i+=1
        j=0

        browser.find_element_by_id("LeaderBoard1_cmdCSV").click() # download after reset
        time.sleep(5)
        renamer(i,j)
        j+=1

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    #options.add_extension('AdBlock_v3.27.0.crx')
    browser = webdriver.Chrome(chrome_options=options)
    dictionary_loader()
    main()
