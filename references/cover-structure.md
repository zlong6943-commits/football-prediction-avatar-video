# Approved standalone cover structure

Use this structure by default for every football-prediction avatar video unless the user explicitly requests a different cover. The canonical visual reference is [`../assets/approved-cover-reference-v01.png`](../assets/approved-cover-reference-v01.png). Export the cover as an independent platform thumbnail; do not place it on the MP4 timeline by default.

## Composition

Build one 1080×1920 editorial sports cover with five fixed zones:

1. **Competition pill — upper left**
   - Small gold/yellow rounded label.
   - Show the verified competition or round plus a short editorial tag such as `单场焦点`.
   - Keep the label concise and high contrast.

2. **Two-line headline — left visual anchor**
   - Use a very large two-line title.
   - First line: competition, rivalry, or match identity in warm gold.
   - Second line: a neutral content promise such as `焦点战` or `赛前解析` in white.
   - Do not use odds, guaranteed-result language, or an unsupported superlative.

3. **Analysis subtitle and three topic cues — below headline**
   - Put the analysis type in a short dark translucent label with one red vertical accent; default to `阵容分析` when the content supports it.
   - Add exactly three compact topic cues below it, derived from the approved script, for example `中立场交锋　主帅更替　阵容完整度`.
   - Keep all cover text inside the left half and preserve generous negative space.

4. **Presenter — center right**
   - Use the approved presenter image, waist-up or seated upper-body framing.
   - Place the presenter on the center-right, facing the camera, without covering the headline.
   - Keep the face, hair, and upper-body silhouette above decorative panels and unobstructed. A fixture panel may overlap only non-critical lower-body space when the approved structure requires it.
   - Keep the presenter brighter than the background. Blend the left edge into the dark background; do not fabricate a different identity.
   - Avoid the rejected pasted-cutout look. Match scene color, grain, light direction, edge light, shadow softness, and depth; use a soft scene-derived transition instead of a hard mask edge.

5. **Fixture panel — bottom**
   - Use one rounded dark-navy panel with restrained home/away club-color edges.
   - On a 1080×1920 cover, use a default 150px bottom margin. The panel bottom must not extend below y=1780; do not return to the rejected near-bottom placement around a 42px margin.
   - Place the current official crest and Chinese short name for each team on opposite sides; include a small official English name when space permits.
   - Put a gold `VS` in the center.
   - Put Beijing kickoff time and verified venue in one compact bottom line.
   - Preserve crest colors and aspect ratios; never redraw, recolor, or force equal crest shapes.

## Background and color system

- Use a dark navy editorial background built from the presenter setting, an official stadium/trophy image, or generated non-deceptive football atmosphere.
- Keep the left side darker for headline readability and allow brighter photographic detail behind the presenter.
- Default palette: deep navy, warm gold, white, one red accent, and the two clubs' real colors in the fixture panel.
- Do not imitate a bookmaker or broadcast channel. Do not show platform playback controls in the rendered cover.

## Delivery and timing

- Export one independent 1080×1920 PNG or JPG for the platform cover slot.
- When supported safely, also embed that same image as MP4 poster/attached cover art. Keep it outside the timed main video stream and retain the separate image as the authoritative platform cover.
- The cover contributes `0.00s` to the default MP4 timeline. Do not encode it as an opening frame, one-second clip, audio delay, or hidden hold.
- Start the presenter picture and clean source audio at MP4 time `0.00s`, preserving their original synchronization.
- Only when the user explicitly requests an in-band opening cover may it receive timeline duration; record that exception and apply the same measured delay to picture, speech, captions, cards, and SFX exactly once.

## Safe zones and QA

- Keep critical content at least 48px from the left and right edges.
- Keep the bottom fixture panel above platform controls and crop risk. Record its measured bottom y and require `cover_fixture_bottom_y <= 1780`; default to a 150px bottom margin.
- Inspect the exported cover image at full resolution and the MP4 presenter frame at `0.00s`.
- Verify competition, team order, Beijing time, venue, Chinese spelling, official crest fidelity, and absence of prohibited text.
- Treat a different headline layout, presenter side, or fixture-panel structure as a material visual change that requires user approval.
- Verify the cover image is absent from the MP4 timeline and has not shifted narration or captions.
- If poster metadata is embedded, verify the main H.264 stream is still first/default, the poster is identified as attached cover art, duration is unchanged, and seeking to time zero shows the presenter rather than the cover.
