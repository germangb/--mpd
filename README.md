# μMPD
μMPD is a very small MPD client meant for statusbars and notifications. The script will connect to the MPD server and listen
to playlist and mixer events (new songs playin and volume changes)

For each event, a new line is printed to **stdout**, so that you can pipe it to whatever program you want. This README includes examples for dzen2

When the connection to MPD is lost, the script stops running.

## Usage example
```
$ # host and port will default to localhost and 6600 respectively
$ ./mmpd.py --host 127.0.0.1 --port 6600
```

## Usage example with dzen2
```
$ ./mmpd.py --host 127.0.0.1 --port 6600 | dzen2
```

## Display formats

You can modify the output format. With `--format` you specify the "song playing" format. With `--format-error` you speify the format of the "connection error" message. With `--format-none` you specify the format of the message that shows up when the MPD playlist ends
```
$ ./mmpd.py \
    --format 'Now playing {title} by {artist}' \
    --format-error 'Connection to {host}:{port} refused :/' \
    --format-none 'There is no more music'
```

Tag | Data
--- | ---
{title} | Song title (falls back to the file name)
{artist} | Song artist
{date} | Song date
{genre} | Song genre
{track} | Track number
{album} | Song album
{volume} | Volume 0-100
{host} | Hostname from --host
{port} | Port from --port

## Random stuff
### I want a fancy volume indicator
You can pipe the output to some program that reformats the text
```
$ # cool_volume.py is a script that finds the volume integer and replaces it with something fancy like ▁▂▃▅█
$ # the {volume} tag has to be wrapped as specified in this --format
$ ./mmpd.py --format 'Now Playing {title} #({volume})' | ./cool_volume.py | dzen2
```

### I want dzen2 to only appear when something starts playing
One option is to reformat the output as a command, including the pipe to dzen2 there
```
$ ./mmpd.py --no-mixer \
    --format 'echo "MMPD :: ♫ Now Playing ♪ {title} by {artist}" | dzen2 -p 2 ' | sh
```
This will make dzen show up and disappear after a 4 seconds. If you go with this option, then disable mixer events as they will spam dzen2
## Additional information
The Music Player Daemon protocol [http://www.musicpd.org/doc/protocol/](http://www.musicpd.org/doc/protocol/)
