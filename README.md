# Spotify Repository

![Logo of the Project](https://cdn.pixabay.com/photo/2016/11/03/20/03/music-on-your-smartphone-1796117_1280.jpg)

This repository contains Python scripts for archiving and analyzing Spotify playlists using the Spotify Web API.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing
1. Make sure you have Python installed on your system (version 3.6 or later).

2. Clone the repository to your local machine
```
git clone https://github.com/JiGro/SpotiPy.git
```

3. Install the required packages
```
pip install -r requirements.txt
```

4. Set ENV Variables 
```
########################################################################
CLIENT_ID=''
CLIENT_SECRET=''
REDIRECT_URI=''
########################################################################
```

5. Run the code using the following command:
```
python Weekly_Archiving.py
python User_Analysis.py
```
For weekly archiving, a cron job is recommended. This way, my weekly archiving playlist is dating back to November 2020.

## Authors
- **Jimmy (JiGro)** - *Initial work* - [My Github Profile](https://github.com/JiGro)