import json
from datetime import datetime
import os
import boto3
from craigslist import CraigslistHousing

def lambda_handler(event, context):

	# Pull in environmental variable for number of posts to pull
	number_of_posts = os.environ.get("number_of_posts")

	# Instantiate our Craigslist scraper
	cl = CraigslistHousing(site='newyork', 
							area=None, 
							category='aap')

	# Pull data from Craigslist and put into a list
	results = cl.get_results(sort_by='newest', geotagged=True, limit=5)
	resultsList = [result for result in results]
	
	# Convert data to json
	data = json.dumps(resultsList)

	# Get the current datetime for the file name
	now = str(datetime.today())
	
	# Export the data to S3
	client = boto3.client('s3')
	response = client.put_object(Bucket='lazyapartment', 
					Body=data, 
					Key='rawdata/{}.json'.format(now))