# GMusic Year Wrapper V0.0.0.2 Pre-Alpha
A spotify year wrap like for Google Play Music

Note : This project is highly experimental

## To use GMusic Year Wrapper
`git clone https://github.com/Lolincolc/gmusic_wrapped.git`
<br>
`sudo pip install beautifulsoup4`
<br>
`sudo pip install requests`
<br>
<br>
Then download a history file from Google My Activity containing your Play Music History.
<br>
You can now launch the script with the following options :
<br>
`python main.py [your html history file name]`
<br>
`-v` to enable a full detailed log in log.dt
<br>
`-d [LastFm API key]` to enable duration calculation
<br>
<br>
Your report will be available in report.dat. Note that it usually takes between 1 and 4 hours to complete a report and it can take several more hours with `-d` option.
