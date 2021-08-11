# cachemoney

Extracts files from Chrome/Chromium/Electron cache.

## usage

Requires Python 3.6+ (probably).

This will extract all files whose original URL ended with JPG into `files/`.

```
python -m cachemoney --cache-dir /Users/me/Chrome/Cache --output-root files --filter '*jpg'
```
