#!/usr/bin/python3
__author__ = "u/wontfixit"
__copyright__ = "Copyright 2020"
__license__ = "GPL"
__version__ = "1.0.0"

import praw
import os
import re
import ast
from datetime import datetime
import configparser
import logging as log
from DBhelper import *
from messages import *
import time
import argparse

now = datetime.now()
timestamp = datetime.timestamp(now)
timeMinusOneDay = timestamp-(24*60*60)

LOG_FILENAME = "./log_main.log"


___debug___ = True
___runprod___= True

if ___debug___ == True:
		log.basicConfig( handlers=[
            log.FileHandler(LOG_FILENAME),
            log.StreamHandler()],level=log.INFO,format='%(asctime)s ; %(levelname)s ; %(funcName)s() ; %(message)s')



class manage_deleted_users:
	
	def __init__(self):
		self.subredditname = 'mysteryobject'
		_UA = 'MOB by /u/[yourouija]'
		try:
			reddit = praw.Reddit("bot1",user_agent=_UA)
			reddit.validate_on_submit=True	
			self.r = reddit
		except Exception as err:
			log.error("Exception {}".format(str(err)))
			self.rebootClass(err)
				
		self.flair_solved = "882c5aa6-c926-11ea-a888-0e38155ddc41"
		self.flair_running = "7ae507b2-c926-11ea-8bf8-0ef44622e4b7"
		self.flair_onhold = "4aecca10-c99c-11ea-bc5c-0e190f721893"
		
		log.info("Starting the Bot Class, omg i'm nervous! Starting in sub r/{}".format(self.subredditname))	
		None
	
	
	def streamAll(self):
	
		start_time = time.time()
		start_time = start_time-300
		log.info("Getting Posts not older than {}".format(str(time.ctime(start_time))))
		
		
		submission_stream = self.r.subreddit(self.subredditname).stream.submissions(pause_after=-1)
		while True:
			try:
								for submission in submission_stream:
					if submission is None:
						break
					if submission.created_utc < start_time:
						continue
					#regex for only do some action when picture submission is detected, i bet there is some better methode	
					regex = r"https:\/\/i\.redd\.it|https:\/\/i\.imgur\.com|https:\/\/v\.redd\.it|https:\/\/imgur\.com"
					if re.search(regex, submission.url, re.MULTILINE):
						log.info("IMAGE found")	
						
						if ___runprod___ == True:
							#here we monitor for new submissions
							self.getDatabase(db.addNewGame(submission))	
							#self.initialComment(submission.id)
							self.updateUserFlair(submission.author.name)
						else:
							log.info("RUN only in DEMO mode, no changes were made at the submission.")
							
					else:
						log.info("no Image found")
					
					prettytime = datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')	
					log.info("Submission detected: {},{},{},{},{}".format(prettytime,submission.author.name,submission.title,submission.link_flair_text,submission.url))

			except Exception as err:
				log.error("Exception {} ".format(str(err)))
				self.rebootClass(err)
	

	
	def rebootClass(self,err):
		log.error("FATAL, restart class {}".format(str(err)))	
		os.system("python main.py")	
	
	
	
if __name__ == "__main__":			
	
	ap = argparse.ArgumentParser(description="Post the submission ID")
	ap.add_argument("-s" ,dest='SubmissionID',type=str, required=False,
		help="Submission ID only xxx.py -s h4No0B")
	argument = ap.parse_args()

	if argument.SubmissionID != None:
		log.info("Single Submission processed SID:{}".format(argument.SubmissionID))
		singleobj = MO()
		db = DBhelper()
		singleobj.getDatabase(db)
		singleobj.runSingleSubmission(argument.SubmissionID)
		exit()
	elif argument.SubmissionID == None:
		log.info("Class started regular ")
		obj = MO()
		db = DBhelper()
		obj.getDatabase(db)
		obj.streamAll()
		log.info("no arg {}".format(argument.SubmissionID))
		None













