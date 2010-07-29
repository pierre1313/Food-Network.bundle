import re, urllib
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

WEB_ROOT = 'http://www.foodnetwork.com'
VID_PAGE = 'http://www.foodnetwork.com/video-library/index.html'

CACHE_INTERVAL = 3600 * 6

####################################################################################################
def Start():
  Plugin.AddPrefixHandler("/video/foodNetwork", MainMenu, 'Food Network', 'icon-default.png', 'art-default.png')
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  MediaContainer.title1 = 'Food Network'
  MediaContainer.content = 'Items'
  MediaContainer.art = R('art-default.png')
  HTTP.SetCacheTime(CACHE_INTERVAL)

####################################################################################################
def MainMenu():
  dir = MediaContainer()
  dhold = {}
  page = XML.ElementFromURL(VID_PAGE, cacheTime=1200, isHTML=True)
  for tag in page.xpath("//div[@id='vid-channels']/ul/li"):
    title = tag.xpath("./h4")[0].text.strip().replace("Full Episodes", "").replace('"','')
    channel_id = tag.xpath("./div")[0].get('id')
    dhold[title] = Function(DirectoryItem(ShowBrowse, title=title, icon="icon-default.png"), channel_id=channel_id, title=title)
    

  kl = dhold.keys()[:]
  kl.sort()
  for i in kl:
    dir.Append(dhold[i])
  
  return dir  

####################################################################################################
def ShowBrowse(sender, channel_id, title = None):
    page = XML.ElementFromURL(VID_PAGE, cacheTime=1200, isHTML=True)

    dir = MediaContainer(title2=title)
    for tag in page.xpath("//div[@id='"+channel_id+"']//a[@class='frame']"):
		thumb = tag.xpath("./img")[0].get('src')
		root = tag.xpath("./..//a")[1]
		title = root.text.strip()
		url = root.get('href')
		try:
			duration = root.xpath("../span")[0].text
		except:
			duration = None
		if duration:
			duration = GetDurationFromDesc(duration)			
		dir.Append(WebVideoItem(WEB_ROOT+url, title, thumb=thumb, duration=duration))
	
    
    return dir
 
####################################################################################################
def GetDurationFromDesc(desc):
  duration = ""

  try:
    descArray =  desc.split("(")
    descArrayLen =  len (descArray)
    if descArrayLen<2:
      return ""

    time = descArray[descArrayLen - 1]
    timeArray = time.split(":")

    timeArrayLen = len(timeArray)

    if timeArrayLen<2:
      return ""

    minutes = int(timeArray[0])
    seconds = int(timeArray[1].split(")")[0])
    duration = str(((minutes*60) + seconds)*1000)
    
  except:
    # There was a problem getting the duration (maybe it isn't on the description any more?) so quit with a null
    return ""

  return duration