from playwright.sync_api import Page, expect
from utils.config import get_app_url

#important concepts#

def test_ui_validations(page: Page, practice_credentials):
    page.goto(get_app_url("/loginpagePractise/"))
    page.get_by_label('Username:').fill(practice_credentials["username"])
    page.get_by_label('Password:').fill(practice_credentials["password"])
    page.get_by_role('combobox').select_option('teach')
    page.locator("#terms").check()
    page.get_by_role('button', name='Sign In').click()   #getbyrole has 2 parameters that it will take
    page.locator("#login").click()

    iphonecard = page.locator('app-card').filter(has_text='iphone X')
    iphonecard.get_by_role('button').click()
    nokiacard = page.locator('app-card').filter(has_text='Nokia Edge')  #locator has filter() option externally
    nokiacard.get_by_role('button').click()
    page.get_by_text('Checkout').click()   #getbytext has partial text on the page as well
    expect(page.locator(".media-body")).to_have_count(2)  #using dot for CSS selectors

def test_child_window(page: Page):
    page.goto(get_app_url("/loginpagePractise/"))

    #closure
    with page.expect_popup() as newPageInfo:
        #step1..2..
        page.locator(".blinkingText").get_by_text("Free Access").click()  # use selectorhub plugin to check CSS selectors
        childPage = newPageInfo.value    #newpageInfo object gets invoked here
        text = childPage.locator(".red").text_content() or ""
        email = text.split("at", 1)[1].strip().split(" ", 1)[0]
        assert email == 'mentor@rahulshettyacademy.com'



        #text - Please email us at mentor@rahulshettyacademy.com with below template to receive response
