# entrypoint
import os
from app import create_core

__author__ = 'talamo_a'


app = create_core()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv("PORT")))
