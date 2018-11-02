from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import pyperclip
import requests
import json
import time
import sys

api_key = 'YOUR-API-KEY'

def get_dynamic_list(url):
    """
    Description: Gets the contents of a
    dynamic URL
    -------------------------------------
    :param url: the url to pull from
    :return result: the result of the GET
    request
    -------------------------------------
    Use: v = get_driver(max_screen)
    """
    r = requests.get(url)
    r_text = r.text
    data = json.loads(r_text)
    contacts = data['contacts']

    print('HTTP Status Code:', r.status_code)
    print('Contacts retrieved:', len(contacts))
    contacts_array = []

    for i in contacts:
        first_name = i['properties']['firstname']['value']
        last_name = i['properties']['lastname']['value']
        try:
            company =  i['properties']['company']['value']
        except:
            company = 'No company property'
        profile_url = i['profile-url']
        new_contact = [first_name, last_name, company, profile_url]

        print('**************')
        print('First Name:', first_name)
        print('Last name:', last_name)
        print(company)
        print('Profile URL:', profile_url)

        contacts_array.append(new_contact)
    return contacts_array


def get_driver(max_screen):
    """
    Description: Gets a chrome driver
    session. User chooses if screen is
    maximized
    -------------------------------------
    :param max_screen: Boolean of if the
    chrome window should open maximized
    :return driver: and open chrome
    driver
    -------------------------------------
    Use: v = get_driver(max_screen)
    """
    if max_screen:
        options = webdriver.ChromeOptions()
        options.add_argument("--kiosk")
        driver = webdriver.Chrome(chrome_options=options)
        return driver
    elif not max_screen:
        driver = webdriver.Chrome()
        return driver
    else:
        print("parameter must be boolean")


def wait_for_element(element, driver, element_type):
    """
    Description: Will wait until the
    page has loaded the element before
    continuing
    -------------------------------------
    :param element: either a class name
    or id
    :param driver: the current driver
    :param element_type: either "class"
    or "id"
    :return:
    -------------------------------------
    Use: wait_for_element(element, driver, element_type)
    """
    if element_type == "class":
        try:
            myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, element)))
        except TimeoutException:
            print("Loading took too much time!")
            return False
    elif element_type == "id":
        try:
            myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element)))
        except TimeoutException:
            print("Loading took too much time!")
            return False
    elif element_type == 'xpath':
        try:
            myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, element)))
        except TimeoutException:
            print("Loading took too much time!")
            return False
    elif element_type == 'selector':
        try:
            myElem = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, element)))
        except TimeoutException:
            print("Loading took too much time!")
    else:
        print('Invalid type')
        return False
    return True


def login(credentials, driver):
    """
    Description: Logs the user into
    Hubspot
    -------------------------------------
    :param credentials: a 1d list with
    username at index 0 and password
    at index 1
    :param driver: the currently active
    driver
    :return:
    -------------------------------------
    Use: login(credentials, driver)
    """
    driver.get("https://app.hubspot.com/login")
    wait_for_element("login-email", driver, "class")
    login_user = driver.find_element_by_class_name("login-email")
    user = credentials[0]
    password = credentials[1]

    for letter in user:
        login_user.send_keys(letter)
        time.sleep(0.05)

    login_pass = driver.find_element_by_class_name("login-password")

    for letter in password:
        login_pass.send_keys(letter)
        time.sleep(0.05)

    login_pass.send_keys(Keys.ENTER)

    time.sleep(1)

    driver.get('YOUR-HUBSPOT-MAIN-URL')

    return


def get_emails(contacts, template, when, driver):
    """
    Description: Gets emails by url
    rather than search
    -------------------------------------
    :param contacts: a 2D list of contacts
     to search with their URLs provided
    :param driver: the currently active
    driver
    :param when: a list of when params
    :param template: string name of the
    template that should be used
    :return:
    -------------------------------------
    Use: search_emails(emails, driver)
    """
    # Set variables to fill out inputs

    date = when[0]
    send_time = when[1]
    am_pm = when[2]
    follow_up = when[3]
    follow_up_time = when[4]
    follow_up_am_pm = when[5]

    init_len = len(contacts) - 1

    while not contacts == []:
        new_email = contacts.pop()
        contact_name = new_email[0] + ' ' + new_email[1]
        contact_url = new_email[2]
        email = new_email[3]


        if len(contacts) > init_len:
            res = wait_for_element("inline-nav-search-bar", driver, "id")
            if not res:
                return 'Error'
            res = wait_for_element("inline-nav-search-bar", driver, "id")
            if not res:
                return 'Error'

            driver.get(contact_url)
        else:
            time.sleep(2)
            print(contact_url)
            driver.get(contact_url)

        res = wait_for_element('body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-4 > div > ul > li:nth-child(1) > section > div.is--module.has--vertical-spacing.private-card.private-card__wrapper.private-card--compact > div.private-card__height-transition.private-card__content-wrapper.private-height-transition > div > div > div > form > div.is--module.has--vertical-spacing > div:nth-child(4) > div.p-x-0.col-xs-12', driver, 'selector')
        if not res:
            return 'Error'
        time.sleep(0.05)
        driver.find_element(By.CSS_SELECTOR, value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-8 > div.onboarding-peek-communicator > div > div > div.private-tabs__list__wrapper > nav > a:nth-child(2)').click()

        if not res:
            return 'Error'
        time.sleep(0.5)
        driver.find_element_by_partial_link_text('Email').click()
        time.sleep(0.5)
        res = wait_for_element('public-DraftStyleDefault-block', driver, 'class')
        if not res:
            return 'Error'
        time.sleep(2)
        driver.find_element_by_xpath("//*[contains(text(), 'Sequences')]").click()
        time.sleep(1)

        res = wait_for_element('body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-8 > div.onboarding-peek-communicator > div > div > div.is--module.has--vertical-spacing.m-y-0.panel-is-email.private-tabs__panel > div > div.display-inline-flex.justify-between.width-100.crm-light-border-bottom.p-bottom-3.p-x-5 > div > div > span > div > div > div > div > div > div.private-flex.display-flex.sales-modal-header.p-x-8.p-bottom-3.align-center.justify-start > div.private-dropdown.private-typeahead.sales-content-search.m-right-3.sales-modal-search > div > input', driver, 'selector')
        if not res:
            return 'Error'
        time.sleep(1)
        search_bar = driver.find_element(By.CSS_SELECTOR, value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-8 > div.onboarding-peek-communicator > div > div > div.is--module.has--vertical-spacing.m-y-0.panel-is-email.private-tabs__panel > div > div.display-inline-flex.justify-between.width-100.crm-light-border-bottom.p-bottom-3.p-x-5 > div > div > span > div > div > div > div > div > div.private-flex.display-flex.sales-modal-header.p-x-8.p-bottom-3.align-center.justify-start > div.private-dropdown.private-typeahead.sales-content-search.m-right-3.sales-modal-search > div > input')
        search_bar.click()
        time.sleep(1)
        for l in template:
            search_bar.send_keys(l)
            time.sleep(0.05)

        wait_for_element('body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-8 > div.onboarding-peek-communicator > div > div > div.is--module.has--vertical-spacing.m-y-0.panel-is-email.private-tabs__panel > div > div.display-inline-flex.justify-between.width-100.crm-light-border-bottom.p-bottom-3.p-x-5 > div > div > span > div > div > div > div > div > div.private-flex.display-flex.sales-modal-header.p-x-8.p-bottom-3.align-center.justify-start > div.private-dropdown.private-typeahead.sales-content-search.m-right-3.sales-modal-search > ul > li > div > div', driver, 'selector')
        search_bar.send_keys(Keys.RETURN);

        time.sleep(1.5)

        res = wait_for_element('hs-pickadate', driver, 'class')
        if res:
            time.sleep(0.5)
            date_input_first = driver.find_element_by_class_name('hs-pickadate')
            date_input_first.click()
            time.sleep(1)
            # date_input = driver.find_element_by_class_name('form-control')
            # date_input.click()
            # time.sleep(0.5)
            # date_input.clear()
            # time.sleep(0.05)
            #
            # for l in date:
            #     date_input.send_keys(l)
            #     time.sleep(0.05)
            #
            # time.sleep(0.05)
            # date_input.send_keys(Keys.RETURN)
            # time.sleep(0.05)

            time_input = driver.find_element(By.CSS_SELECTOR, value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-8 > div.onboarding-peek-communicator > div > div > div.is--module.has--vertical-spacing.m-y-0.panel-is-email.private-tabs__panel > div > div.display-inline-flex.justify-between.width-100.crm-light-border-bottom.p-bottom-3.p-x-5 > div > div > span > div > div > div > div > div > div > div.private-flex.display-flex.modal-body.width-100.align-start.justify-start > div.enroll-modal-content.steps.p-right-3.p-bottom-3 > div:nth-child(2) > div.private-flex.display-flex.sequence-step-title-detail.align-center.justify-start > div.private-clickable.btn.uiButton.private-button.private-button--default.private-button--form.private-form__control.private-timepicker.sequence-step-title-time-selection.m-left-2.private-button__dropdown-opener.uiDropdown__button.private-hoverable.private-button--non-link')
            time_input.click()

            time_search = driver.find_element_by_class_name('private-search-control__input')
            time_search.click()

            for l in send_time:
                time_search.send_keys(l)
                time.sleep(0.05)
            time.sleep(0.05)

            if am_pm == 'pm':
                time_search.send_keys(Keys.DOWN)
                time.sleep(0.05)

            time_search.send_keys(Keys.RETURN)

            scroll_to = driver.find_element(By.CSS_SELECTOR, value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-8 > div.onboarding-peek-communicator > div > div > div.is--module.has--vertical-spacing.m-y-0.panel-is-email.private-tabs__panel > div > div.display-inline-flex.justify-between.width-100.crm-light-border-bottom.p-bottom-3.p-x-5 > div > div > span > div > div > div > div > div > div > div.private-flex.display-flex.modal-body.width-100.align-start.justify-start > div.enroll-modal-content.steps.p-right-3.p-bottom-3 > div:nth-child(3) > div.private-flex.display-flex.sequence-step-title-detail.align-center.justify-start > div.private-flex.display-flex.sequence-step-delay-selector.align-center.justify-start')

            actions = ActionChains(driver)
            actions.move_to_element(scroll_to).perform()

            follow_up_days = driver.find_element(By.CSS_SELECTOR, value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-8 > div.onboarding-peek-communicator > div > div > div.is--module.has--vertical-spacing.m-y-0.panel-is-email.private-tabs__panel > div > div.display-inline-flex.justify-between.width-100.crm-light-border-bottom.p-bottom-3.p-x-5 > div > div > span > div > div > div > div > div > div > div.private-flex.display-flex.modal-body.width-100.align-start.justify-start > div.enroll-modal-content.steps.p-right-3.p-bottom-3 > div:nth-child(3) > div.private-flex.display-flex.sequence-step-title-detail.align-center.justify-start > div.private-flex.display-flex.sequence-step-delay-selector.align-center.justify-start > div > div.private-clickable.btn.uiButton.private-button.private-button--default.private-button--form.private-form__control.delay-selector-dropdowns__number.m-right-2.private-button__dropdown-opener.uiDropdown__button.private-hoverable.private-button--non-link')
            follow_up_days.click()
            time.sleep(0.05)
            follow_up_days.send_keys(follow_up)
            time.sleep(0.05)
            follow_up_days.send_keys(Keys.RETURN)
            time.sleep(0.05)

            enter_follow_up_time = driver.find_element(By.CSS_SELECTOR, value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-8 > div.onboarding-peek-communicator > div > div > div.is--module.has--vertical-spacing.m-y-0.panel-is-email.private-tabs__panel > div > div.display-inline-flex.justify-between.width-100.crm-light-border-bottom.p-bottom-3.p-x-5 > div > div > span > div > div > div > div > div > div > div.private-flex.display-flex.modal-body.width-100.align-start.justify-start > div.enroll-modal-content.steps.p-right-3.p-bottom-3 > div:nth-child(3) > div.private-flex.display-flex.sequence-step-title-detail.align-center.justify-start > div.private-clickable.btn.uiButton.private-button.private-button--default.private-button--form.private-form__control.private-timepicker.sequence-step-title-time-selection.m-left-2.private-button__dropdown-opener.uiDropdown__button.private-hoverable.private-button--non-link')
            enter_follow_up_time.click()
            time.sleep(0.05)

            for l in follow_up_time:
                enter_follow_up_time.send_keys(l)
                time.sleep(0.05)

            if follow_up_am_pm == 'pm':
                enter_follow_up_time.send_keys(Keys.DOWN)
                time.sleep(0.05)

            enter_follow_up_time.send_keys(Keys.RETURN)
            time.sleep(0.05)

            enroll_check = driver.find_element(By.CSS_SELECTOR, value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-8 > div.onboarding-peek-communicator > div > div > div.is--module.has--vertical-spacing.m-y-0.panel-is-email.private-tabs__panel > div > div.display-inline-flex.justify-between.width-100.crm-light-border-bottom.p-bottom-3.p-x-5 > div > div > span > div > div > div > div > div > div > footer > div.sequence-enroll-warning-container > button')
            enroll_check.click()
            enroll_confirm = driver.find_element(By.CSS_SELECTOR, value='body > div.tether-element.tether-enabled.tether-element-attached-bottom.tether-element-attached-right.tether-target-attached-top.tether-target-attached-left > div > div.m-bottom-4 > button.btn.uiButton.private-button.private-button--default.private-button__link.btn-link.private-hoverable')
            enroll_confirm.click()

            print(contact_name + ' has been sequenced')
        else:
            print(contact_name + ' is already enrolled')

    return 'Completed'


def search_emails(emails, template, when, driver):
    """
    Description: Searches emails in
    Hubspot
    -------------------------------------
    :param emails: a 1d list emails that
     are to be searched
    :param driver: the currently active
    driver
    :param when: a list of when params
    :param template: string name of the
    template that should be used
    :return:
    -------------------------------------
    Use: search_emails(emails, driver)
    """

    #Set variables to fill out inputs

    date = when[0]
    send_time = when[1]
    am_pm = when[2]
    follow_up = when[3]
    follow_up_time = when[4]
    follow_up_am_pm = when[5]

    #sequence with selenium

    while not emails == []:
        new_email = emails.pop()

        res = wait_for_element("inline-nav-search-bar", driver, "id")
        if not res:
            return 'Error'
        search_bar = driver.find_element_by_id("inline-nav-search-bar")

        for letter in new_email:
            search_bar.send_keys(letter)
            time.sleep(0.05)

        res = wait_for_element('nav-search-item-link', driver, 'class')
        if not res:
            return 'Error'
        search_bar.send_keys(Keys.DOWN);
        time.sleep(0.05)
        search_bar.send_keys(Keys.RETURN);
        #res = wait_for_element('private-tabs__list', driver, 'class') #HERE
        time.sleep(0.05)

        driver.find_element(By.CSS_SELECTOR, value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-4 > div > ul > li:nth-child(1) > section > div.is--module.has--vertical-spacing.private-card.private-card__wrapper.private-card--compact > div.private-card__section.has--vertical-spacing.private-card__header.private-card__header--expandable > div > div > div').click()
        res = wait_for_element('body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-4 > div > ul > li:nth-child(1) > section > div.is--module.has--vertical-spacing.private-card.private-card__wrapper.private-card--compact > div.private-card__height-transition.private-card__content-wrapper.private-height-transition > div > div > div > form > div.is--module.has--vertical-spacing > div:nth-child(4) > div.p-x-0.col-xs-12', driver, 'selector')
        if not res:
            return 'Error'
        time.sleep(0.05)
        contact_email = driver.find_element(By.CSS_SELECTOR, value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-4 > div > ul > li:nth-child(1) > section > div.is--module.has--vertical-spacing.private-card.private-card__wrapper.private-card--compact > div.private-card__height-transition.private-card__content-wrapper.private-height-transition > div > div > div > form > div.is--module.has--vertical-spacing > div:nth-child(4) > div.p-x-0.col-xs-12').text.lower()
        time.sleep(0.05)
        driver.find_element(By.CSS_SELECTOR, value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-4 > div > ul > li:nth-child(1) > section > div.is--module.has--vertical-spacing.private-card.private-card__wrapper.private-card--compact > div.private-card__section.has--vertical-spacing.private-card__header.private-card__header--expandable > div > div > div > span > span > span > span > span > i18n-string').click()

        #just incase the wrong contact is selected
        while not new_email == contact_email:
            res = wait_for_element("inline-nav-search-bar", driver, "id")
            if not res:
                return 'Error'
            search_bar = driver.find_element_by_id("inline-nav-search-bar")

            for letter in new_email:
                search_bar.send_keys(letter)
                time.sleep(0.05)

            res = wait_for_element('nav-search-item-link', driver, 'class')
            if not res:
                return 'Error'
            search_bar.send_keys(Keys.DOWN);
            time.sleep(0.05)
            search_bar.send_keys(Keys.RETURN);
            res = wait_for_element('private-tabs__list', driver, 'class')
            if not res:
                return 'Error'
            time.sleep(0.05)

            driver.find_element(By.CSS_SELECTOR,
                                value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-4 > div > ul > li:nth-child(1) > section > div.is--module.has--vertical-spacing.private-card.private-card__wrapper.private-card--compact > div.private-card__section.has--vertical-spacing.private-card__header.private-card__header--expandable > div > div > div').click()
            res = wait_for_element(
                'body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-4 > div > ul > li:nth-child(1) > section > div.is--module.has--vertical-spacing.private-card.private-card__wrapper.private-card--compact > div.private-card__height-transition.private-card__content-wrapper.private-height-transition > div > div > div > form > div.is--module.has--vertical-spacing > div:nth-child(4) > div.p-x-0.col-xs-12',
                driver, 'selector')
            if not res:
                return 'Error'
            time.sleep(0.05)
            contact_email = driver.find_element(By.CSS_SELECTOR,
                                                value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-4 > div > ul > li:nth-child(1) > section > div.is--module.has--vertical-spacing.private-card.private-card__wrapper.private-card--compact > div.private-card__height-transition.private-card__content-wrapper.private-height-transition > div > div > div > form > div.is--module.has--vertical-spacing > div:nth-child(4) > div.p-x-0.col-xs-12').text.lower()
            time.sleep(0.05)
            driver.find_element(By.CSS_SELECTOR,
                                value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-4 > div > ul > li:nth-child(1) > section > div.is--module.has--vertical-spacing.private-card.private-card__wrapper.private-card--compact > div.private-card__section.has--vertical-spacing.private-card__header.private-card__header--expandable > div > div > div > span > span > span > span > span > i18n-string').click()

        if not res:
            return 'Error'
        time.sleep(0.5)

        driver.find_element_by_partial_link_text('Email').click()
        time.sleep(0.5)
        res = wait_for_element('public-DraftStyleDefault-block', driver, 'class')
        if not res:
            return 'Error'
        time.sleep(1)
        wait_for_element("//*[contains(text(), 'Sequences')]", driver, 'xpath')
        driver.find_element_by_xpath("//*[contains(text(), 'Sequences')]").click()
        time.sleep(1)
        # res = wait_for_element("//*[contains(text(), 'View all sequences')]", driver, 'xpath')
        # if not res:
        #     return 'Error'
        # driver.find_element_by_xpath("//*[contains(text(), 'View all sequences')]").click()
        res = wait_for_element('form-control', driver, 'class')
        if not res:
            return 'Error'
        time.sleep(0.5)
        search_bar = driver.find_element_by_class_name('form-control')
        search_bar.click()
        for l in template:
            search_bar.send_keys(l)
            time.sleep(0.05)

        wait_for_element('body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-8 > div.onboarding-peek-communicator > div > div > div.is--module.has--vertical-spacing.m-y-0.panel-is-email.private-tabs__panel > div > div.display-inline-flex.justify-between.width-100.crm-light-border-bottom.p-bottom-3.p-x-5 > div > div > span > div > div > div > div > div > div.private-flex.display-flex.sales-modal-header.p-x-8.p-bottom-3.align-center.justify-start > div.private-dropdown.private-typeahead.sales-content-search.m-right-3.sales-modal-search > ul > li > div > div', driver, 'selector')
        search_bar.send_keys(Keys.RETURN);

        res = wait_for_element('hs-pickadate', driver, 'class')
        if res:
            time.sleep(0.5)
            date_input_first = driver.find_element_by_class_name('hs-pickadate')
            date_input_first.click()
            time.sleep(0.5)
            date_input = driver.find_element_by_class_name('form-control')
            date_input.click()
            time.sleep(0.5)
            date_input.clear()
            time.sleep(0.05)

            for l in date:
                date_input.send_keys(l)
                time.sleep(0.05)

            time.sleep(0.05)
            date_input.send_keys(Keys.RETURN)
            time.sleep(0.05)

            time_input = driver.find_element(By.CSS_SELECTOR, value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-8 > div.onboarding-peek-communicator > div > div > div.is--module.has--vertical-spacing.m-y-0.panel-is-email.private-tabs__panel > div > div.display-inline-flex.justify-between.width-100.crm-light-border-bottom.p-bottom-3.p-x-5 > div > div > span > div > div > div > div > div > div > div.private-flex.display-flex.modal-body.width-100.align-start.justify-start > div.enroll-modal-content.steps.p-right-3.p-bottom-3 > div:nth-child(2) > div.private-flex.display-flex.sequence-step-title-detail.align-center.justify-start > div.private-clickable.btn.uiButton.private-button.private-button--default.private-button--form.private-form__control.private-timepicker.sequence-step-title-time-selection.m-left-2.private-button__dropdown-opener.uiDropdown__button.private-hoverable.private-button--non-link')
            time_input.click()

            time_search = driver.find_element_by_class_name('private-search-control__input')
            time_search.click()

            for l in send_time:
                time_search.send_keys(l)
                time.sleep(0.05)
            time.sleep(0.05)

            if am_pm == 'pm':
                time_search.send_keys(Keys.DOWN)
                time.sleep(0.05)

            time_search.send_keys(Keys.RETURN)

            scroll_to = driver.find_element(By.CSS_SELECTOR, value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-8 > div.onboarding-peek-communicator > div > div > div.is--module.has--vertical-spacing.m-y-0.panel-is-email.private-tabs__panel > div > div.display-inline-flex.justify-between.width-100.crm-light-border-bottom.p-bottom-3.p-x-5 > div > div > span > div > div > div > div > div > div > div.private-flex.display-flex.modal-body.width-100.align-start.justify-start > div.enroll-modal-content.steps.p-right-3.p-bottom-3 > div:nth-child(3) > div.private-flex.display-flex.sequence-step-title-detail.align-center.justify-start > div.private-flex.display-flex.sequence-step-delay-selector.align-center.justify-start')

            actions = ActionChains(driver)
            actions.move_to_element(scroll_to).perform()

            follow_up_days = driver.find_element(By.CSS_SELECTOR, value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-8 > div.onboarding-peek-communicator > div > div > div.is--module.has--vertical-spacing.m-y-0.panel-is-email.private-tabs__panel > div > div.display-inline-flex.justify-between.width-100.crm-light-border-bottom.p-bottom-3.p-x-5 > div > div > span > div > div > div > div > div > div > div.private-flex.display-flex.modal-body.width-100.align-start.justify-start > div.enroll-modal-content.steps.p-right-3.p-bottom-3 > div:nth-child(3) > div.private-flex.display-flex.sequence-step-title-detail.align-center.justify-start > div.private-flex.display-flex.sequence-step-delay-selector.align-center.justify-start > div > div.private-clickable.btn.uiButton.private-button.private-button--default.private-button--form.private-form__control.delay-selector-dropdowns__number.m-right-2.private-button__dropdown-opener.uiDropdown__button.private-hoverable.private-button--non-link')
            follow_up_days.click()
            time.sleep(0.05)
            follow_up_days.send_keys(follow_up)
            time.sleep(0.05)
            follow_up_days.send_keys(Keys.RETURN)
            time.sleep(0.05)

            enter_follow_up_time = driver.find_element(By.CSS_SELECTOR, value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-8 > div.onboarding-peek-communicator > div > div > div.is--module.has--vertical-spacing.m-y-0.panel-is-email.private-tabs__panel > div > div.display-inline-flex.justify-between.width-100.crm-light-border-bottom.p-bottom-3.p-x-5 > div > div > span > div > div > div > div > div > div > div.private-flex.display-flex.modal-body.width-100.align-start.justify-start > div.enroll-modal-content.steps.p-right-3.p-bottom-3 > div:nth-child(3) > div.private-flex.display-flex.sequence-step-title-detail.align-center.justify-start > div.private-clickable.btn.uiButton.private-button.private-button--default.private-button--form.private-form__control.private-timepicker.sequence-step-title-time-selection.m-left-2.private-button__dropdown-opener.uiDropdown__button.private-hoverable.private-button--non-link')
            enter_follow_up_time.click()
            time.sleep(0.05)

            for l in follow_up_time:
                enter_follow_up_time.send_keys(l)
                time.sleep(0.05)

            if follow_up_am_pm == 'pm':
                enter_follow_up_time.send_keys(Keys.DOWN)
                time.sleep(0.05)

            enter_follow_up_time.send_keys(Keys.RETURN)
            time.sleep(0.05)

            enroll_check = driver.find_element(By.CSS_SELECTOR, value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-8 > div.onboarding-peek-communicator > div > div > div.is--module.has--vertical-spacing.m-y-0.panel-is-email.private-tabs__panel > div > div.display-inline-flex.justify-between.width-100.crm-light-border-bottom.p-bottom-3.p-x-5 > div > div > span > div > div > div > div > div > div > footer > div.sequence-enroll-warning-container > button')
            enroll_check.click()
            enroll_confirm = driver.find_element(By.CSS_SELECTOR, value='body > div.tether-element.tether-enabled.tether-element-attached-bottom.tether-element-attached-right.tether-target-attached-top.tether-target-attached-left > div > div.m-bottom-4 > button.btn.uiButton.private-button.private-button--default.private-button__link.btn-link.private-hoverable')
            enroll_confirm.click()

            print(new_email + ' has been sequenced')
        else:
            print(new_email + ' is already enrolled')

    return 'Completed'


def send_template(contact, template, driver):

    """
    Description: Searches emails in
    Hubspot and sends templates
    -------------------------------------
    :param contact: a 1d list of contact
    information
    :param driver: the currently active
    driver
    :param template: a 1d list containing
    [subject, msg]
    :return string: how process went
    -------------------------------------
    Use: search_emails(emails, driver)
    """

    # Sort contact info into variables

    contact_id = contact[0]

    contact_json = json.loads(requests.get(
        'https://api.hubapi.com/contacts/v1/contact/vid/' + contact_id + '/profile?hapikey=' + api_key).text)
    try:
        first_name = contact_json['properties']['firstname']['value'].strip()
        last_name = contact_json['properties']['lastname']['value'].strip()
    except:
        first_name = 'there'
        last_name = None

    if last_name:
        full_name = first_name, last_name
    else:
        full_name = 'No name found'

    # Set variables to fill out inputs

    subject = template[0]
    body = [
        'Hi %s,' % first_name,

        'How are you',

        'Best Regards,',

        'ME'

    ]

    # sequence with selenium

    try:
        driver.get('YOUR MAIN HUBSPOT URL' + contact_id + '/')

        res = wait_for_element(
                'body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-4 > div > ul > li:nth-child(1) > section > div.is--module.has--vertical-spacing.private-card.private-card__wrapper.private-card--compact > div.private-card__height-transition.private-card__content-wrapper.private-height-transition > div > div > div > form > div.is--module.has--vertical-spacing > div:nth-child(4) > div.p-x-0.col-xs-12',
                driver, 'selector')
        if not res:
            return 'Error'
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, value='body > div.app > div > div > div > div > div:nth-child(2) > div > div > div > div > div.p-top-5.p-bottom-10.align-center.UIColumn-spreads.overflowVisible > div.row.p-x-0.width-100.m-x-0 > div.col-xs-12.col-sm-8 > div.onboarding-peek-communicator > div > div > div.private-tabs__list__wrapper > nav > a:nth-child(2)').click()
        time.sleep(0.5)
        res = wait_for_element('public-DraftStyleDefault-block', driver, 'class')
        if not res:
            return 'Error'
        time.sleep(1)
        subject_box = driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div[2]/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div/div/div[2]/div/div[2]/div/div[3]/div[2]/input")
        subject_box.click()
        time.sleep(1)

        for l in subject:
            subject_box.send_keys(l)
            time.sleep(0.01)

        time.sleep(0.05)
        body_box = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div/div/div[2]/div/div[3]/div[1]/div/div[1]/div/div')
        time.sleep(1)

        for line in body:
            if line == '#LV18IL':
                for l in line:
                    body_box.send_keys(l)
                    time.sleep(0.01)
                time.sleep(2)
                body_box.send_keys(Keys.RETURN)
                time.sleep(2.5)
            else:
                pyperclip.copy(line)
                body_box.send_keys(pyperclip.paste())
                time.sleep(0.5)

            time.sleep(1)
            body_box.send_keys(Keys.RETURN)
            time.sleep(0.03)
            body_box.send_keys(Keys.RETURN)

        time.sleep(0.05)
        send_button = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div/div/div[2]/div/div[3]/div[3]/div/div/div[1]/div/button[1]')
        time.sleep(1)
        ActionChains(driver).move_to_element(send_button).click().perform()
        time.sleep(1.2)

        return 'Contact ID:', contact_id, 'Contact Name:', full_name, 'Status: email successful'

    except Exception as e:
        print(e)
        print('Contact ID:', contact_id, 'Contact Name:', full_name, 'Status: email unsuccessful - Reason: ', sys.exc_info()[0])
        print('Skipping contact:', full_name)
