from cloudsoc.services.rclone import RcloneService

r = RcloneService()

for remote in r.list_remotes():
    print(remote)
    print(r.progress_bar(remote))
    print(f"{r.usage_percent(remote):.2f}%")
    print()