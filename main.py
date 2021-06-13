from selenium import webdriver
import time
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from list_of_companies import list_of_companies


driver = webdriver.Chrome()
driver.maximize_window()


def main():
    login()
    access_jobs()


# logs into website
def login():
    driver.get('https://employer.jobbank.gc.ca/employer/jobpostings/0')

    email_input = driver.find_element_by_xpath('//*[@id="loginForm:input-email"]')
    email_input.send_keys('anoo.intactimmigration@gmail.com')

    password_input = driver.find_element_by_xpath('//*[@id="loginForm:input-password"]')
    password_input.send_keys("Intact@123")

    sign_in = driver.find_element_by_xpath('//*[@id="loginForm:j_id_3x"]')
    sign_in.click()

    security_question = driver.find_element_by_xpath('//*[@id="securityForm"]/fieldset/div/p').text
    question_input = driver.find_element_by_xpath('//*[@id="securityForm:input-security-answer"]')
    if security_question == "What is your father's middle name?":
        question_input.send_keys('Chander')
    if security_question == "Who was your most memorable school teacher?":
        question_input.send_keys('joel')
    if security_question == "Where did you first meet your significant other?":
        question_input.send_keys('Chandigarh')
    if security_question == "":
        question_input.send_keys('Chander')
    if security_question == "":
        question_input.send_keys('Chander')

    login_continue = driver.find_element_by_xpath('//*[@id="continueButton"]')
    login_continue.click()


# after logging in, finds which job to access
def access_jobs():
    access_jobs_list = driver.find_element_by_xpath('//*[@id="employerNavs"]/li/ul/li[4]/a')
    access_jobs_list.click()
    driver.implicitly_wait(2)
    number_of_show_jobs = driver.find_element_by_xpath('//select[@name="joblist_length"]/option[text()="100"]')
    number_of_show_jobs.click()
    driver.implicitly_wait(2)
    for i in range(3):
        find_jobs()
        driver.find_element_by_xpath('//*[@id="joblist_next"]').click()
        time.sleep(10)


# loop through jobs and sees which ones are found in list.
def find_jobs():
    time.sleep(3)
    table = driver.find_element_by_xpath('//*[@id="joblist"]/tbody')
    count = 0
    for companies in table.find_elements_by_css_selector('tr'):
        count = count + 1
        xpath_company_name = '//*[@id="joblist"]/tbody/tr[' + str(count) + ']/td[6]'
        xpath_access_company = '//*[@id="joblist"]/tbody/tr[' + str(count) + ']/td[11]/a'
        try:
            company = driver.find_element_by_xpath(xpath_company_name).get_attribute("innerHTML")
            company_link = driver.find_element_by_xpath(xpath_access_company)
            if company in list_of_companies:
                company_link.click()
                sort_list()
                loop_invite()
                next_page()
                time.sleep(8)
                driver.get('https://employer.jobbank.gc.ca/employer/jobpostings/0')
                driver.implicitly_wait(3)
                time.sleep(15)
        except NoSuchElementException:
            continue


# sorts inside jobs list. sorts stars descending and shows 100 profiles per page.
def sort_list():
    driver.implicitly_wait(3)
    sorter = driver.find_element_by_xpath('/html/body/div/div/main/div[5]/div[1]/div[4]/form[2]/div[1]/div/table/thead/tr/th[2]')
    sorter.click()
    sorter.click()
    number_of_shown_applications = driver.find_element_by_xpath('//select[@name="matchlistpanel_length"]/option[text()="100"]')
    number_of_shown_applications.click()


# invites profiles within a job. detects if profile is canadian and not already invited.
def invite():
    table = driver.find_element_by_xpath('//*[@id="matchlistpanel"]/tbody')
    count = 0
    length = 15
    number_of_applicants = driver.find_element_by_xpath('//*[@id="matchlistpanel_info"]').text
    if "1 to 100" in number_of_applicants:
        length = 30
    for profile in table.find_elements_by_css_selector('tr'):
        count = count + 1
        xpath_if_invited = '//*[@id="matchlistpanel"]/tbody/tr[' + str(count) + ']/td[9]/span/span[@class="wb-inv "]'
        xpath_if_intact = '//*[@id="matchlistpanel"]/tbody/tr[' + str(count) + ']/td[2]/span'
        star_rating = '//*[@id="matchlistpanel"]/tbody/tr[' + str(count) + ']/td[3]/span/span[1]'
        invited = driver.find_element_by_xpath(xpath_if_invited)
        intact = driver.find_element_by_xpath(xpath_if_intact)
        if star_rating.__getattribute__('class') == "star-matches-one-half" or "star-matches-one":
            break
        if invited.get_attribute("innerHTML") == "Invited to apply":
            continue
        if intact.get_attribute('class') == 'jb-canada-icon':
            if count != 1:
                time.sleep(length)
            xpath_button = '//*[@id="matchlistpanel"]/tbody/tr[' + str(count) + ']/td[1]/a'
            button = driver.find_element_by_xpath(xpath_button)
            button.click()
            driver.implicitly_wait(3)
            time.sleep(2)
            invite_profile = driver.find_element_by_id('j_id_7:j_id_17')
            invite_profile.click()


# if invite fails and leads to next blank page, goes back to previous page and repeats invite()
def loop_invite():
    try:
        invite()
    except StaleElementReferenceException:
        time.sleep(5)
        loop_invite()
    except:
        time.sleep(5)
        test = driver.find_element_by_class_name('modal-title').text
        if "Comparison chart" in test:
            driver.back()
            time.sleep(25)
            loop_invite()


# checks number of applicants by the 100. for every 100. click next page
def next_page():
    number_of_applicants = driver.find_element_by_xpath('//*[@id="matchlistpanel_info"]').text
    if "1 to 100" in number_of_applicants:
        if "1 to 100 of 100" not in number_of_applicants:
            driver.find_element_by_xpath('//*[@id="matchlistpanel_next"]').click()
            loop_invite()
    if "101 to 200" in number_of_applicants:
        if "101 to 200 of 200" not in number_of_applicants:
            driver.find_element_by_xpath('//*[@id="matchlistpanel_next"]').click()
            loop_invite()
    if "201 to 300" in number_of_applicants:
        if "201 to 300 of 300" not in number_of_applicants:
            driver.find_element_by_xpath('//*[@id="matchlistpanel_next"]').click()
            loop_invite()
    if "301 to 400" in number_of_applicants:
        if "301 to 400 of 400" not in number_of_applicants:
            driver.find_element_by_xpath('//*[@id="matchlistpanel_next"]').click()
            loop_invite()
    if "401 to 500" in number_of_applicants:
        if "401 to 500 of 500" not in number_of_applicants:
            driver.find_element_by_xpath('//*[@id="matchlistpanel_next"]').click()
            loop_invite()
    if "501 to 600" in number_of_applicants:
        if "501 to 600 of 600" not in number_of_applicants:
            driver.find_element_by_xpath('//*[@id="matchlistpanel_next"]').click()
            loop_invite()
    if "601 to 700" in number_of_applicants:
        if "601 to 700 of 700" not in number_of_applicants:
            driver.find_element_by_xpath('//*[@id="matchlistpanel_next"]').click()
            loop_invite()


if __name__ == '__main__':
    main()
