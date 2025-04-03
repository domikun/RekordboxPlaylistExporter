# RekordboxPlaylistExporter
Tool to extract playlists from Rekordbox collection .xml to .m3u playlist files. This extracts only songlocations. Rating, cue points etc. will be ignored.

# HowTo Use
1. Extract Rekordbox Library into .xml File via File -> extract collection to xml format
2. Name file **RekordboxCollection.xml**
3. Either use RekordboxPlaylistExporter.py or RekordboxPlaylistExporter.exe in same directory
4. ROOT folder containins folders and playlists
5. Locate folder in Traktor and use playlist :)

# Info
When the script run again, the ROOT folder will be moved to ROOT.bak
The script simply converts all existing playlists and creates a new ROOT folder. Diffs are not tracked.
A log file will be written.

# Versions 
Tested with \
Python 3.11 \
Windows 10 \
Rekordbox: 6.8.5 \
Traktor 2.11.3 17
