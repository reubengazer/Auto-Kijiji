# Auto-Kijiji 1.0.1

### Automatically post and re-post Kijiji ads to remain on the front page
![kijijilogo](autokijiji.jpg)

**To successfully sell items or services on Kijiji, keep your posts on the front page as often as possible!**  
  
Though there are paid options for keeping ads at the top, I wanted a method of doing so that was both free and easy.

Enter **_autokijiji_** - a command-line tool (or stand-alone Python program) to post and re-post your Kijiji ads.

> **The main function of _autokijiji_ is not simply to _post_ ads but to _repost_ ads.**

By _deleting_ a current ad and _reposting it_, it will turn up near the front of the listing.

**_autokijiji_** can be executed on a timer (eg. cron) to re-post your ads daily or weekly.  

This is a personal project to moderate my buying-and-reselling-of-camping-equipment, and has been successful thus far!

- Reuben S. Gazer (2020)

## Install
### Manually

```bash
git clone https://github.com/reubengazer/Auto-Kijiji.git
cd Auto-Kijiji
python3 setup.py install
```

Then, setup your config.yaml file (more on this below):

```bash
autokijiji --init
```

**Dependencies: selenium, python-dotenv, pathlib, numpy**  
Run `pip install selenium python-dotenv pathlib numpy` to manually install all the dependencies

## Configure

### config.yaml

*autokijiji* needs to point to a config.yaml file which contains:

- base kijiji urls for posting ads and viewing your active ads (included by default)
- the path to your browser driver
- [optional] your phone number (optional to post with ad, your Kijiji profile doesn't save the phone-number)
- [optional] your preferred browser in which to deploy auto_kijiji

To download the driver for your browser:

- for **Mozilla** you can [download the driver here](https://github.com/mozilla/geckodriver/releases) 
- for **Chrome** you can [download the driver here](https://chromedriver.chromium.org/downloads) 

**Easiest way to define config.yaml**: simply run autokijiji with --init:

```bash
autokijiji --init
```

It will by default save a _config.yaml_ file in the install directory.  

You may edit this file at any time :

```bash
autokijiji --update_config
```

Optionally, you may create your own config anywhere and pass it in as an argument (--config) on the fly:

```bash
autokijiji --config myconfig.yaml --ads ./some-item-to-sell
```

The config.yaml file looks like this:

```yaml
kijiji_post_ad_url : https://www.kijiji.ca/p-admarkt-post-ad.html?
kijiji_my_ads_url : https://www.kijiji.ca/m-my-ads/active
phone_number : 1234567890
preferred_browser : firefox
browser_driver_path : /path/to/your/browser/driver
```
Currently supported browsers are 'firefox' and 'chrome'.

## Example: Let's Sell Some Hiking Boots!

### Logging In to Kijiji
Auto-Kijiji assumes you are already logged in via your browser, and grabs your browser profile to login to your Kijiji account.   
Auto-Kijiji currently does not perform any auth-like procedures but for checking your User's browser profile (.default file).

### Storing Your Ad Content
For Auto-Kijiji to work properly, each ad must be represented by a DIRECTORY.
Each of these directories (ads) must contain 1 .json file containing your ad information and any number of images, like this:  

```bash
# Example directory of some boots I'm selling
/scarpa_hiking_boots/
    hikingboots.json
    mybootphoto.JPG
```  

Your ad content is contained in the .json file and must look like this:

```json
{
  "category_id":"286",
  "title": "A cool pair of hiking boots!",
  "price": "100",
  "description": "A pair of boots that has been worn once. \nGreat grip on the bottom and waterproof.",
  "tags": ["hiking boots", "camping equipment", "camping attire", "hiking equipment"],
  "image_fps": ["mybootphoto.JPG"]
}
```

Image types currently supported are .jpg/.jpeg/.JPG and .png.  

## Try it out
Assuming you've set the config.yaml file (if not, see above) let's post the example ad contained in the repo (hiking boots):  

```bash
autokijiji --ads ./example_ad_hiking_boots 
```

This will open up a browser in real-time in front of you.  

Let's run it in the background:

```bash
autokijiji --ads ./example_ad_hiking_boots --background
```

**Uploading Multiple Ads**: Simply pass in multiple arguments for --ad_dirs:

```bash
autokijiji --ads ./example_ad_hiking_boots ./vintage_campstove ./fishing_rods
```

## Command-Line Arguments

--init -> initialize config.yaml  
--ads -> directory or directories of your ads to post  
--delete_first -> whether to delete your ad before re-posting it (default: True)  
--browser -> the browser you'd like to deploy ('firefox' or 'chrome')  
--background -> whether to run this in the background (default: True)  
--config -> manually submit a config.yaml file that isn't setup from --init  
--version, -v -> print your current version of *auto_kijiji*  