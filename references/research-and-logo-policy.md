# Research and official-logo policy

## Source hierarchy

Use fresh browsing for every fixture. Prefer, in order:

1. Official competition, federation, league, and club sources.
2. Official press conferences, squad announcements, injury updates, and match reports.
3. Reputable first-party statistical providers named by the competition or club.
4. Reputable reporting only for facts unavailable from primary sources.

For each claim record: text, category (`verified`, `reported`, `inference`, `user-opinion`), URL, publisher, publication/update date, event date when different, and retrieval time.

Never manufacture recent form, expected lineups, injuries, suspension status, odds, quotes, or player availability. A likely lineup is an inference unless officially announced.

## Fixture identity

Confirm:

- official club names and short names;
- home/away order;
- competition and round;
- kickoff time and timezone;
- whether “tomorrow” or similar relative language matches the actual date.

If any two authoritative sources conflict, surface the conflict and avoid stating the disputed item as fact.

## Logo acceptance

Accept a logo only from:

- an official club brand/media/press page;
- an asset URL demonstrably served by the club's official site and used for the current identity;
- an official competition/league/federation team page when the club does not publish a usable asset.

Do not accept:

- search thumbnails;
- Wikipedia or Wikimedia;
- fan sites, kit sites, logo databases, stock sites, or reposted social images;
- AI output, traced vectors, screenshots of a crest, emoji, or hand redraws;
- an old crest chosen from memory.

Official provenance matters independently from pixel similarity. Never say “官网一致” without a recorded official source.

## Logo treatment

- Prefer SVG, then transparent PNG at the highest practical resolution.
- Preserve the complete crest, original aspect ratio, colors, internal text, clear space, and transparency.
- Do not recolor, distort, rotate, crop, simplify, rebuild, or add effects inside the crest.
- External drop shadow is permitted only when subtle and not mistaken for part of the mark.

## `sources.json` minimum schema

```json
{
  "fixture": {
    "home": "Official club name",
    "away": "Official club name",
    "competition": "Competition",
    "kickoff_iso": "2026-08-13T20:00:00+08:00",
    "verified_urls": ["https://official.example/match"]
  },
  "logos": [
    {
      "team": "Official club name",
      "official_page_url": "https://club.example/brand",
      "asset_url": "https://club.example/assets/crest.svg",
      "evidence_class": "club-brand-page",
      "retrieved_at": "2026-08-12T12:00:00+08:00",
      "file": "logos/club.svg",
      "mime_type": "image/svg+xml",
      "width": 512,
      "height": 512,
      "sha256": "64 lowercase hex characters"
    }
  ]
}
```

`evidence_class` must be one of `club-brand-page`, `club-site-current-asset`, or `competition-official-page`.

The manifest validator checks provenance shape, denied third-party hosts, safe local paths, and byte hashes. It cannot prove that an arbitrary domain is official; the agent must establish that through primary-source browsing and preserve the evidence URL.
