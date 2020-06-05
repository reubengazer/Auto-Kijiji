from auto_kijiji.auto_kijiji import AutoKijiji
import os
import argparse
from . import VERSION

def parse_args():
    parser = argparse.ArgumentParser(description="""Auto-Kijiji: Automatically post and re-post Kijiji ads to keep them at the top of the listings for free.""")
    parser.add_argument('--init', action='store_true', help="""Create config.yaml file if doesn't exist and open with default text editor.""")
    parser.add_argument('--update_config', action='store_true', help="""Update your config.yaml file found in the install directory.""")
    parser.add_argument('--ads', metavar='Ads directory or directories', action='append', nargs='+', help="""The directory/directories of your ads (an ad: 1 directory with a .json file representing the ad content, and any images (.png, .jpg/.jpeg/.JPG)""")
    parser.add_argument('--dont_delete', action='store_true', help="""Whether to delete the ads first before re-posting (default True).""")
    parser.add_argument('--browser', default='firefox', metavar='Browser', help="""The browser through which to post. Options are 'firefox' or 'chrome'.""")
    parser.add_argument('--background', action='store_true', help="""Whether to run the script in the background or not (if not, will open browser in front of you while posting).""")
    parser.add_argument('--config', metavar='Config file (yaml)', help="""The script must point to a config.yaml file which contains the path to the browser driver.""")
    parser.add_argument('--version', '-v', metavar='Version', help="Version of Auto-Kijiji.")
    args = parser.parse_args()
    return(args)

def main():
    # Get directory to where the ad folders reside (usually called /ad_files/ or /ads/)
    print("Welcome to Auto-Kijiji!")
    args = parse_args()

    # Version
    if args.version:
        print("Version:\t\t%s" %VERSION)
        exit(0)

    # Init - to define .auto_kijiji/config.yaml file
    if args.init:
        init()
        exit(0)

    # Upgrade config
    if args.update_config:
        update_config()
        exit(0)

    # Handle custom config file passed as argument
    # If one isn't passed, find the config file in the install directory
    if args.config:
        config_filepath = args.config
    else:
        # Retrieve the default config file in the install directory
        install_path = os.path.abspath(__file__)
        config_filepath = os.path.join(os.path.dirname(install_path), 'config.yaml')
        if not os.path.exists(config_filepath):
            config_filepath = None
    if config_filepath:
        print("Config file: %s" % config_filepath)
    else:
        print("No config file loaded - run the following command to instantiate one (change /path/to/browser/driver):")
        print(" >> autokijiji --init ")

    # Instantiate the AutoKijiji object.
    ak = AutoKijiji(
                    ads=args.ads[0],
                    config=config_filepath,
                    browser=args.browser,
                    in_background=args.background,
                    dont_delete=args.dont_delete
                    )


    # Post each of the ads.
    for ad in ak.ads:

        print(f"\nPosting ad: {ad.title}")
        ak.post_ad(ad)
        print("Successfully posted.")

    print(f"\nCompleted posting {len(ak.ads)} advertisement(s) with Auto-Kijiji.")
    print("Thanks for running Auto-Kijiji!")

    # Close the driver and the program.
    ak.driver.close()
    exit(0)

def init():
    default_config="""
# Kijiji base urls

# The url to begin posting an ad
kijiji_post_ad_url : https://www.kijiji.ca/p-admarkt-post-ad.html?
# The url to view your active ads (for --delete_first)
kijiji_my_ads_url : https://www.kijiji.ca/m-my-ads/active

# User phone_number (optional when posting ad).
phone_number : 1234567890

# Set preferred browser.
# Currently supported browser options: [firefox, chrome]
preferred_browser : firefox

# Browser driver filepath
# Find it here for Mozilla Firefox: https://github.com/mozilla/geckodriver/releases
# Find it here for Google Chrome: https://chromedriver.chromium.org/downloads
browser_driver_path : /path/to/your/browser/driver
"""
    # Create config.yaml file in the install directory
    install_path = os.path.abspath(__file__)
    config_path = os.path.join(os.path.dirname(install_path), 'config.yaml')
    # Check if it already exists
    if os.path.exists(config_path):
        print("Configuration file already initiated.")
        print("To update, do: >> autokijiji --update_config")
        exit(0)
    else:
        with open(config_path, 'w') as f:
            f.write(default_config)
        print("New config.yaml file created: %s" % (os.path.join(os.path.dirname(install_path), 'config.yaml')))

    # Open with editor
    if os.name == 'nt':
        os.system(config_path)
    elif 'EDITOR' in os.environ:
        os.system('%s %s' % (os.getenv('EDITOR'), config_path))
    elif os.system("which gedit") is not None:
        os.system('gedit %s' % config_path)
    elif os.system("which nano") is not None:
        os.system('nano %s' % config_path)
    elif os.system("which vim") is not None:
        os.system('vim %s' % config_path)

def update_config():
    """Upgrade the config.yaml file found in the install directory."""
    install_path = os.path.abspath(__file__)
    config_path = os.path.join(os.path.dirname(install_path), 'config.yaml')
    # Check if it already exists
    if os.path.exists(config_path):
        # Open with editor
        if os.name == 'nt':
            os.system(config_path)
        elif 'EDITOR' in os.environ:
            os.system('%s %s' % (os.getenv('EDITOR'), config_path))
        elif os.system("which gedit") is not None:
            os.system('gedit %s' % config_path)
        elif os.system("which nano") is not None:
            os.system('nano %s' % config_path)
        elif os.system("which vim") is not None:
            os.system('vim %s' % config_path)
    else:
        print("Need to run:\n\n>> autokijiji --init\n\nbefore --update_config")