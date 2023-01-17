from flask_qa import create_app
from flask_qa.config.config import Config


app = create_app(Config)

# if __name__ == '__main__':
#     app.run(port = 5007)