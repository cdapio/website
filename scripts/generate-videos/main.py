#!/usr/bin/python

#  Copyright © 2015-2019 Cask Data, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import argparse
import os
import json
from youtube import API

MAX_RESULTS = 50
CHANNEL_ID='UCfkRcekMTa5GA2DdNKba7Jg'

api = None

def search_videos(page_token):
  return api.get('search', part='id,snippet', channelId=CHANNEL_ID, maxResults=MAX_RESULTS, pageToken=page_token, type='video')

def video_preview(video):
  preview_size = ['maxres', 'high', 'medium', 'standard', 'default']
  thumbnails = video['snippet']['thumbnails']
  preview = ''
  for size in preview_size:
    if size in thumbnails:
      preview = thumbnails[size]['url']
      break
  return preview

def extract_video_data(video):
  preview = ''
  video_data = {}
  video_data['videoId'] = video['id']['videoId']
  video_data['title'] = video['snippet']['title']
  video_data['description'] = video['snippet']['description']
  video_data['preview'] = video_preview(video)
  return video_data

def fetch_videos():
  all_videos = []
  total_items = MAX_RESULTS
  page_token = ''
  while page_token is not None:
    response = search_videos(page_token)
    if 'nextPageToken' in response:
      all_videos = all_videos + list(map(extract_video_data, response['items']))
      page_token = response['nextPageToken']
    else:
      page_token = None

  return all_videos

def get_original_videos(path):
  try:
    with open(path) as video_file:
      return json.load(video_file)
  except:
    print('File not found: %s. Will create new one.' % path)
    return {
      'videos': []
    }

def merge_videos(original_videos, youtube_videos, visible, update, update_props):
  props = update_props.split(',')
  marked = []
  for video in youtube_videos:
    matched_video = next((v for v in original_videos['videos'] if v['videoId'] == video['videoId']), None)
    if matched_video is None:
      marked = [video['videoId']] + marked
      video['visible'] = visible
      original_videos['videos'] = [video] + original_videos['videos']
      print('Added new video:\n Link: https://www.youtube.com/watch?v=%s \n Title: %s \n' % (video['videoId'], video['title']) )
    else:
      marked = [video['videoId']] + marked
      if update is not False:
        for prop in props:
          matched_video[prop] = video[prop]
  original_videos['videos'] = list(filter(lambda v: v['videoId'] in marked, original_videos['videos']))
  return original_videos

def save_videos(data, file_path):
  with open(file_path, 'w') as outfile:
    json.dump(data, outfile, indent=2)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-o', '--output', help='Absolute path to output file. Output file can exist.', required=True)
  parser.add_argument('-k', '--api-key', help='Youtube API key.', required=True)
  parser.add_argument('-v', '--visible', help='Append new videos as visible.', default=False)
  parser.add_argument('-u', '--update', help='Update video in output file if it exists.', default=False)
  parser.add_argument('--update-attributes', '--update-attributes', help='Comma separated list of attributes allowed to update. Works only when --update flag is true', default='description,title,preview')
  args = parser.parse_args()

  global api
  api = API(api_key=args.api_key, client_secret='', client_id='')

  original_videos = get_original_videos(args.output)
  youtube_videos = fetch_videos()
  merged_videos = merge_videos(original_videos, youtube_videos, args.visible, args.update, args.update_attributes)
  save_videos(merged_videos, args.output)

if __name__ == '__main__':
  main()
