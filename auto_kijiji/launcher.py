from auto_kijiji.auto_kijiji import AutoKijiji
import sys
import argparse

# TODO: Add an init() method like Chase to immediately force user to use nano/vim to create .env file

def parse_args():
    parser = argparse.ArgumentParser(description="""Auto-Kijiji: Automatically post and re-post Kijiji ads to keep them at the top of the listings for free.""")
    #parser.add_argument('--init','--setup', help="Create .env file if doesn't exist and open with default text editor", action='store_true')
    parser.add_argument('--ads', metavar='Ads directory or directories', action='append', nargs='+', help="""The directory/directories of your ads (an ad: 1 directory with a .json file representing the ad content, and any images (.png, .jpg/.jpeg/.JPG)""")
    parser.add_argument('--delete_first', action='store_true', help="""Whether to delete the ads first before re-posting (default True).""")
    parser.add_argument('--browser', default='firefox', metavar='Browser', help="""The browser through which to post. Options are 'firefox' or 'chrome'.""")
    parser.add_argument('--background', action='store_true', help="""Whether to run the script in the background or not (if not, will open browser in front of you while posting).""")
    parser.add_argument('--env', '-e', default='./.env', metavar='Environment file', help="""The script must read a .env file with the path to the browser driver.""")
    args = parser.parse_args()
    return(args)

def main():
    # Get directory to where the ad folders reside (usually called /ad_files/ or /ads/)
    print("Welcome to Auto-Kijiji!")
    args = parse_args()
    ak = AutoKijiji(ads=args.ads[0],
                    env_path=args.env,
                    browser=args.browser,
                    in_background=args.background,
                    delete_first=args.delete_first
                    )

    # Post each of the ads.
    for ad in ak.ads:

        print(f"\nPosting ad: {ad.title}")
        ak.post_ad(ad)
        print("Successfully posted.")

    print(f"\nCompleted posting {len(ak.ads)} advertisements with Auto-Kijiji.")
    print("Thanks for running Auto-Kijiji!")

    # Close the driver and the program.
    ak.driver.close()
    sys.exit()