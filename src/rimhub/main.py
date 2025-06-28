from rimhub.app import RimHubApp
from rimhub.core.logger import setup_basic_logger

def main():
    logger = setup_basic_logger(__name__)
    try :
        logger.info("正在启动RimHub...")
        app = RimHubApp("config/config.yaml")
        app.run()
    except Exception as e:
        logger.exception(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
