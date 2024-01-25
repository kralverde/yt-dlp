import re

from typing import TYPE_CHECKING
from .ffmpeg import FFmpegPostProcessor
from ..extractor import list_extractor_classes

if TYPE_CHECKING:
    from ..YoutubeDL import YoutubeDL

_URL_REGEX = re.compile(r'(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')

class CrawlDescriptionsPP(FFmpegPostProcessor):
    def __init__(self, downloader: 'YoutubeDL'):
        FFmpegPostProcessor.__init__(self, downloader)
        self._downloader = downloader
        self._extractors = ('YouTube',)

    def run(self, info):
        if 'description' not in info:
            return [], info

        urls = _URL_REGEX.finditer(info['description'])
        valid_url_sets = (map(lambda extractor: extractor._match_valid_url(url[0]), 
                              (clazz for clazz in list_extractor_classes() if clazz.IE_DESC in self._extractors)) 
                              for url in urls)
        
        valid_urls = set(url[0] for group in valid_url_sets for url in group if url)

        seen_urls = self._downloader._url_seen.intersection(valid_urls)
        new_urls = valid_urls.difference(seen_urls)

        if seen_urls:
            self.write_debug(f'Not adding {", ".join(seen_urls)} as they have already been seen.')
        if new_urls:
            self.to_screen(f'Adding {", ".join(new_urls)} to be downloaded.')

        self._downloader._url_seen.update(new_urls)
        self._downloader._url_list.extend(new_urls)

        return [], info
