from cloudsoc.core.logger import EventLogger

logger = EventLogger()

logger.log("INFO", "CloudSOC", "Application Started")
logger.log("SUCCESS", "OneDrive", "Connected")
logger.log("SUCCESS", "Google Drive", "Connected")
logger.log("WARNING", "OneDrive", "Storage Above 80%")
logger.log("ERROR", "Telegram", "Upload Failed")

for event in logger.get_events():
    print(event.format())