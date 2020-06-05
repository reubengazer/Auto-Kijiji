import os
import json
import sys
import time
import platform
import yaml
import numpy as np

# Custom class for an advertisement (Ad)
from auto_kijiji.ad import Ad
# selenium imports
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# TODO: Use manual login if user doesn't want to use browser profile / saved logins
# TODO: gather map of category_id codes and category names for Kijiji so users don't have to manually do it
# TODO: Change all time.sleep() commands to explicit waits (with conditions) in Selenium
# TODO: Make Selenium begin faster!

class AutoKijiji:

    def __init__(self, ads: list, config=None, browser='firefox', in_background=False, dont_delete=False):
        """
        Auto-Kijiji: automatically post and re-post Kijiji ads to stay at the top of the listings.

        After some time, your Kijiji ad is no longer "recent enough" in your posting category
        to lie on the front page. Whenever I sell items on Kijiji, I want my ads on
        the front page FOR FREE without paying the Kijiji promotionals to "keep it at the top".
        To do this, you simply have to delete your ad, and re-post it. This is what Auto-Kijiji does!
        You may run this through the command-line manually (as a bash command) on a schedule.

        :param config: path to config.yaml (default: install folder / config.yaml) file which holds the path to the browser driver
        :param ads: list of absolute paths to ad folder(s)
        :param browser: the browser you'd like to use to launch AutoKijiji - ['firefox', 'chrome]
        :param in_background: whether to run this in the background (if not, will open and control browser in real-time)
        :param dont_delete: dont delete the ad if it's already valid before (re)posting
            - you may want to keep this True, as posting duplicate Kijiji ads CAN get you banned in some circumstances.
        """
        # Load configuration file.
        with open(config) as f:
            data = yaml.load(f)

        self.browser=browser
        self.browser_profile_path = self.get_browser_profile()
        self.browser_driver_path = data['browser_driver_path']  # see README.md for download links to drivers
        # Check if the config.yaml file has been updated from the default:
        if self.browser_profile_path == '/path/to/your/browser/driver':
            print("config.yaml file does not have the path to the browser driver.")
            print("Go edit your config.yaml file (default saved to: ~.auto_kijiji/config.yaml")
        self.driver = self.start_driver(in_background=in_background)
        self.post_ad_url = data['kijiji_post_ad_url']
        self.my_ads_url = data['kijiji_my_ads_url']
        self.ad_dirs = [os.path.abspath(dir) for dir in ads]
        self.dont_delete = dont_delete
        self.ads = self.create_ads()
        self.phone = data['phone_number']

        if not self.dont_delete:
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
                profile_path = os.path.join('/home/',
                                            f'{os.getlogin()}',
                                            '.mozilla/firefox/')
            elif plat=='Darwin':
                profile_path = os.path.join('/Users/',
                                            f'{os.getlogin()}',
                                            '/Library/Application Support/Firefox/Profiles/')
            elif plat=='Windows':
                profile_path = os.path.join('\\Users\\',
                                            f'{os.getlogin()}',
                                            '\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\')
        elif self.browser=='chrome':

            if plat=='Linux':
                profile_path = os.path.join('/home/',
                                            f'{os.getlogin()}',
                                            '/.config/google-chrome/default')
            elif plat=='Darwin':
                profile_path = os.path.join('Users/',
                                            f'{os.getlogin()}',
                                            '/Library/Application Support/Google/Chrome/Default')
            elif plat=='Windows':
                profile_path = os.path.join('C:\\Users\\',
                                            f'{os.getlogin()}',
                                            '\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
        else:
            print("Browser argument not recognized. Must be one of: ['firefox', 'chrome'].")
            sys.exit()
        # Return absolute path to this .default file.
        browser_profile_path = os.path.join(profile_path, [f for f in os.listdir(profile_path) if f.endswith('.default')][0])
        return browser_profile_path

    def start_driver(self, in_background=False, implicit_wait_time=4):
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

    def sleep_randomly(self, low=1, high=8):
        """Make the driver wait a random number of seconds between low and high.
        A simple layer to potentially avoid being caught as a bot."""
        time.sleep(np.random.randint(low, high))

    def fill_title(self, title: str):
        """Submit title of ad.
        Since this is the first part of form-filling, we perform an explicit Wait for this element to appear.
        """
        title_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "postad-title"))
        )
        title_box.click()
        title_box.send_keys(title)

    def fill_description(self, description: str):
        """Submit the description of the ad."""
        description_id = 'pstad-descrptn'
        description_box = self.driver.find_element_by_id(description_id)
        description_box.click()
        description_box.send_keys(description)

    def fill_tags(self, tags: list):
        """Submit tags of ad."""
        tag_id = 'pstad-tagsInput'
        tag_box = self.driver.find_element_by_id(tag_id)
        enter_button_class = 'addButton-1154397290'
        enter_button = self.driver.find_element_by_class_name(enter_button_class)
        for tag in tags:
            tag_box.send_keys(tag)
            enter_button.click()

    def fill_photos(self, image_fps: list):
        """Upload the photos of the ad."""
        for image_fp in image_fps:
            self.driver.find_element_by_xpath("//input[@type='file']").send_keys(image_fp)
        # Since it takes a bit for the photos to upload, sleep for a few seconds.
        # TODO: Should create explicit wait condition in Selenium
        time.sleep(20)

    def fill_price(self, price: str):
        """Submit price of the ad."""
        price_id = 'PriceAmount'
        price_box = self.driver.find_element_by_id(price_id)
        price_box.click()
        price_box.send_keys(price)

    def fill_phone(self, phone: str):
        """Submit phone number for the ad."""
        phone_id = 'PhoneNumber'
        phone_box = self.driver.find_element_by_id(phone_id)
        phone_box.click()
        phone_box.send_keys(phone)

    def submit(self):
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
        self.submit()
        self.sleep_randomly()

