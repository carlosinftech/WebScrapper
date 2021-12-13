
from src.Navigator import Navigator


def connect():
    """Project WebScraper. This method launches the execution. """
    navigator = Navigator()
    navigator.create_session()


if __name__ == '__main__':

    connect()


