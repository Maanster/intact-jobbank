from selenium import webdriver
import time

ABWAGE = 27.28
BCWAGE = 25.00
MBWAGE = 21.60
NBWAGE = 20.12
NLWAGE = 23.00
NTWAGE = 34.36
NSWAGE = 20.00
NUWAGE = 32.00
ONWAGE = 24.04
PEIWAGE = 20.00
QBWAGE = 23.08
SKWAGE = 24.55
YTWAGE = 30.00

driver = webdriver.Chrome()
driver.maximize_window()


def main():
    login()
    on_site()
    sort_list()
    invite()
    next_page()


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


def on_site():
    access_jobs_list = driver.find_element_by_xpath('//*[@id="employerNavs"]/li/ul/li[4]/a')
    access_jobs_list.click()
    driver.implicitly_wait(2)
    number_of_show_jobs = driver.find_element_by_xpath('//select[@name="joblist_length"]/option[text()="100"]')
    number_of_show_jobs.click()
    driver.implicitly_wait(2)
    access_job = driver.find_element_by_xpath('//*[@id="row_1724712"]/td[11]/a')
    access_job.click()


def sort_list():
    driver.implicitly_wait(3)
    sorter = driver.find_element_by_xpath('/html/body/div/div/main/div[5]/div[1]/div[4]/form[2]/div[1]/div/table/thead/tr/th[2]')
    sorter.click()
    sorter.click()
    number_of_shown_applications = driver.find_element_by_xpath('//select[@name="matchlistpanel_length"]/option[text()="100"]')
    number_of_shown_applications.click()


def invite():
    table = driver.find_element_by_xpath('//*[@id="matchlistpanel"]/tbody')
    count = 0
    for profile in table.find_elements_by_css_selector('tr'):
        count = count + 1
        xpath_invited = '//*[@id="matchlistpanel"]/tbody/tr[' + str(count) + ']/td[9]/span/span[@class="wb-inv "]'
        invited = driver.find_element_by_xpath(xpath_invited)
        if invited.get_attribute("innerHTML") == "Not invited to apply":
            driver.implicitly_wait(3)
            time.sleep(25)
            xpath_button = '//*[@id="matchlistpanel"]/tbody/tr[' + str(count) + ']/td[1]/a'
            button = driver.find_element_by_xpath(xpath_button)
            button.click()
            driver.implicitly_wait(3)
            time.sleep(2)
            invite_profile = driver.find_element_by_id('j_id_7:j_id_17')
            invite_profile.click()
            # close = driver.find_element_by_xpath('//*[@id="howtoapply"]/div[2]/button')
            # close.click()


#checks number of applicants by the 100. for every 100. click next page
def next_page():
    number_of_applicants = driver.find_element_by_xpath('//*[@id="matchlistpanel_info"]').text
    if "1 to 100" in number_of_applicants:
        if "1 to 100 of 100" not in number_of_applicants:
            driver.find_element_by_xpath('//*[@id="matchlistpanel_next"]').click()
            invite()
    if "101 to 200" in number_of_applicants:
        if "101 to 200 of 200" not in number_of_applicants:
            driver.find_element_by_xpath('//*[@id="matchlistpanel_next"]').click()
            invite()
    if "201 to 300" in number_of_applicants:
        if "201 to 300 of 300" not in number_of_applicants:
            driver.find_element_by_xpath('//*[@id="matchlistpanel_next"]').click()
            invite()
    if "301 to 400" in number_of_applicants:
        if "301 to 400 of 400" not in number_of_applicants:
            driver.find_element_by_xpath('//*[@id="matchlistpanel_next"]').click()
            invite()

# check the province and set high or low wage
def is_high_wage():
    job_wage = driver.find_element_by_xpath('/html/body/div/div/main/div[4]/div/div/ul/li[2]/text()')
    province = driver.find_element_by_xpath('/html/body/div/div/main/div[5]/div[2]/div/div/dl/dt[2]')
    if province == 'British Colombia':
        if job_wage > BCWAGE:
            return True
        else:
            return False
    if province == 'Saskatchewan':
        if job_wage > SKWAGE:
            return True
        else:
            return False
    if province == 'Alberta':
        if job_wage > ABWAGE:
            return True
        else:
            return False


if __name__ == '__main__':
    main()
