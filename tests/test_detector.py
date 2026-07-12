from cloudsoc.detectors.storage_detector import StorageDetector

detector = StorageDetector()

cloud = {
    "service": "OneDrive",
    "used": "82 GiB",
    "total": "100 GiB",
}

detector.check(cloud)