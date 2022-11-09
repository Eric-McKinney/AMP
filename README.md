# AMP
Adaptive Music Player for Spotify

The idea of this project is that playing music appropriate for a user's activity is more engaging and will reduce skips. I tried to keep the spaghetti to a minimum, but I don't know what I'm doing so it is a bit messy. 

There are also quite a few interesting inconsistencies across the code as I was learning during the creation of this project. For example, using dict.get("something") instead of dict["something"] in connection.py, but switching in speaker.py or the use of f strings which I learned of halfway through the project.

### Addendum:
About seven months later as of writing this addendum (November 2022) I would like to give some context to bits and pieces of this project. As you may be able to tell from the description above, I was not super confident in my Python skills. 

This project was my first project in Python. I learned a lot along the way and now that I've had time to digest the experience and apply and refine my skills elsewhere I understand the finer details of my project and programming in general.

The comments being rather inconsistent across the project ranging from sparse to overabundant might seem rather strange, but there is a reason. I presented my project to the local community in a science fair style event. I initially thought I was going to show the source code in my presentation, so I began to make thorough comments to make the code more accesible to the average person. Shortly after that I decided not to show the source code in my presentation, so I stopped creating those rather verbose comments. I would have removed these comments but there was always a chance that someone might ask to see the source code.

### Key
|File/Folder|Description|
|----|-----------|
|main.py|The main script|
|connection.py|Assigning an intensity from 0 to 5 to user's current activiy|
|speaker.py|Using assigned intensity to create a playlist in user's Spotify account|
|cred.py|Spotify API credentials (obviously didn't include my credentials)|
|preferences|Contains names of programs with intensities assigned to them|
|Example API Outputs|Some outputs from the Spotify API, sans personal information, made pretty by yours truly|
