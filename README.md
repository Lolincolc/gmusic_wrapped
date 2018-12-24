# GMusic Year Wrapper V1 Beta
A spotify year wrap like for Google Play Music

Note : This project is not endorsed by Google

![alt text](https://raw.githubusercontent.com/Lolincolc/gmusic_wrapped/master/example_report.jpg)

## To use GMusic Year Wrapper
`git clone https://github.com/Lolincolc/gmusic_wrapped.git`
<br>
`sudo pip install requests`
<br>
<br>
Then download a history file from Google My Activity containing your Play Music History.
<br>
To download a history file <a href="https://takeout.google.com/u/0/?hl=fr&utm_source=google-account&utm_medium=web&pageId=none"> go here </a>. Detailled instructions are avaialble <a href="https://raw.githubusercontent.com/Lolincolc/gmusic_wrapped/master/howto/help.jpg"> here </a>
<br><br>
You can now launch the script with the following options :
<br>
`python main.py [path/to/your/json/history_file]`
<br>
`-v` to enable a full detailed log in log.dat
<br>
`-d [LastFm API key]` to enable duration calculation with LastFM API
<br>
<br>
Your report will be available in report.dat. Note that it usually takes less than 1 minute to complete a report. However `-d` option can add several hours to the process depending on LastFM API speed.
