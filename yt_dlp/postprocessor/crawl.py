from .ffmpeg import FFmpegPostProcessor

class CrawlDescriptionsPP(FFmpegPostProcessor):
    EXTRACTORS = {
        'Youtube': 'YouTube',
    }
    
    def __init__(self, downloader):
        FFmpegPostProcessor.__init__(self, downloader)

    def run(self, info):
        print('WORKS!')
        print(info['description'])
        return [], info
