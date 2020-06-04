import os
import json
import sys
import time
import platform
# Custom class for an advertisement (Ad)
from auto_kijiji.ad import Ad
# selenium imports
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import FirefoxProfile
# Env
from dotenv import load_dotenv

# TODO: Use manual login if user doesn't want to use browser profile / saved logins
# TODO: Find better way of setting the phone number for the ad
# TODO: make kijiji links stored in a kijiji_base_links file
# TODO: create better way to store path to the browser_driver. Maybe a config step?
# TODO: gather map of category_id codes and category names for Kijiji so users don't have to manually do it
# TODO: Change all time.sleep() commands to explicit waits (with conditions) in Selenium
# TODO: Make Selenium begin faster!
# TODO: code in explicit wait after loading post-ad url to look for the postad-title box! Failed in tests.
# TODO: change the input to be single ad directories instead of a directory OF ad folders

class AutoKijiji:

    def __init__(self, ads: list, env_path='./.env', browser='firefox', in_background=False, delete_first=True):
        """
        Auto-Kijiji: automatically post and re-post Kijiji ads to stay at the top of the listings.

        After some time, your Kijiji ad is no longer "recent enough" in your posting category
        to lie on the front page. Whenever I sell items on Kijiji, I want my ads on
        the front page FOR FREE without paying the Kijiji promotionals to "keep it at the top".
        To do this, you simply have to delete your ad, and re-post it. This is what Auto-Kijiji does!
        You may run this through the command-line manually (as a bash command) on a schedule.

        :param env_path: path to .env file which holds the path to the browser driver
        :param ads: list of absolute paths to ad folder(s)
        :param browser: the browser you'd like to use to launch AutoKijiji - ['firefox', 'chrome]
        :param in_background: whether to run this in the background (if not, will open and control browser in real-time)
        :param delete_if_active: delete the ad if it's already valid before (re)posting
            - you may want to keep this True, as posting duplicate Kijiji ads CAN get you banned in some circumstances.
        """
        # Set environment file.
        load_dotenv(dotenv_path=env_path)
        self.browser=browser
        self.browser_profile_path = self.get_browser_profile()
        self.browser_driver_path = os.getenv("browser_driver_path")  # see README.md for download links to drivers
        self.driver = self.start_driver(in_background=in_background)
        self.post_ad_url = 'https://www.kijiji.ca/p-admarkt-post-ad.html?'
        self.my_ads_url = 'https://www.kijiji.ca/m-my-ads/active'
        self.ad_dirs = [os.path.abspath(dir) for dir in ads]
        self.delete_first = delete_first
        self.ads = self.create_ads()
        self.phone = os.getenv("phone_number")

        if self.delete_first == True:
            self.delete_ads()

    def get_browser_profile(self) -> str:
        """Return the profile (login cookies) of your chosen browser.
        profile_paths returnable for Windows, Mac and Linux automatically.
        :param browser: 'firefox', 'chrome'
        :return: absolute path to your browser profile file (file ending in .default)
        """
        plat = platform.system()  # will return one of: Darwin (Mac), Windows, Linux
        profile_path = None

        if self.browser=='firefox':
            if plat=='Linux':
                profile_path = os.path.join('/home/', f'{os.getlogin()}', '.mozilla/firefox/')
            elif plat=='Darwin':
                profile_path = os.path.join('/Users/', f'{os.getlogin()}', '/Library/Application Support/Firefox/Profiles/')
            elif plat=='Windows':
                profile_path = os.path.join('\\Users\\', f'{os.getlogin()}', '\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\')
        elif self.browser=='chrome':
            if plat=='Linux':
                profile_path = os.path.join('/home/', f'{os.getlogin()}', '.mozilla/firefox/')
            elif plat=='Darwin':
                profile_path = os.path.join('/Users/', f'{os.getlogin()}', '/Library/Application Support/Firefox/Profiles/')
            elif plat=='Windows':
                profile_path = os.path.join('\\Users\\', f'{os.getlogin()}', '\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\')
        else:
            print("Browser argument not recognized. Must be one of: ['firefox', 'chrome'].")
            sys.exit()
        # Return absolute path to this .default file.
        browser_profile_path = os.path.join(profile_path, [f for f in os.listdir(profile_path) if f.endswith('.default')][0])
        return browser_profile_path

    def start_driver(self, in_background=False, implicit_wait_time=3):
        """
        Start the selenium web-driver.
        :return: the selenium web-driver object, from which you will find elements, click things, etc.
        """
        # Suppress actual physical browser opening, put in background.
        options = Options()
        if in_background:
            options.add_argument('--headless')
        if self.browser=='firefox':
            profile = FirefoxProfile(self.browser_profile_path)
            driver = webdriver.Firefox(profile, options=options, executable_path=self.browser_driver_path)
        elif self.browser=='chrome':
            print("Haven't implemented Chrome profiles yet. TODO.")
            #profile = ...
            #driver = webdriver.Chrome()
        else:
            print("Browser argument not recognized. Must be one of: ['firefox', 'chrome'].")
            return None
        driver.implicitly_wait(implicit_wait_time)
        return driver

    def create_ads(self) -> list:
        """Create Ad objects out of the ads inside self.ad_dirs

        Each ad should be a SINGLE FOLDER containing:
            - 1 .json that outlines the actual "meat" of your advertisement (title, description, price, etc)
                - see hikingboots.json.json for what this dictionary should look like
            - any # of .png, .jpg, or .JPG images which will be uploaded as images for the advertisement
        """

        list_of_ads = []

        for ad_dir in self.ad_dirs:
            # Grab .json and create the Ad instance.
            ad_json = [f for f in os.listdir(ad_dir) if f.endswith('.json')]

            if len(ad_json) == 0:
                print("Did not find .json file in 1 or more ad folders.")
                #sys.exit()
            else:
                ad_json = ad_json[0]

            with open(os.path.join(ad_dir, ad_json), 'r') as f:
                ad = Ad(**json.load(f))

                # Add image filepaths as attributes.
                img_fps = [os.path.join(ad_dir, file) for file in os.listdir(os.path.join(ad_dir))
                           if file.endswith('jpg')
                           or file.endswith('jpeg')
                           or file.endswith('JPG')
                           or file.endswith('.png')]
                ad.image_fps = img_fps

                # Append this ad to list of ads.
                list_of_ads.append(ad)
        return list_of_ads

    def go_to_post_page(self, ad):
        """Go directly to the post-ad page."""
        url = self.post_ad_url + f'categoryId={ad.category_id}'
        self.driver.get(url)

    def fill_ad(self, ad):
        """Fill all necessary information on the ad page."""
        self.fill_title(ad.title)
        self.fill_description(ad.description)
        self.fill_tags(ad.tags)
        self.fill_photos(ad.image_fps)
        self.fill_price(ad.price)
        self.fill_phone(self.phone)

    def fill_title(self, title: str):
        """Submit title of ad."""
        title_box = self.driver.find_element_by_id('postad-title')
        title_box.click()
        title_box.send_keys(title)

    def fill_description(self, description: str):
        """Submit the description of the ad."""
        description_box = self.driver.find_element_by_id('pstad-descrptn')
        description_box.click()
        description_box.send_keys(description)

    def fill_tags(self, tags: list):
        """Submit tags of ad."""
        tag_box = self.driver.find_element_by_id('pstad-tagsInput')
        enter_button = self.driver.find_element_by_class_name('addButton-1154397290')
        for tag in tags:
            tag_box.send_keys(tag)
            enter_button.click()

    def fill_photos(self, image_fps: list):
        """Upload the photos of the ad."""
        for image_fp in image_fps:
            self.driver.find_element_by_xpath("//input[@type='file']").send_keys(image_fp)
        # Since it takes a bit for the photos to upload, sleep for a few seconds.
        # TODO: Should create explicit wait condition in Selenium
        time.sleep(30)

    def fill_price(self, price: str):
        """Submit price of the ad."""
        price_box = self.driver.find_element_by_id('PriceAmount')
        price_box.click()
        price_box.send_keys(price)

    def fill_phone(self, phone: str):
        """Submit phone number for the ad."""
        phone_box = self.driver.find_element_by_id('PhoneNumber')
        phone_box.click()
        phone_box.send_keys(phone)

    def submit_ad(self):
        """Click to submit the ad finally."""
        submission_button = self.driver.find_element_by_xpath("//button[@type='submit']")
        submission_button.click()

    def delete_ads(self):
        """Delete the ad from your Kijiji, before re-posting."""
        self.driver.get(self.my_ads_url)
        delete_buttons = self.driver.find_elements_by_xpath("//button[@data-qa-id='adDeleteButton']")
        for delete_button in delete_buttons:
            delete_button.click()
            time.sleep(2)

    def post_ad(self, ad: Ad):
        """Post a single ad on the Kijiji site."""
        self.go_to_post_page(ad)
        self.fill_ad(ad)
        self.submit_ad()
        time.sleep(5)
