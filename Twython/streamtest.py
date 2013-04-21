from twython import Twython

def on_results(results):
    """A callback to handle passed results. Wheeee.
        """
    
    print results

Twython.stream({
               'username': '@leopoldsg94',
               'password': 'leopold321',
               'track': 'python'
               }, on_results)