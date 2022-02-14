from django.urls import reverse
from common.tests.library.page_test import PageTest

class HomePageNotLoggedInTest(PageTest):
    def setUp(self) -> None:
        return super().setUp('/', 'get')

    def assert_link(self, tag_id, url):
        content = f'<a ut-tag-id="{tag_id}" href="{url}"'
        self.assert_contains(content)

    def assert_users_agent_list(self, tag_id):
        url = reverse('users:agent_list')
        self.assert_link(tag_id, url)

    def assert_leads_lead_list(self, tag_id):
        url = reverse('leads:lead_list')
        self.assert_link(tag_id, url)

    def assert_login(self, tag_id):
        url = reverse('login')
        self.assert_link(tag_id, url)

    def assert_register(self, tag_id):
        url = reverse('register')
        self.assert_link(tag_id, url)

    def test_hero_agents_link_exists(self) -> None:
        self.assert_users_agent_list('hero_agents_link')
    
    def test_hero_i_need_agents_link_exists(self) -> None:
        self.assert_leads_lead_list('hero_leads_link')

    def test_nav_bar_desktop_agents_link_exists(self) -> None:
        self.assert_users_agent_list('nav_bar_desktop_agents_link')

    def test_nav_bar_desktop_i_need_agents_link_exists(self) -> None:
        self.assert_leads_lead_list('nav_bar_desktop_leads_link')

    def test_nav_bar_desktop_register_link_exists(self) -> None:
        self.assert_register('nav_bar_desktop_register_link')

    def test_nav_bar_desktop_login_link_exists(self) -> None:
        self.assert_login('nav_bar_desktop_login_link')

    def test_nav_bar_mobile_agents_link_exists(self) -> None:
        self.assert_users_agent_list('nav_bar_mobile_agents_link')

    def test_nav_bar_mobile_i_need_agents_link_exists(self) -> None:
        self.assert_leads_lead_list('nav_bar_mobile_i_need_agents_link')

    def test_nav_bar_mobile_register_link_exists(self) -> None:
        self.assert_register('nav_bar_mobile_register_link')

    def test_nav_bar_mobile_login_link_exists(self) -> None:
        self.assert_login('nav_bar_mobile_login_link')

# class HomePageLoggedInTest(TestCase):
#     def setUp(self) -> None:
#         c = Client()
#         self.response = c.get('/')
#         return super().setUp()

#     def test_hero_agents_link_exists(self) -> None:
#         pass

#     def test_hero_i_need_agents_link_exists(self) -> None:
#         pass

#     def test_nav_bar_desktop_agents(self) -> None:
#         pass

#     def test_nav_bar_desktop_i_need_agents(self) -> None:
#         pass

#     def test_nav_bar_desktop_register(self) -> None:
#         pass

#     def test_nav_bar_desktop_login(self) -> None:
#         pass

#     def test_nav_bar_mobile_agents(self) -> None:
#         pass

#     def test_nav_bar_mobile_i_need_agents(self) -> None:
#         pass

#     def test_nav_bar_mobile_register(self) -> None:
#         pass

#     def test_nav_bar_mobile_login(self) -> None:
#         pass