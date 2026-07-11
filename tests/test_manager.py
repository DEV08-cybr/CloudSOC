from cloudsoc.plugins.manager import PluginManager

manager = PluginManager()

manager.initialize_all()
manager.connect_all()

for plugin in manager.collect_all():
    print(plugin)