from instagram import client, subscriptions
import pythontwitter2
import storage
import app



def get_pics(user_id, access_token, user_hashtag):
    instagram_client = client.InstagramAPI(access_token=access_token)
    recent_media, next = instagram_client.user_recent_media(user_id=user_id, count = 5)
    photos = []
    for media in recent_media:
        #if hasattr(media, 'tags'):
         #   tagged = media.tags.count(user_hashtag)
          #  if tagged > 0:
                photos.append(media.images['standard_resolution'].url)
    return photos



        #images = []
        #tags = []
        #for tag in media.tags:
         #   if tag == app.user_hashtag:
          #      images[tag] = media.standard_resolution.url
    #print images
    #return images
