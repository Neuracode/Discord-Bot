import firebase_admin

cred = firebase_admin.credentials.Certificate('Neruabot/Firebase/neuracode-discord-bot-firebase-adminsdk-mor5r-5576ccdbbf.json')
default_app = firebase_admin.initialize_app(cred)