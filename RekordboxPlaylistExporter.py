import os
import xml.etree.ElementTree as ET
import re
import urllib.parse
import logging
from datetime import datetime

# Get the current working directory
current_directory = os.getcwd()

# Set up logging
log_filename = f'RekordboxPlaylistExporter_{datetime.now().strftime("%d%m%y_%H%M%S")}.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Log the current directory
logging.info(f'Current directory: {current_directory}')

# Path to the XML file in the current directory
xml_file_path = os.path.join(current_directory, 'RekordboxCollection.xml')

# Function to clean up folder and playlist names
def clean_name(name):
    # Remove invalid characters for Windows filenames
    return re.sub(r'[<>:"/\\|?*]', '', name)

# Function to process playlists and folders
def process_playlists(node, current_path):
    for child in node.findall('NODE'):
        node_type = child.get('Type')
        name = clean_name(child.get('Name'))  # Clean the name
        if node_type == '1':  # Type '1' indicates a playlist
            track_keys = [track.get('Key') for track in child.findall('TRACK')]
            collection_dict[name] = {
                'Type': 'Playlist',
                'Entries': track_keys
            }
            create_playlist_file(name, track_keys, current_path)
        elif node_type == '0':  # Type '0' indicates a folder
            folder_path = os.path.join(current_path, name)
            os.makedirs(folder_path, exist_ok=True)  # Create folder
            logging.info(f'Created folder: {folder_path}')
            collection_dict[name] = {
                'Type': 'Folder',
                'Entries': []
            }
            process_playlists(child, folder_path)  # Recursively process sub-nodes

# Function to create a playlist file
def create_playlist_file(playlist_name, track_keys, current_path):
    playlist_file_path = os.path.join(current_path, f'{playlist_name}.m3u')
    with open(playlist_file_path, 'w', encoding='utf-8', newline='\n') as f:  # Set encoding to utf-8
        for key in track_keys:
            # Look up the track information in the collection_dict
            track_info = collection_dict.get(key)
            if track_info:
                # Write only the location to the file, replacing ASCII characters
                location = track_info['Location'].replace("file://localhost/", "")  # Remove prefix
                cleaned_location = urllib.parse.unquote(location)  # Decode URL-encoded characters
                f.write(f"{cleaned_location}\n")
    logging.info(f'Created playlist file: {playlist_file_path}')

# Rename the ROOT folder to ROOT.bak if it exists
root_folder_path = os.path.join(current_directory, 'ROOT')
backup_folder_path = os.path.join(current_directory, 'ROOT.bak')

if os.path.exists(root_folder_path):
    os.rename(root_folder_path, backup_folder_path)
    logging.info(f'Renamed folder: {root_folder_path} to {backup_folder_path}')
else:
    logging.info(f'The folder {root_folder_path} does not exist, skipping rename.')

# Read the XML file
try:
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Create a dictionary for the Collection
    collection_dict = {}
    for track in root.find('COLLECTION').findall('TRACK'):
        track_id = track.get('TrackID')
        collection_dict[track_id] = {
            'Name': track.get('Name'),
            'Artist': track.get('Artist'),
            'DateAdded': track.get('DateAdded'),
            'Location': track.get('Location').replace("file://localhost/", "")  # Remove prefix
        }

    # Process the playlists starting from the ROOT node
    process_playlists(root.find('PLAYLISTS'), current_directory)

except FileNotFoundError:
    logging.error(f'The file {xml_file_path} was not found.')
except ET.ParseError:
    logging.error('Error parsing the XML file.')