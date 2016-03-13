#!/usr/bin/env python

import sys
import socket
import argparse

def send (sock, data):
    cc = sock.send(data)
    if cc == 0:
        raise ConnectionError
    return cc

def recv (sock, buffsize):
    rr = sock.recv(buffsize)
    if len(rr) == 0:
        raise ConnectionError
    return rr

def parse (resp):
    parsed = {}
    lines = resp.split('\n')
    for line in lines:
        data = line.split(':', maxsplit=1)
        if len(data) == 2:
            parsed[data[0]] = data[1].lstrip()
    return parsed

def main(args):
    address = (args['host'], args['port'])
    client = socket.socket()
    
    try:
        client.connect(address)
        ok = recv(client, 1024)
        if args['verbose']:
            sys.stderr.write(ok.decode())
        
        first = True

        while True:
            if not first:
                # wait until something happens in the player
                idle = 'idle player mixer\n'
                if args['no_mixer']:
                    idle = 'idle player\n'
                send(client, idle.encode())
                event = parse(recv(client, 1024).decode())
                if args['verbose']:
                    sys.stderr.write(str(event)+'\n')

            first = False
            
            # send a currentsong request
            send(client, b'currentsong\n')
            song = parse(recv(client, 1024).decode()) 
            if args['verbose']:
                sys.stderr.write(str(song)+'\n')
            
            # get status
            send(client, b'status\n')
            status = parse(recv(client, 1024).decode())
            if args['verbose']:
                sys.stderr.write(str(status)+'\n')
            
            # write stuff
            volume = status['volume']
            title = song.get('Title', song['file'])
            artist = song.get('Artist', 'Unknown')
            album = song.get('Album', 'Unknown')
            date = song.get('Date', 'Unknown')
            track = song.get('Track', 'Unknown')
           
            if not bool(song):
                sys.stdout.write(args['format_none'].format(host=args['host'], port=args['port'], volume=volume))
                sys.stdout.write('\n')
            else:
                sys.stdout.write(args['format'].format(
                    host=args['host'], port=args['port'],
                    volume=volume, title=title, artist=artist, album=album, date=date)) 
                sys.stdout.write('\n')
            
            sys.stdout.flush()

    except ConnectionError:
        sys.stderr.write('Connection to MPD refused or lost\n')
        sys.stdout.write(args['format_error'].format(host=args['host'], port=args['port']))
        sys.stdout.write('\n')
    except KeyboardInterrupt:
        sys.stderr.write('Interrupted\n')
        pass
    finally:
        sys.stdout.flush()
        sys.stderr.flush()
        client.close()

if __name__ == '__main__':
    argp = argparse.ArgumentParser()
    argp.add_argument('--host', default='localhost', help='MPD host')
    argp.add_argument('--port', type=int, default=6600, help='MPD port')
    argp.add_argument('--format', default='μMPD :: ♫ {title} :: {artist} :: {album} ({date}) :: volume {volume}', help='Specify output format')
    argp.add_argument('--format-error', default='μMPD :: Connection to {host}:{port} refused', help='specify connection error message format')
    argp.add_argument('--format-none', default='μMPD :: No more music to play :(', help='Specify output format for whenever MPD ends the music playlist')
    argp.add_argument('--verbose', action='store_true', help='Write debug information to stderr')
    argp.add_argument('--no-mixer', action='store_true', help='Disable mixer events (volume updates)')
    main(vars(argp.parse_args()))
