---
name: football-prediction-avatar-video
description: Turn a user's football match prediction or viewpoint into a verified Chinese vertical talking-head video using the user's avatar image and voice-clone reference audio. Research the fixture, recent form, injuries and lineups; obtain current official club or competition logos; require script approval; create a clean caption-free HeyGen presenter video; and finish it in HyperFrames with single-line Chinese captions, football motion graphics, source images, matching sound effects, QA, and MP4/SRT/project delivery. Use for 足球预测、赛事前瞻、比分预测、数字人足球解说、球队对阵短视频、口播成片、avatar football video, or requests that provide a match opinion and ask for a finished social video.
---

# Football Prediction Avatar Video

Create a reproducible 9:16 football-prediction video from one viewpoint. Keep the user's prediction as editorial direction, verify changing facts independently, and stop at approval gates.

## Fixed production contract

- Use HeyGen for the presenter and cloned voice.
- Use HyperFrames for captions, official logos, match graphics, supporting images, animation, sound effects, inspection, and final render.
- Do not use ChatCut unless the user explicitly requests manual ChatCut finishing.
- Never switch to another generator or editor silently. Report the unavailable dependency and pause.
- Treat generation, voice cloning, and rendering as consequential operations. Do not start them before their gates pass.
- Never present a prediction as certain. Preserve the user's viewpoint while distinguishing verified facts, inference, and opinion.

## Default specification

- Language: Simplified Chinese.
- Format: 1080×1920, 30 fps, H.264 MP4.
- Duration: 55–65 seconds unless the user specifies otherwise.
- Script length: about 280–350 Chinese characters, adjusted to the reference voice's natural pace.
- Structure: suspense hook → both teams' evidence → decisive variables → score prediction → uncertainty/risk note → optional CTA.
- Visual reference: the approved Paris SG vs Aston Villa example—presenter remains primary, top fixture bar, restrained football cards, one-line captions, clean sound-design accents.

## Required inputs

Obtain or reuse all of the following:

1. Both teams, match date, competition, and home/away order.
2. The user's prediction/viewpoint, including a score when they have one.
3. A presenter image the user is authorized to use.
4. A clean reference audio sample the user is authorized to clone.
5. Target platform if not the default vertical short-video format.

Ask only for missing load-bearing inputs. If a team or date is ambiguous, stop and resolve it before research or writing.

## Workflow

### 1. Establish the job folder

Create a non-overwriting folder named `YYYY-MM-DD_home-vs-away/` in the user-selected output directory, or `outputs/` when none is given. Keep:

- `brief.json`
- `research.md`
- `sources.json`
- `script-vNN.md`
- `approvals.json`
- `logos/`
- `media/`
- `avatar-clean.mp4`
- `captions.srt`
- `hyperframes/`
- `final-vNN.mp4`
- `qa.md`

Resolve bundled paths from this skill directory, not from the job directory. Use `<skill>/scripts/check_approvals.py` before HeyGen generation and before final rendering. The state file is a production record, not a substitute for actual user approval.

### 2. Verify the match and football facts

Read [references/research-and-logo-policy.md](references/research-and-logo-policy.md) completely.

Browse current primary sources. Confirm fixture identity, official team names, competition, date/time and home/away order. Research recent form, availability, official injury/team news, and likely tactical variables. Prefer competition, club, league, and federation sources; use reputable reporting only where primary sources do not publish the needed fact.

Record every factual claim and URL in `research.md`. Mark each item as verified fact, source-backed report, inference, or user opinion. If current evidence contradicts the user's premise, explain the conflict before drafting; do not silently rewrite their core prediction.

### 3. Acquire current official logos

For every team, obtain the current crest from this priority order:

1. The club's official brand/media/press page.
2. The club's official website asset used in its current header or team identity.
3. The official competition, league, or federation team page.

Reject search-result thumbnails, Wikipedia/Wikimedia, fan sites, logo aggregators, social reposts, stock libraries, AI-generated or manually redrawn crests. Do not infer an official logo from appearance alone.

Download the highest-quality official SVG or transparent PNG available. Preserve aspect ratio and colors. Do not recolor, redraw, crop into the crest, remove elements, or add text inside it. Store source URL, retrieval date, SHA-256, dimensions, MIME type, and evidence class in `sources.json`. Run `<skill>/scripts/verify_logo_manifest.py <job>` before composition work.

If an official source cannot be verified, stop and ask the user whether to wait, provide the official asset, or accept a clearly disclosed competition-source fallback.

### 4. Draft the script

Write one complete spoken script from the verified research and the user's viewpoint. Follow [references/editorial-and-script.md](references/editorial-and-script.md) completely.

Do not add unsupported injury claims, odds, quotes, or invented statistics. Keep the argument specific enough to justify the prediction but concise enough for the target duration.

### 5. Hard gate: obtain script approval

Present the full script to the user. Include the intended duration, score prediction, and any material uncertainty. Ask for explicit approval or revisions.

Do not clone the voice, synthesize speech, generate the presenter video, create captions, build HyperFrames, or render before an approval message is received. “试验稿”, “先看看”, silence, or approval of the topic does not approve the script.

After explicit approval, write a record into `approvals.json` with `script.approved=true`, version, timestamp, and a SHA-256 hash of the approved script. Any later change to the viewpoint, facts, score, CTA, or spoken wording invalidates approval and returns to this gate.

### 6. Create the clean presenter in HeyGen

Load and follow the installed HeyGen avatar/video skills and current tool schemas. Use the provided audio only as a voice-clone reference, not as final narration. Confirm that the user is authorized to clone it.

1. Upload local media through the supported HeyGen asset route when necessary.
2. Clone the voice and wait until it is ready.
3. Animate the supplied image or reuse the approved private avatar.
4. Generate the approved script in portrait 1080×1920.
5. Explicitly disable captions, titles, logos, text bands, watermarks when controllable, and auto-added visual packages.
6. Save the result as `avatar-clean.mp4`.

Reject the result if it contains burned-in captions or unintended text. Regenerate clean rather than covering generated subtitles with a mask. Never add a bottom mask to a clean source.

Check lip-sync, identity consistency, frame crop, pronunciation of club/player names, voice similarity, audio clarity, and duration. Pause for user review if the avatar or voice materially differs from the approved identity.

### 7. Build the HyperFrames project

Load and follow the installed HyperFrames, HyperFrames CLI, GSAP, captions, typography, motion, and transitions instructions. If HyperFrames is not installed or callable, pause with setup instructions; do not move the project to ChatCut automatically.

Run `npx hyperframes init <job>/hyperframes --video <job>/avatar-clean.mp4 --non-interactive`. Treat HTML as the editable source of truth.

Create `DESIGN.md` using [references/visual-and-audio-spec.md](references/visual-and-audio-spec.md). Use the official logos and verified supporting media. Never place an unlicensed arbitrary web image merely because it fits the narration; prefer official press images, competition assets, user-provided material, or generated non-deceptive background imagery without official marks.

### 8. Captions

Transcribe the clean presenter audio or use word timestamps returned by approved speech generation. Produce `captions.srt` and render captions as an independent HyperFrames layer.

- Show one semantic group at a time, never duplicated.
- Use one visual line only.
- Use at most 8 Chinese characters per card; punctuation does not justify overflow.
- Reveal each card as a group, not character by character.
- Place the caption block above platform description/UI obstruction, using the reference safe zone: approximately y=1540–1645 on a 1920px canvas, then visually verify on the actual shot.
- Default to bold white Chinese text, dark navy stroke/shadow, no permanent band.
- Never create a bottom subtitle or a top-layer mask when the clean source has no burned-in subtitle.

### 9. Fixture graphics, images, motion, and SFX

Use the reference style as a system, not a literal copy of Paris/Villa content:

- Top fixture bar: competition label, both current official logos, Chinese/official short team names, and VS. Keep the presenter's face clear.
- Add 4–6 meaningful visual beats per minute: form card, tactical matchup, player/availability point, key statistic, prediction, or final score.
- Tie every graphic to a spoken claim; avoid decorative data that is not narrated or sourced.
- Use short whoosh/swish sounds for directional entrances, restrained hits for score/stat landings, and a deeper accent for the final prediction. Align each sound to the motion onset.
- Keep sound effects under speech and avoid stacking accents. Use fades and conservative gain.
- Avoid fake broadcast marks, bookmaker styling, excessive particles, or animation on every sentence.

### 10. Visual checkpoint

Render or preview representative frames covering the settled top bar, an ordinary caption, every card type, and the final score. Present the visual sample to the user before the full final render. Record approval in `approvals.json` as `visual.approved=true` with the approved revision hash.

Any material change to placement, caption style, top bar, animation language, or score card invalidates visual approval.

### 11. Validate and render

Run, fix, and rerun:

```bash
npx hyperframes lint <job>/hyperframes
npx hyperframes validate <job>/hyperframes
npx hyperframes inspect <job>/hyperframes --samples 15
```

Inspect real pixels at opening, normal captions, each visual beat, final prediction, and outro. Check logo fidelity, safe zones, caption count and line count, subtitle duplication, burned-in text, mask absence, animation/SFX sync, speech intelligibility, spelling, source accuracy, and output duration.

Run `<skill>/scripts/check_approvals.py <job> --stage render`. Render only after both approvals pass:

```bash
npx hyperframes render <job>/hyperframes --output <job>/final-vNN.mp4 --quality high --fps 30 --strict
```

### 12. Deliver

Deliver:

- H.264 1080×1920 final MP4.
- Independent SRT.
- `avatar-clean.mp4`.
- Editable HyperFrames project.
- `research.md` and `sources.json` with official logo provenance.
- `qa.md` describing checks and any disclosed limitations.

Do not overwrite prior versions. Do not call an unapproved render “final”.

## Failure rules

- Missing/ambiguous fixture: stop before research.
- Material factual conflict: disclose and resolve before script approval.
- Missing official logo provenance: stop before visual composition.
- Unapproved script: stop before any paid generation.
- Burned-in HeyGen subtitle: regenerate clean; do not mask it.
- Missing HyperFrames: report setup requirement and pause; do not default to ChatCut.
- Failed lint, validation, inspect, or visual QA: fix and rerun; do not deliver.

## Bundled resources

- [references/research-and-logo-policy.md](references/research-and-logo-policy.md): primary-source rules and logo manifest requirements.
- [references/editorial-and-script.md](references/editorial-and-script.md): writing, approval, and risk-language rules.
- [references/visual-and-audio-spec.md](references/visual-and-audio-spec.md): portrait layout, caption, Motion Graphics, image, and SFX specification.
- `scripts/check_approvals.py`: enforce approval records before generation or rendering. Run it by absolute skill-relative path.
- `scripts/verify_logo_manifest.py`: validate official logo provenance and file hashes. Run it by absolute skill-relative path.
