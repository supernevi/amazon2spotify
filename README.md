# amazon2spotify
A small application to import playlists from amazon music to spotify.

## How to use it
* checkout this project
* install chrome browser (if chrome is impossible for you, let me know)
* setup python environment
* start your favourite IDE 
* Go to https://developer.spotify.com/dashboard/ and create an application (use http://localhost:8080/ as redirect URL). Find and copy the client ID and the secret key, then paste it into **config.py**
* Find your public playlist link from Amazon Music. You'll have to paste it into **config.py**
* adjust your userid/username in the config.py
* Run **Application.py**

## How this application works
At first your default browser will be opened, because you need to authorize this application to use the spotify API. 
Since the authorization token will be cached, you just need to do that once (or after token expiration).

Then the chrome browser starts (in test mode) and opens the amazon url. 
The HTML source code will be analyzed for the playlist name and the track names.

The amazon part ends here and the spotify magic begins...

At first the new empty playlist will be created on spotify (old playlist name + [Amazon]) (you can rename or merge playlists later if you want on spotify).
Then each earlier found track will be searched in spotify to get the spotify specific identifier. 
It is just a simple search by **Artist Title** and use the first result (like you might do that in the spotify app).

As the last step the collected spotify track identifiers will be used to add the songs to your playlist on spotify.

Then you can copy the next amazon url and start the app again.  


## Note
* no guarantee every single song will be imported correctly (but in my case with 1000 songs was a great success)
* since amazon music uses javascript to render the page (SPA) and I didn't want to mess up with cross-origin issues, 
a browser is needed to firstly render the list entries into the DOM, which then is used to find the songs
* selenium is used under the hood (that's why chrome starts in test mode)

