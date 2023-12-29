#!/usr/bin/env python
# coding: utf-8

# # SCRAPING SONG DATASET FROM `AZLyrics`
# 
# <img src="https://i.imgur.com/U4BrQEd.png" title="source: imgur.com" />
# 
# This notebook contains our web scraping project for group 1.
# 
# Group members:
# - Gift Abah
# - Ibukunoluwa Moses
# - Abayomi-Perez Okekunle
# - Sophia Emifoniye
# 
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# > ## TASK
# 
# To create a **dataset of songs and albums** that have been created by differnt artists (e.g Sam Smith, Nicki Minaj) by scraping the `AZLyrics` site: https://www.azlyrics.com/f.html
# 
# The Function should be able to take any artist page and return the EPs and/or albums that the artist have released, the release date (year) and some songs on that album.

# 
# ---
# 
# 
# 
# For this dataset, we decided to collect the following information:
# 
# - Name of the Artist
# - EPs or Albums that they have released
# - Year of release
# - Tracks on the album
# - Cover art (to be saved as image link) for the EP or album
# 
# 
# ---
# 
# 

# > **OUTPUT FORMAT:** Our final export will be made into a `CSV file`

# 
# 
# ---
# 
# 

#  ### OUR CODES START HERE
# 
# Here's an outline of the steps we intend to follow:
# 
# 1. Install the necessary libraries
# 2. Use `requests` to download the webpage
# 3. Use `BeautifulSoup` to parse and read the webpage
# 4. Collect the necessary dataset and save it as a list of dictionaries
# 5. Write a simple function that does everything
# 6. Save final result as a CSV file

# 
# 
# ---
# 
# 

# > Step 1: Installing the necessary libraries that are needed - `requests` and `BeautifulSoup`

# In[1]:


get_ipython().system('pip install requests --upgrade --quiet')


# In[2]:


import requests


# In[3]:


get_ipython().system('pip install beautifulsoup4 --upgrade --quiet')


# In[4]:


from bs4 import BeautifulSoup


# > Getting the topic url to be scraped, `https://store.steampowered.com/genre/Free%20to%20Play/`

# In[37]:


topic_url = 'https://www.azlyrics.com/s/samsmith.html'

#  Using requests.get to download the webpage

response = requests.get(topic_url)


# In[38]:


# Checking to ensure that I got the response of "200 family"
response.status_code


# In[39]:


page_content = response.text
len(page_content)


# In[40]:


# Checking to be sure the webpage has been downloaded and is being read correctly
page_content[:1001]


# > Parsing your code into BeautifulSoup using parsers

# In[41]:


doc = BeautifulSoup(response.text, 'html.parser')
# type(doc)


# > **STEP 2:** Getting the `Name of the Artist` from the `h1` tag

# In[42]:


artist_name = doc.h1.text.strip()
artist_name = artist_name.strip(' Lyrics')
artist_name


# 
# 
# ---
# 
# 
# > STEP 3:
# 
# > Using `.find_all` to find all `div` tags that contain the class `album`
# 
# 
# 

# In[43]:


list_of_albums = doc.find_all('div', class_='album')
list_of_albums

#  Trying it out to see if it works
first_item = list_of_albums[0]
first_item.text.strip()


# In[44]:


albums_and_year = []

for album in list_of_albums:
  album = album.text.strip()
  albums_and_year.append(album)


albums_and_year


# In[45]:


# @title **Step 4:** Getting the `Cover Images` of the albums

album_img = doc.find_all('img', class_='album-image')
album_img


# In[46]:


# Getting the Url for the img
img_src = []

for img in album_img:
  base_url = 'https://www.azlyrics.com'
  src = base_url + img['src']
  img_src.append(src)

img_src


# In[28]:


# @title Step 5: Getting the `List of songs` under each album
list_of_songs = doc.find_all('div', class_='listalbum-item')

# Creating a list of all the songs
song_list_and_url = {}

for song in list_of_songs:
    # Using find method to extract song name and link
    song_name = song.find('a').text.strip()
    song_link = base_url + song.find('a')['href']

    # Updating the dictionary
    song_list_and_url.update({song_name: song_link})

song_list_and_url


# 
# 
# ---
# 
# 
# ## Now that we know how to extract the data we want, let's combine all the lines of code above into a `function` called `song_dataset`

# In[47]:


def song_dataset(url):
    # Step 1: Download the webpage
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

    # Step 2: Parse the HTML content
    doc = BeautifulSoup(response.text, 'html.parser')

    # Step 3: Get the artist name
    artist_name = doc.h1.text.strip()
    artist_name = artist_name.strip(' Lyrics')

    # Step 4: Get the list of albums
    list_of_albums = doc.find_all('div', class_='album')
    albums_and_year = [album.text.strip() for album in list_of_albums]

    # Step 5: Get the album images
    album_img = doc.find_all('img', class_='album-image')
    img_src = [base_url+img['src'] for img in album_img]

    # Step 6: Get the list of songs for each album
    list_of_songs = doc.find_all('div', class_='listalbum-item')
    song_list_and_url = {}

    for song in list_of_songs:
        album = song.find_previous('div', class_='album').text.strip()
        song_name = song.find('a').text.strip()
        song_link = url + song.find('a')['href']

        # Update the dictionary with the new structure
        if album not in song_list_and_url:
            song_list_and_url[album] = []
        song_list_and_url[album].append({'song_name': song_name, 'song_link': song_link})

    # Combine all the data into a dictionary
    result = {
        'Artist Name': artist_name,
        'Album Name (Year)': albums_and_year,
        'Cover Image Link': img_src,
        'Song List and Url': song_list_and_url
    }

    return result


# ### Testing out the function
# 
# Example using `Sam Smith`

# In[48]:


# Example for "Sam Smith"
url_to_scrape = 'https://www.azlyrics.com/s/samsmith.html'
result_dataset = song_dataset(url_to_scrape)

# Print the result or further processing
print(result_dataset)


# ### Example 2 -- Scraping the song_dataset for using `Rihanna`

# In[49]:


# Example for "Sam Smith"
url_to_scrape = 'https://www.azlyrics.com/r/rihanna.html'
result_dataset = song_dataset(url_to_scrape)

# Print the result or further processing
print(result_dataset)


# 
# 
# ---
# 
# ## Writing the dataset into a CSV file

# In[50]:


import csv
import os

def write_csv(data, path):
    # Check if the file already exists
    file_exists = os.path.isfile(path)

    with open(path, 'a', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer
        csv_writer = csv.writer(csvfile)

        # If the file doesn't exist, write the header
        if not file_exists:
            csv_writer.writerow(['Artist Name', 'Album Name (Year)', 'Cover Image Link', 'Song Name', 'Link to Song'])

        # Repeat artist_name for each row
        artist_name = data['Artist Name']

        # Iterate through each album
        for album, songs_and_links in data['Song List and Url'].items():
            # Repeat img_src for each row in the same album
            img_src = data['Cover Image Link'][0]

            # Iterate through each song in the album
            for song_info in songs_and_links:
                csv_writer.writerow([artist_name, album, img_src, song_info['song_name'], song_info['song_link']])


# ---
# 
# ### Calling and using the CSV writer function
# 
# The `write_csv` function is coded such that it appends new artists, their albums, song names and links to the end of the previous dataset to create a gigantic dataset.
# 
# An example is shown below using `Sam Smith` and `Rihanna's` page

# In[51]:


# Example usage:
url_to_scrape = 'https://www.azlyrics.com/s/samsmith.html'
result_dataset = song_dataset(url_to_scrape)

# Specifying the path where you want to save the CSV file
csv_path = 'output_dataset.csv'

# Calling the write_csv function to save the dataset to a CSV file
write_csv(result_dataset, csv_path)


# In[52]:


# Example usage:
url_to_scrape = 'https://www.azlyrics.com/r/rihanna.html'
result_dataset = song_dataset(url_to_scrape)

# Specifying the path where you want to save the CSV file
csv_path = 'output_dataset.csv'

# Calling the write_csv function to save the dataset to a CSV file
write_csv(result_dataset, csv_path)


# Testing the entire code and the `write_csv` function to see if it works... This time, we're outputting to `Output_dataset2.csv`

# ### For Beyonce

# In[53]:


# Songs of Beyonce
url_to_scrape = 'https://www.azlyrics.com/k/knowles.html'
result_dataset = song_dataset(url_to_scrape)

# Specifying the path where you want to save the CSV file
csv_path = 'output_dataset2.csv'

# Calling the write_csv function to save the dataset to a CSV file
write_csv(result_dataset, csv_path)


# ### For Cardi B
# 
# To be outputed to the same csv file as Beyonce's

# In[54]:


# Songs of Cardi B
url_to_scrape = 'https://www.azlyrics.com/c/cardi-b.html'
result_dataset = song_dataset(url_to_scrape)

# Specifying the path where you want to save the CSV file
csv_path = 'output_dataset2.csv'

# Calling the write_csv function to save the dataset to a CSV file
write_csv(result_dataset, csv_path)


# ---
# 
# This completes the project
