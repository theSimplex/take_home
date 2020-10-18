from page_objects.page_objects import LoginPage, Search


def test_login():
    LoginPage().login()
    result = Search().search('Fetch Rewards').open()
    assert result.current_url == 'https://www.facebook.com/FetchRewards' #Verify that we're at the correct page.
    result.find_element_by_link_text('Like')
    assert result.ind_element_by_link_text('Liked') #Assertion that text on the button will change, otherwise test would fail.