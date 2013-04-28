from instagram import client, subscriptions
import pythontwitter2
import storage
import app



def get_pics(user_id, access_token):
    instagram_client = client.InstagramAPI(access_token=user_token)
    recent_media, next = instagram_client.user_recent_media(user_id=user_id, count=count)
    for media in recent_media:
        tags = []
        images = []
        for tag in media.tags:
            if tag == app.user_hashtag:
                images[tag] = media.standard_resolution.url
    print images
    return images
