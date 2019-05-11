from authlib.flask.client import OAuth
import config
import os

if os.getenv('FLASK_ENV') == 'production':
    config = eval(config.ProductionConfig)
else:
    config = eval('config.DevelopmentConfig')


google_oauth = OAuth()
facebook_oauth = OAuth()


google_oauth.register('google',
                      client_id=config.GOOGLE_CLIENT_ID,
                      client_secret=config.GOOGLE_CLIENT_SECRET,
                      access_token_url='https://accounts.google.com/o/oauth2/token',
                      access_token_params=None,
                      refresh_token_url=None,
                      authorize_url='https://accounts.google.com/o/oauth2/auth',
                      api_base_url='https://www.googleapis.com/oauth2/v1/',
                      client_kwargs={
                          'scope': 'https://www.googleapis.com/auth/userinfo.email',
                          'token_endpoint_auth_method': 'client_secret_basic',
                          'token_placement': 'header',
                          'prompt': 'consent'
                      })


facebook_oauth.register('facebook',
                        client_id=config.FACEBOOK_APP_ID,
                        client_secret=config.FACEBOOK_APP_SECRET,
                        access_token_url='https://graph.facebook.com/oauth/access_token',
                        access_token_params=None,
                        refresh_token_url=None,
                        authorize_url='https://www.facebook.com/dialog/oauth',
                        api_base_url='https://www.facebook.com/v3.3/dialog/',
                        client_kwargs={
                            'scope': 'email',
                            'token_endpoint_auth_method': 'client_secret_basic',
                            'token_placement': 'header',
                            'prompt': 'consent'
                        })

# f"https://www.facebook.com/v3.3/dialog/oauth?client_id={FACEBOOK_APP_ID}&redirect_uri={redirect-uri}&state={state-param}"
