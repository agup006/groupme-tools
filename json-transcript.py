import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import json
import datetime


def printTranscript(messages):
    """Prints a readable "transcript" from the given list of messages.

    Assumes the input list is sorted."""
    f = open('out3.json', 'w')

    for message in messages:
        name = message[u'name']

        time = datetime.datetime.fromtimestamp(message[u'created_at']).strftime('%Y-%m-%d %H:%M')

        # text is None for a photo message
        if message[u'text'] is not None:
            text = message[u'text']
        else:
            text = "(no text)"

        # System Message indicating user changing username
	if message[u'system'] is True:
            system_padded = '(SYS) '
        else:
            system_padded = ''

	# Get number of Likes from message
        if len(message[u'favorited_by']) is not 0:
            favorites_padded = str(len(message[u'favorited_by'])) 
        else:
            favorites_padded = '0'

	# Give URL for picture if needed
        if message[u'picture_url'] is not None:
            pic = ' ; photo URL ' + message[u'picture_url']
        else:
            pic = ''


	string = json.dumps({'timestamp': time, 'message': system_padded + text, 'likes':favorites_padded, 'picurl': pic})
#        string = system_padded + name + ' (' + time + ')' + favorites_padded + ': ' + text + pic
	print >> f, string.encode(sys.stdout.encoding)

def main():
    """Usage: simple-transcript.py filename.json

Assumes filename.json is a JSON GroupMe transcript in chronological order.

Times displayed in local timezone.
    """

    if len(sys.argv) < 2:
        print(main.__doc__)
        sys.exit(1)

    transcriptFile = open(sys.argv[1])
    transcript = json.load(transcriptFile)
    transcriptFile.close()

    printTranscript(transcript)


if __name__ == '__main__':
    main()
    sys.exit(0)
