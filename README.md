# Auto-Kijiji 1.0.1

### Automatically post and re-post Kijiji ads to remain near on the front page
![kijijilogo](autokijiji.jpg)

**To successfully sell items or services on Kijiji, it is recommended to keep your posts on the front page as often as possible.**  
  
Though there are paid options for keeping ads near the top/front, I wanted a method of keeping my posts near the top that was both free and hassle-free.

Enter **_autokijiji_** - a command-line tool (or stand-alone Python program) that can be run on a timer (eg. cron) to post and re-post your Kijiji ads.  

**The main function of AutoKijiji is not simply to _post_ ads but to _repost_ ads.**

By _deleting_ a current ad and _reposting it_, it will turn up near the front of the listing.

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

### .env file + Browser Driver Path (Firefox, Chrome)  

You need a .env file either passed as command line argument or in local directory by default.   
   
This needs to contain just 1 line - the path to your BROWSER DRIVER.  
  
Currently Auto-Kijiji supports Mozilla Firefox and Google Chrome browsers.  
   
_Note: You may ALSO include a phone_number (an optional input to a Kijiji ad)._

### Your Ads
For Auto-Kijiji to work properly, you need to create 1 directory per advertisement on Kijiji.  
 
Inside of an "ad folder" you have 1 .json file which outlines the parameters of your advertisement, like:

```{
  "category_id":"656",
  "title": "A cool pair of hiking boots!",
  "price": "100",
  "description": "A pair of boots that has been worn once. \nGreat grip on the bottom and waterproof.",
  "tags": ["hiking boots", "camping equipment", "camping attire", "hiking equipment"],
  "image_fps": ["mybootphoto.JPG"]
}
```
You may put as many images as necessary in the folder as well to upload with the ad (.jpg, .jpeg, .JPG, .png).  
Then, keep each "ad folder" inside of a directory - it is this directory you will submit as a command line argument to *autokijiji*.  

As an example, the directory you point *autokijiji* to could look like this:
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
```    
  
For **Mozilla** you can [download the driver here](https://github.com/mozilla/geckodriver/releases).  
For **Chrome** you can [download the driver here](https://chromedriver.chromium.org/downloads).   

## Try out
`autokijiji --ads_dir ./ad_files --env_path ./.env `