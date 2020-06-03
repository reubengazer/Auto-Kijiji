# Auto-Kijiji 1.0.1

### Automatically post and re-post Kijiji ads to remain on the front page
![kijijilogo](autokijiji.jpg)

**To successfully sell items or services on Kijiji, keep your posts on the front page as often as possible!**  
  
Though there are paid options for keeping ads at the top, I wanted a method of doing so that was both free and easy.

Enter **_autokijiji_** - a command-line tool (or stand-alone Python program) to post and re-post your Kijiji ads.

**The main function of AutoKijiji is not simply to _post_ ads but to _repost_ ads.**

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
**Dependencies: selenium, python-dotenv, pathlib**  
Run `pip install selenium python-dotenv pathlib` to manually install all the dependencies

## Configure

### .env file + Browser Driver Path (Firefox, Chrome)  

You need 1 .env file, which contains at least 1 item - the path to your BROWSER DRIVER.  

Find your driver:
- for **Mozilla** you can [download the driver here](https://github.com/mozilla/geckodriver/releases) 
- for **Chrome** you can [download the driver here](https://chromedriver.chromium.org/downloads) 

If this .env file *is not* in your local directory it must be passed as a command-line argument (--env_path) after *autokijiji* like:

```
autokijiji --env_path /path/to/my/.env
```
  
Currently Auto-Kijiji supports **Mozilla Firefox** and **Google Chrome** browsers. 
   
**Note**: You may ALSO include a phone_number (str) in the .env file (an optional input to a Kijiji ad).

An example .env file might look like this:

```
# .env file for Auto-Kijiji
browser_driver_path='/path/to/my/driver'
phone_number='9056162285'
```

## Logging In to Kijiji
Auto-Kijiji assumes you are already logged in via your browser, and grabs your browser profile to login to your Kijiji account. 
Auto-Kijiji currently does not perform any auth-like procedures but for checking your User's browser profile (.default file).

## Your Ads
For Auto-Kijiji to work properly, you need to create 1 directory per advertisement on Kijiji. 
Each ad is a .json dictionary and looks something like this:  

```
{
  "category_id":"656",
  "title": "A cool pair of hiking boots!",
  "price": "100",
  "description": "A pair of boots that has been worn once. \nGreat grip on the bottom and waterproof.",
  "tags": ["hiking boots", "camping equipment", "camping attire", "hiking equipment"],
  "image_fps": ["mybootphoto.JPG"]
}
```
Drop this file into a folder, along with any images you'd like to upload (.jpg, .jpeg, .JPG, .png).  
Then, stick this "ad folder" inside of a directory (your /ad_files/ or /ads/ folder) - it is this directory you will submit as a command line argument to *autokijiji*.  

As an example, the directory you point *autokijiji* to could contain two items: a tent, and a campstove:
```
/ad_files/
    /tent/
        tent.json
        tent_from_side.jpg
        tent_from_front.jpg
    /campstove/
        campstove.json
        campstove_pic.png
        campstove_top.jpg
        rust_spot.png
```       
Inside /ad_files/ are two directories - each with 1 .json and some number of images.

## Try it out
Assuming you have your ads as listed above in a local directory called */ad_files/*, as well as a local .env with the path to my browser driver,  

```
autokijiji --ads_dir ./ad_files --env_path ./.env 
```