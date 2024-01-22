import re

from typing import TYPE_CHECKING
from .ffmpeg import FFmpegPostProcessor

if TYPE_CHECKING:
    from ..YoutubeDL import YoutubeDL

class CrawlDescriptionsPP(FFmpegPostProcessor):
    EXTRACTORS = {
        'Youtube': 'YouTube',
    }

    def __init__(self, downloader: 'YoutubeDL'):
        FFmpegPostProcessor.__init__(self, downloader)
        from ..extractor.youtube import YoutubeIE
        self._valid_urls = re.compile(YoutubeIE._VALID_URL.replace(r'^', '').replace(r'$', ''))
        self._downloader = downloader

    def run(self, info):
        extractor = info['extractor_key']
        if extractor not in self.EXTRACTORS:
            self.to_screen(f'Crawling is not supported for {extractor}')
            return [], info
            
        urls = set(match[0] for match in self._valid_urls.finditer(info['description']) if match[1] and match[2])
        seen_urls = self._downloader._url_seen.intersection(urls)
        new_urls = urls.difference(seen_urls)

        if seen_urls:
            self.write_debug(f'Not adding {", ".join(seen_urls)} as they have already been seen.')
        if new_urls:
            self.to_screen(f'Adding {", ".join(new_urls)} to be downloaded.')

        self._downloader._url_seen.update(new_urls)
        self._downloader._url_list.update(new_urls)

        return [], info
