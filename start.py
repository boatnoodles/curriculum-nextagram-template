from app import app
import instagram_api
import instagram_web

if __name__ == '__main__':
    context = ('local.crt', 'local.key')  # certificate and key files
    app.run(debug=True, ssl_context=context)
