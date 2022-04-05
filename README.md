# AMP
Adaptive Music Player for Spotify

The idea of this project is that playing music appropriate for a user's activity is more engaging and will reduce skips. I tried to keep the spaghetti to a minimum, but I don't know what I'm doing so it is a bit messy. 

There are also quite a few interesting inconsistencies across the code as I was learning during the creation of this project. For example, using dict.get("something") instead of dict["something"] in connection.py, but switching in speaker.py or the use of f strings which I learned of halfway through the project.

|File/Folder|Description|
|----|-----------|
|main.py|The main script|
|connection.py|Assigning an intensity from 0 to 5 to user's current activiy|
|speaker.py|Using assigned intensity to create a playlist in user's Spotify account|
|cred.py|Spotify API credentials (obviously didn't include my credentials)|
|preferences|Contains names of programs with intensities assigned to them|
|Example API Outputs|Some outputs from the Spotify API, sans personal information, made pretty by yours truly|
