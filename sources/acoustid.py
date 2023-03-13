""" Acoust ID utilities """

import os

import acoustid


async def acoust_id_match(filename: str):
    """ Try to get a fingerprint and match from Acoust ID service """
    try:
        results = acoustid.match(os.getenv('ACOUST_KEY'), filename)

        first = True
        for score, rid, title, artist in results:
            if first:
                first = False
            else:
                print()
            print(f'%s - %s' % (artist, title))
            print('http://musicbrainz.org/recording/%s' % rid)
            print('Score: %i%%' % (int(score * 100)))
    except acoustid.NoBackendError:
        print("chromaprint library/tool not found")
    except acoustid.FingerprintGenerationError:
        print("fingerprint could not be calculated")
    except acoustid.WebServiceError as exc:
        print("web service request failed:", exc.message)
