from cloudsoc.plugins.onedrive import OneDrivePlugin

plugin = OneDrivePlugin()

plugin.connect()

print(plugin.collect())