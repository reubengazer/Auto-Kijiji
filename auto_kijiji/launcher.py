from auto_kijiji.auto_kijiji import AutoKijiji
import sys
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="""Auto-Kijiji: Automatically post and re-post Kijiji ads to keep them at the top of the listings for free.""")
    #parser.add_argument('--init','--setup', help="Create .env file if doesn't exist and open with default text editor", action='store_true')
    parser.add_argument('--ads_dir', default='./ad_files', metavar='Ads directory',help="""The directory in which your ads lie. Inside this dir, each ad is ITS OWN DIR with 1 .json file representing the ad content, and any images (.png, .jpg/.jpeg/.JPG)""")
    parser.add_argument('--delete_first', action='store_false', help="""Whether to delete the ads first before re-posting (default True).""")
    parser.add_argument('--browser', default='firefox', metavar='Browser', help="""The browser through which to post. Options are 'firefox' or 'chrome'.""")
    parser.add_argument('--in_background', action='store_true', help="""Whether to run the script in the background or not (if not, will open browser in front of you while posting).""")
    parser.add_argument('--env_path', '-e', default='./.env', metavar='Environment file', help="""The script must read a .env file with the path to the browser driver.""")
    args = parser.parse_args()
    return(args)

def main():
    # Get directory to where the ad folders reside (usually called /ad_files/ or /ads/)
    args = parse_args()

    if args.ads_dir:
        ads_dir = args.ads_dir
    else:
        if os.path.exists('./ad_files/'):
            ads_dir = './ad_files/'
        elif os.path.exists('./ads/'):
            ads_dir = './ads/'
        else:
            print("Need to provide --ads_dir argument to tell Auto-Kijiji where to look for your ads.")
            print("Each ad is its OWN DIR inside, containing 1 .json file and any images you'd like to upload.")
            sys.exit()

    ak = AutoKijiji(
                    ads_dir=ads_dir,
                    env_path=args.env_path,
                    browser=args.browser,
                    delete_first=args.delete_first,
                    in_background=args.in_background
                    )

    # Post each of the ads.
    for ad in ak.ads:
        print(f"\nPosting ad: {ad.title}")
        ak.post_ad(ad)
        print("Successfully posted.")
    print(f"Completed printing {len(ak.ads)}")

    # Close the driver and the program.
    ak.driver.close()
    sys.exit()