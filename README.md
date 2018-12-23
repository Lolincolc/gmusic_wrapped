# GMusic Year Wrapper V0.0.0.0.0.1 Pre-Alpha
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
Then download a history file from Google My Activity containing your Play Music History. Paste it in the same folder and change line 76 with the name of your file. You will also need a token for LastFm API that is used to retrieve song duration. Paste your LastFm token line 133.
<br>
When you are ready launch the script with `python test.py`
<br>
<br>
Note : This can take some time, for a full year history it usually takes between 1 and 3 hours to generate a report.
<br>
<br>
Your report will be available in report.dat and a full detailled logger will be available in out.dat that contains more informations.
<br><br>
I am working on an improved and more automated version, stay tuned !
