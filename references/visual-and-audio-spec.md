# Visual and audio specification

## Contents

- Canvas and protected areas
- Approved standalone cover and fixture bar
- Captions and sensitive visible text
- Supporting visuals and motion language
- Sound effects and required visual samples

## Canvas and protected areas

- Canvas: 1080×1920 at the clean source frame rate; use 25 fps when the source is 25 fps.
- Keep ordinary critical content at least 48px from left/right edges. Treat x=0–56 as a hard left phone-edge exclusion zone for persistent widgets.
- Reserve y=0–110 as a hard upper phone-UI exclusion zone for the in-video fixture bar. Default the bar top to y=120 and keep its bottom at least 24px above the measured presenter hair/head top.
- Put ordinary captions around y=1540–1645 by default, then inspect real frames against the target platform UI.
- Do not put captions at the extreme bottom.
- Do not add a bottom band or mask to a clean source.

## Approved standalone cover

Use the reusable structure in [cover-structure.md](cover-structure.md) unless the user explicitly approves another cover. The reference image is `assets/approved-cover-reference-v01.png` in the skill folder.

- Delivery: independent 1080×1920 platform-cover PNG/JPG, not a clip inside the MP4.
- Upper left: gold competition pill, large two-line gold/white headline, analysis subtitle with a red edge, and three short topic cues.
- Center right: the approved presenter, clearly separated from the dark navy background and not covering the title.
- Keep the presenter face, hair, and upper-body silhouette visually in front of decorative elements. Integrate the portrait through matched grading, light direction, grain, depth, and soft edge transitions; a hard-edged pasted cutout is a failed cover.
- Bottom: one rounded fixture panel containing both current official crests, Chinese names, optional small English names, central gold `VS`, Beijing kickoff time, and verified venue.
- Raise the bottom fixture panel to a default 150px bottom margin; require its bottom y to be no greater than 1780 on the 1920px canvas.
- Use a dark navy editorial football background, warm gold, white, one red accent, and restrained real club colors.
- Change only match-specific content and approved presenter assets; keep the composition hierarchy stable across future videos.
- Do not add an entrance/hold/exit to the default MP4. Start presenter picture and source audio at `0.00s`.
- Inspect both the standalone cover image and the MP4 frame at `0.00s`. Do not include player controls, app UI, bookmaker styling, or unsupported claims.
- If the cover is also embedded as MP4 poster metadata, verify it is not a duration-bearing frame or clip and that the presenter still appears at video time `0.00s`.

## Fixture bar

Use a rounded, dark navy sports panel with restrained club-color accents. Include:

- competition/round label;
- current official crest for each team;
- Chinese or official short team name;
- compact English/official label when space permits;
- central VS.

Keep logos undistorted and visually balanced without forcing equal crest shapes. On 1080×1920, use top y=120 by default and never y<110. Record the bar and face/hair bounds and require `fixture_bar_bottom_y <= presenter_hair_top_y - 24`. When the safe band is tight, reduce the bar height or internal padding instead of moving it upward or covering the head. Animate the container and content with one short entrance. Avoid repeating the entrance throughout the video.

## Persistent search widget

- Keep a compact search/discovery widget to the left of the presenter's head throughout the presenter section. On 1080×1920, place it at x=64 by default and never x<56; reduce its width if necessary instead of allowing the phone edge to clip it.
- Use `查看更多` with a clear view/search icon as its title; never leave the English placeholder `search` visible.
- Use the selected presenter's saved brand text. The approved 七姐 default is `7姐聊球`.
- Type the text near the start of the presenter timeline, keep it visible, then clear and retype every 10 seconds. Keep the cursor and breathing effects subtle.
- Keep the widget outside the face/head box and away from the fixture bar.

## Captions

- Use [`../assets/approved-caption-reference-v01.png`](../assets/approved-caption-reference-v01.png) as the canonical v03 visual reference.
- Display no punctuation in captions. Strip every Chinese, ASCII, and Unicode punctuation character from rendered caption text and SRT cue text, including commas, periods, colons, semicolons, quotation marks, brackets, dashes, ellipses, middle dots, and slashes.
- Preserve the approved spoken wording and timestamp mapping; punctuation removal is a display-layer transformation, not permission to alter narration.
- Regroup by meaning after stripping punctuation. Remove empty groups and replace punctuation-dependent score notation with words when necessary, for example `3-0` → `三比零`.
- One line.
- Determine cue length from semantic phrasing and measured available width; there is no fixed character quota.
- Show the complete cue at once. Never use character-by-character reveal or split one cue across two rendered lines.
- Fit inside the horizontal safe area. Re-segment first when a cue is too wide, then make a small responsive font adjustment only if needed. Do not accept clipping, overflow, or a second line.
- Use `white-space: nowrap` and verify the rendered caption bounds remain between x=48 and x=1032 on the 1080px canvas. Hidden overflow is a failure, not a fit strategy.
- Use a compact translucent dark-navy rounded capsule with a short blue rail on the left and a short red rail on the right. Use bold white main text, restrained team-color keywords, and warm-gold emphasis. Do not underline text.
- No duplicate caption layer.
- Do not add a full-width permanent background or bottom mask. The compact local capsule belongs only to the active cue.
- Validate the final SRT with `scripts/validate_captions.py`; any punctuation is a blocking error.

## Sensitive visible text

- Treat red or otherwise marked terms in the user's supplied script as display-layer substitutions, not permission to change narration.
- Prefer a clear icon that preserves the intended meaning. If no clear icon exists, use concise pinyin initials. Store the exact spoken phrase and display replacement separately in `caption-plan.json` so alignment follows the audio phrase rather than the icon glyphs.
- Scan cover text, captions, cards, logos-adjacent labels, screenshots, B-roll, and English text. Reject `SKY Bet`, other bookmaker names, odds panels, betting calls to action, and betting-interface elements.
- Crop or replace a source image when prohibited text is visible. Do not blur or cover official crests, and do not alter the approved spoken wording unless the user approves a new script.

## Supporting visuals

Use 4–6 significant visual beats per minute, but only 3–4 of them should be large material cards in a normal 60–90 second video. Use small icon, number, crest, or keyword accents for the remaining beats. Choose only beats that aid comprehension:

- recent-form strip;
- tactical matchup/formation cue;
- verified availability or player card;
- one narrated statistic;
- decisive-variable card;
- final score prediction.

Images must be official, user-provided, properly licensed, or generated as non-deceptive atmosphere. Do not place generated badges or counterfeit broadcast graphics.

Keep the approved presenter background coherent. Do not animate isolated spectators, people, flags, lamps, or room objects from a still image as short independent loops; this produces the rejected artificial-background effect. When real background motion is requested, prefer licensed/official moving footage with a clean composite, or regenerate the entire scene coherently and treat it as a material visual change.

Use the approved semi-transparent navy material-card treatment: effective outer-shell opacity 0.50–0.65, 8–12px backdrop blur, and 0.70–0.82 opacity for inner reading panes. The text and icons must remain clear while the presenter stays partially visible beneath the shell. Transparency is not permission for high card density. Large material cards may cover no more than 35% of narrated runtime; preserve at least 65% presenter-only runtime, hold each card no longer than 5 seconds, leave at least 3 seconds between cards, and keep the opening 4 seconds and ending 5 seconds free of large cards.

For an opening streak that is already conveyed by an icon caption such as `⚽17✅15`, animate the success check on its spoken number and omit the large center-screen record card. Do not repeat the same statistic in caption and card.

## Motion language

- Use GSAP transforms and opacity with deterministic, seekable timelines.
- Use 0.25–0.55s entrances; settle before the viewer must read.
- Use slide/wipe for directional cards, scale/impact for numbers and scores, and restrained glow for the final prediction.
- Do not animate every sentence or obscure the presenter.
- Preserve natural presenter motion. Do not cover the hands repeatedly with cards, and do not introduce a visual loop that makes genuine hand gestures appear repetitive.
- Do not post-stretch the complete avatar clip to change speaking speed. Set the requested speed during approved generation; picture/audio time-stretching is allowed only as an explicitly reviewed sync-preserving repair.

## Sound effects

- Treat sound accents as the default companion to every meaningful card or graphic entrance, not as an optional final polish.
- Directional slide/wipe: airy whoosh or swish.
- Crest/fixture panel landing: short clean click or restrained soft hit.
- Stat/number landing: short soft hit or tick.
- Defensive shield/hold graphic: compact lock or latch accent.
- Sensitive-word icon replacement: subtle pop or tick when the icon is a visual beat; keep ordinary caption changes silent.
- Material-card exit: low reverse swish or soft exit accent only when the card visibly departs.
- Final score: deeper hit with a subtle tail.
- Align transient onset to the visible motion onset within about two frames.
- Keep speech dominant; lower or remove an effect that masks consonants.
- Vary adjacent sound families so repeated cards do not all use the same whoosh. Use one primary accent per visual beat and avoid stacking effects.
- Do not use a background music bed unless the user requests it.

## Required visual samples

Inspect at least:

- standalone cover image at full resolution;
- cover face/upper-body occlusion and edge-integration check at full resolution;
- first presenter frame at `0.00s` and before any unintended overlap;
- settled opening fixture bar and persistent search widget;
- ordinary caption over the most crowded presenter pose;
- every unique card design;
- final score card;
- ending frame.

Check face clearance, crest fidelity, spelling, caption punctuation absence, caption line/card length, platform safe zone, search title/text/retype behavior, animation end states, and absence of bottom mask. Record `cover_fixture_bottom_y`, `fixture_bar_top_y`, `fixture_bar_bottom_y`, `presenter_hair_top_y`, `search_box_left_x`, `material_card_shell_opacity`, and `material_card_backdrop_blur_px` in QA.

Also record whether a zero-duration MP4 poster is embedded, whether the source frame extraction covered every expected frame, and whether any artificial background-person/object animation was used.
