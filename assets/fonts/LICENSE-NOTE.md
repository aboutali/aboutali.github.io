# Font licensing

All font files in this directory are subset (latin-only) WOFF2 builds
downloaded from Google Fonts and redistributed under the
[SIL Open Font License 1.1](https://openfontlicense.org/) (OFL).

| Family | Style | Source |
|---|---|---|
| Newsreader | normal (roman), variable weight 200–800 | https://fonts.google.com/specimen/Newsreader |
| Newsreader | italic, variable weight 200–800, variable optical size 6–72 | https://fonts.google.com/specimen/Newsreader |
| JetBrains Mono | normal, variable weight 400–800 | https://fonts.google.com/specimen/JetBrains+Mono |

Files were fetched via Google's `css2` endpoint
(`https://fonts.googleapis.com/css2?family=...`) with a WOFF2-capable
User-Agent (2026-09-11; Newsreader roman added with the v4 identity, 2026-09-24), keeping only the `/* latin */` `unicode-range`
blocks. No modification was made to the font binaries themselves.

- Newsreader: Copyright 2024 The Newsreader Project Authors
  (https://github.com/NewsreaderProject/newsreader)
- JetBrains Mono: Copyright 2020 The JetBrains Mono Project Authors
  (https://github.com/JetBrains/JetBrainsMono)

Licensed under the SIL Open Font License, Version 1.1. Full license text:
https://openfontlicense.org/documents/OFL.txt
