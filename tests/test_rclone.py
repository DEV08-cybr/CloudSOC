from cloudsoc.services.rclone import RcloneService


def test_rclone_installed():
    service = RcloneService()

    assert service.is_installed() is True


def test_list_remotes():
    service = RcloneService()

    remotes = service.list_remotes()

    assert isinstance(remotes, list)


def test_config_path():
    service = RcloneService()

    config = service.config_path()

    assert config is not None