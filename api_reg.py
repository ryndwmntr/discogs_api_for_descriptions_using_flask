from flask import Flask, render_template, request

import requests, json

# APP IS NAME OF MAIN #
app = Flask(__name__)

# DISCOGS ACCOUNT TOKEN #

# REGULAR TOKEN #
token = 'THIS IS ACCOUNT TOKEN'

@app.route('/', methods = ['GET', 'POST'])
def index():
	# IF REQUEST FOUND #
	if request.method == 'POST':
		try:
			#CAT ID ALBUM FROM REQUEST #
			cat_id_release = request.form['cat_no']

			# SEARCH INFO BY CAT ID #

			get_info = requests.get(f'https://api.discogs.com/database/search?catno={cat_id_release}&token={token}')

			# GET RELEASE ID FROM INFO #
			get_info_id = get_info.json()
			release_id = get_info_id['results'][0]['id']

			# GET DATA BY RELEASE ID #
			get_datas = requests.get(f'https://api.discogs.com/releases/{release_id}')
			record_datas = get_datas.json()

			# GET RECORD DETAILS #
			record_formats = record_datas['formats'][0]['descriptions']
			record_cat_no = record_datas['labels'][0]['catno']
			record_artist = record_datas['artists'][0]['name']
			record_title = record_datas.get('title')
			record_year = record_datas.get('year')

			record_genres = record_datas['genres']
			record_genre_lists = []
			for genre in record_genres:
				record_genre_lists.append(genre)

			record_country = record_datas.get('country')

			record_label = record_datas['labels'][0]['name']

			record_tracklists = record_datas['tracklist']
			record_tracklist_titles = []
			for track_details in record_tracklists:
				for key, val in track_details.items():
					if key == 'title':
						record_tracklist_titles.append(f'{val}')

			record_short_info = f'{record_artist} - {record_title} - {record_cat_no} ({record_year}) {record_genre_lists} VINYL/LP/PH/PIRINGAN HITAM'

			#PASS SOME DETAILS INTO DICT
			record_details = {'short':record_short_info, 'formats':record_formats, 'cat_no':record_cat_no, 'artist':record_artist, 'title':record_title, 'year':record_year,'genres':record_genre_lists, 'country':record_country, 'label':record_label, 'tracklists':record_tracklist_titles}

			return render_template('index.html', record_details=record_details)

		except:
			# NO RECORD FOUND #
			message = 'Record not Found!'
			return render_template('index.html', message=message)

	# ELSE NO REQUEST FOUND #
	return render_template('index.html')

# IF NAME IS THE MAIN #
if __name__ == "__main__":
	app.run()