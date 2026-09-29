from playwright.sync_api import Page, expect, Playwright
from utils.config import get_app_url


def test_playwright_basics(playwright):
   browser = playwright.chromium.launch(headless=True)
   context= browser.new_context()
   page=context.new_page()
   page.goto(get_app_url("/"))
   context.close()
   browser.close()

#page - itself is a fixture ,that suits only for chromium & edge engine headless=true mode, 1 single context only
def test_playwright_short(page: Page):
   page.goto(get_app_url("/"))
   #configured --headed in run configurations

def test_playwright_core_locators(page: Page, practice_credentials):
   page.goto(get_app_url("/loginpagePractise/"))
   page.get_by_label('Username:').fill(practice_credentials["username"])
   page.get_by_label('Password:').fill(practice_credentials["password"])
   page.get_by_role('combobox').select_option('teach')
   page.locator("#terms").check()  # CSS selectors using id #terms or .tagname, checking the checkbox
   page.get_by_role('button', name='Sign In').click()   #click signIn button
   expect(page.get_by_role('heading', name='Shop Name')).to_be_visible()


   # also page.get_by_role('link', name='terms and conditions' ).click()
   #page.pause() - to open playwright and see how it works
   #1. expect(page).to_have_url('https://rahulshettyacademy.com/angularpractice/shop')
   # verify login success
   # 🔹 OR Option 2
   #expect(page.get_by_text('Incorrect username/password.')).to_be_visible()    #wrong password check - negative test case
   #verify if dashboard is visible with correct credentials
   #auto wait mechanism for specific locators by playwright
   #time.sleep(3) - not needed as we have assertion here expect()

   #modify for firefox instance as well by creating a function
def test_playwright_firefox_browser(
    playwright: Playwright,
    practice_credentials,
):
   firefoxbrowser = playwright.firefox.launch(headless=True)
   page = firefoxbrowser.new_page()
   page.goto(get_app_url("/loginpagePractise/"))
   page.get_by_label('Username:').fill(practice_credentials["username"])
   page.get_by_label('Password:').fill(practice_credentials["password"])
   page.get_by_role('combobox').select_option('teach')
   page.locator("#terms").check()  # CSS selectors using id #terms or .tagname, checking the checkbox
   page.get_by_role('button', name='Sign In').click()  # click signIn button
   expect(page.get_by_role('heading', name='Shop Name')).to_be_visible()
   firefoxbrowser.close()
