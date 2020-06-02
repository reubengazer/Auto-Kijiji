# Auto-Kijiji 1.0.1
#### Automatically post and re-post Kijiji ads to have your ads show at top of search listings for free.

To successfully sell items or services on Kijiji, it is recommended to keep your posts on the front page as often as possible.
This is much like Google SEO - ads that are more difficult to find are less successful.

Although there are paid options for keeping ads near the top/front (Kijiji's Top Ad, Highlight Ad, Home Gallery, etc) 
I wanted a method of keeping my posts near the top that was both free and hassle-free.

Enter _AutoKijiji_ - a Python program that can be run on a timer (eg. cron) to upload your Kijiji ads in entirety. 
The main function of AutoKijiji is not simply to _post_ ads but to _repost_ ads.

By _deleting_ a current ad and _reposting it_, it will turn up near the front of the pack. 
Thus, AutoKijiji _deletes_ your ad(s) and immediately reposts them, pushing them to the top of the pile.

This was built as a personal project to moderate my buying-and-reselling-of-camping-equipment side-business, and has been successful thus far!

- Reuben S. Gazer (2020)

## Install
### Manually
   ```bash
   git clone https://github.com/reubengazer/Auto-Kijiji.git
   cd Auto-Kijiji
   python3 setup.py install
   ```
**Dependencies: selenium, python-dotenv, pathlib**  
Run `pip install selenium python-dotenv pathlib` to manually install all the dependencies

## Configure
You need a .env file either passed as command line argument or in local directory by default.  
This needs to contain just 1 line - the path to your BROWSER DRIVER.  
For **Mozilla** you can [download the driver here](https://github.com/mozilla/geckodriver/releases).  
For **Chrome** you can [download the driver here](https://chromedriver.chromium.org/downloads).   

## Try out
`auto_kijiji --ads_dir ./my_ads --env_path ./.env `