#!/usr/bin/env python3

from tnlnews import create_app

application = create_app()
if __name__ == "__main__":
    application.run()