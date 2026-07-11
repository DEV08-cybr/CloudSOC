from cloudsoc.plugins.gdrive import GoogleDrivePlugin

plugin = GoogleDrivePlugin()

plugin.connect()

print(plugin.collect())