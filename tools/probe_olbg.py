#!/usr/bin/env python3
"""Probe public OLBG listing availability from a GitHub-hosted runner.

The probe respects robots.txt, identifies itself, and stops immediately for a
403/429. It makes no requests to OLBG's disallowed APIs or authenticated areas.
"""
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser
import json
import time

AGENT = 'CoverageDeskResearch/1.0 (+https://github.com/karagemop466-tech/Olbg7)'
ROOT = 'https://www.olbg.com'
URLS = ['/betting-tips/Tennis/3', '/betting-tips/Basketball/4', '/betting-tips/Snooker/8']


def read(url):
    request = Request(url, headers={'User-Agent': AGENT, 'Accept': 'text/html,text/plain;q=0.9'})
    with urlopen(request, timeout=25) as response:
        return response.status, response.read(2_000_001), response.headers.get_content_charset() or 'utf-8'


def main():
    output = Path('probe-output')
    output.mkdir(exist_ok=True)
    report = []
    try:
        status, data, charset = read(ROOT + '/robots.txt')
        robots = RobotFileParser()
        robots.parse(data.decode(charset, 'replace').splitlines())
        report.append({'url': ROOT + '/robots.txt', 'status': status})
        for i, path in enumerate(URLS):
            url = ROOT + path
            if not robots.can_fetch(AGENT, url):
                report.append({'url': url, 'error': 'robots.txt disallows this user agent'})
                continue
            time.sleep(2)
            try:
                status, data, charset = read(url)
                if len(data) > 2_000_000:
                    raise ValueError('response exceeded 2 MB safety limit')
                (output / f'page-{i}.html').write_text(data.decode(charset, 'replace'), encoding='utf-8')
                report.append({'url': url, 'status': status, 'bytes': len(data), 'file': f'page-{i}.html'})
            except HTTPError as exc:
                report.append({'url': url, 'status': exc.code, 'error': str(exc)})
                if exc.code in (403, 429):
                    break
            except (URLError, TimeoutError, ValueError, OSError) as exc:
                report.append({'url': url, 'error': str(exc)})
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        report.append({'url': ROOT + '/robots.txt', 'error': str(exc)})
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    print("::notice title=OLBG access probe::" + json.dumps(report, separators=(",", ":")))


if __name__ == '__main__':
    main()
