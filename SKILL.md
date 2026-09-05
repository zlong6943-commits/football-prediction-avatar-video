---
name: football-prediction-avatar-video
description: Turn a user's football match prediction or viewpoint into a verified Chinese vertical talking-head video using the user's avatar image and voice-clone reference audio. Research the fixture and current official logos; preserve or approve the exact narration; enforce the installed HeyGen spending caps; create a clean caption-free presenter source; and finish it in HyperFrames with word-aligned single-line Chinese captions, sensitive-text substitutions, the approved football cover/search/fixture system, synchronized sound effects, measured audiovisual QA, and unambiguous MP4/SRT/source/project delivery. Use for 足球预测、赛事前瞻、比分预测、数字人足球解说、球队对阵短视频、口播成片、avatar football video, or requests that provide a match opinion and ask for a finished social video.
---

# Football Prediction Avatar Video

Create a reproducible 9:16 football-prediction video from one viewpoint. Keep the user's prediction as editorial direction, verify changing facts independently, and stop at approval gates.

## Fixed production contract

- Use HeyGen for the presenter and cloned voice.
- Use HyperFrames for captions, official logos, match graphics, supporting images, animation, sound effects, inspection, and final render.
- Do not use ChatCut unless the user explicitly requests manual ChatCut finishing.
- Preserve the approved presenter plate and its natural background by default. Do not fake background life by separately looping, warping, or puppeting still spectators or room elements; when background motion is requested, use a verified real moving plate or regenerate a coherent whole scene and obtain approval for the visual change.
- Never switch to another generator or editor silently. Report the unavailable dependency and pause.
- Treat `40 credits` and `US$2.00` as the independent default cumulative hard ceilings for this installation. Prefer the lowest compatible HeyGen photo-avatar model and target about 29 credits. Permit a higher USD ceiling only for one named job when the user explicitly authorizes the HeyGen official API and a numeric cap; preserve the authorization text in `approvals.json`, keep the credit ceiling at 40, prohibit paid retries, and require the bundled budget checker to validate the task-scoped exception. The installed task-scoped override ceiling is US$4.00. Never infer or reuse an override for another job.
- Treat generation, voice cloning, and rendering as consequential operations. Do not start them before their gates pass.
- Never present a prediction as certain. Preserve the user's viewpoint while distinguishing verified facts, inference, and opinion.

## Standing defaults for this installation

- The user granted standing direct-generation authorization on 2026-08-16 when they personally provide a complete script or marked script screenshot and explicitly ask for production. Record the exact script hash and authorization text, then proceed without asking them to reply `批准 vNN` again.
- This standing authorization does not cover agent-written or agent-revised spoken wording. If any narration changes, or research would change the fixture or core conclusion, show the complete revised script and obtain explicit approval.
- When research finds a non-core numerical or wording discrepancy in a directly authorized user script, preserve the spoken script, record the discrepancy, and do not repeat or amplify the disputed detail in cards or cover text. Reconfirm only when the fixture, central argument, or conclusion would materially change.
- Every meaningful card, crest panel, statistic, icon replacement, and prediction graphic should receive one motion-matched sound accent by default: whoosh/swish for directional entry, light tick/soft hit for data or logo landing, lock/click for defensive emphasis, and a deeper restrained hit for the final prediction. Keep speech dominant and avoid stacking sounds.
- Treat marked sensitive terms as a display-layer instruction: keep the approved narration unchanged, replace the visible term with an appropriate icon, and use pinyin initials only when no clear icon exists. Reject `SKY Bet`, other bookmaker branding, and betting-interface text from captions, cards, covers, and source images.
- Build caption timing from word/token timestamps in the clean presenter audio. Never divide sentence-level SRT time proportionally by character count. Retiming captions also retimes related cards and sound accents.
- Use the approved visual baseline without another visual-approval round when no material layout or style choice changes: a standalone cover asset that is not placed on the video timeline, an official-logo fixture bar clear of the head, the persistent `查看更多` search widget, v03 captions, and the established card/SFX language. A material deviation still requires a new visual checkpoint.
- For the approved 七姐 profile, show `7姐聊球` in the persistent search widget and clear/retype it every 10 seconds. Resolve a different presenter's approved brand text from its saved profile; never silently reuse the wrong persona label.
- For the approved 七姐 quality baseline, prefer the saved native-portrait `7姐-白色衣服-竖屏` photo avatar and `7姐声音`. When a task-scoped budget permits Avatar IV, use one continuous 1080×1920 segment with `expressiveness=low`, no motion prompt, and no burned captions. Voice speed is job-scoped: obey the current request exactly; otherwise use the selected profile's saved default. Historical values such as `0.9`, `1.0`, or `1.1` are not permission to carry a one-off speed into another job. Do not change speed by post-production time-stretching because that risks lip-sync. Do not substitute a horizontal avatar and enlarge/crop it to portrait. A previous US$4 allowance is evidence of an approved quality route, not reusable spending authorization for another job.
- Treat mobile-safe graphic geometry as a hard 1080×1920 baseline. Put the standalone-cover fixture panel at a default 150px bottom margin and never let its bottom exceed y=1780. Put the in-video fixture bar at default y=120, never above y=110, and keep its bottom at least 24px above the measured presenter hair/head bound; compact the bar if those constraints conflict. Put the persistent search widget at default x=64 and never left of x=56. Record all measured bounds in `qa-report.json`.
- Deliver the cover as a separate 1080×1920 image and, when the MP4/container supports it without adding timeline media, embed the same image as poster/attached cover art. The poster must not become frame 0, a hidden hold, or a duration-bearing video segment.
- Preserve the approved semi-transparent material-card treatment: outer shell effective opacity 0.50–0.65 with 8–12px backdrop blur and inner reading panes around 0.70–0.82. The presenter is the primary picture: large material cards may cover at most 35% of narrated runtime, each card normally lasts 2.5–4.5 seconds and never more than 5 seconds, and adjacent cards require at least 3 seconds of presenter-only breathing room. Keep the opening 4 seconds and ending 5 seconds free of large material cards unless the user explicitly requests otherwise.
- Render 1080×1920 H.264 with AAC 48 kHz. Preserve the clean source frame rate; use 25 fps when the source is 25 fps instead of converting it to 30 fps.

## Default specification

- Language: Simplified Chinese.
- Format: 1080×1920, source fps (25 fps default), H.264 MP4 with AAC 48 kHz audio.
- Duration: let a user-supplied approved script run at the reference voice's natural pace without shortening it. Use 55–65 seconds only as the default for an agent-written script when the user has not requested another duration.
- Script length: about 280–350 Chinese characters only for agent-written 55–65 second drafts; preserve a user-supplied complete script exactly.
- Structure: suspense hook → both teams' evidence → decisive variables → score prediction → uncertainty/risk note → optional CTA.
- Visual reference: export the approved Arsenal vs Manchester City cover structure as a separate thumbnail asset, then use the Paris SG vs Aston Villa presentation system from video time `0.00s`—presenter remains primary, top fixture bar, restrained football cards, one-line captions, and clean sound-design accents.

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
- `presenter.json`
- `generation-budget.json`
- `research.md`
- `sources.json`
- `script-vNN.md`
- `approvals.json`
- `logos/`
- `media/`
- `avatar-clean.mp4`
- `captions.srt`
- `caption-plan.json`
- `caption-sync.json`
- `sound-plan.json`
- `hyperframes/`
- `final-vNN.mp4`
- `av-sync-report.json`
- `delivery.json`
- `qa-report.json`
- `qa.md`

Resolve bundled paths from this skill directory, not from the job directory. Use `<skill>/scripts/check_approvals.py` and `<skill>/scripts/check_generation_budget.py` before HeyGen generation. Use the approval check again before rendering. The state files are production records, not substitutes for actual user authorization or a genuine provider quote.

### 2. Verify the match and football facts

Read [references/research-and-logo-policy.md](references/research-and-logo-policy.md) completely.

Browse current primary sources. Confirm fixture identity, official team names, competition, date/time and home/away order. Research recent form, availability, official injury/team news, and likely tactical variables. Prefer competition, club, league, and federation sources; use reputable reporting only where primary sources do not publish the needed fact.

Record every factual claim and URL in `research.md`. Mark each item as verified fact, source-backed report, inference, or user opinion. If current evidence contradicts the user's premise, explain the conflict before drafting; do not silently rewrite their core prediction.

For a user-supplied exact script under standing authorization, separate conflicts into material and non-material. A material conflict changes the fixture, central argument, or conclusion and returns to approval. A non-material discrepancy is logged in `research.md`, left unchanged in speech, and excluded from optional data cards so the edit does not visually certify an unverified detail.

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

### 5. Hard gate or standing direct-generation authorization

Present the full script to the user. Include the intended duration, score prediction, and any material uncertainty. Ask for explicit approval or revisions.

Do not clone the voice, synthesize speech, generate the presenter video, create captions, build HyperFrames, or render before an approval message is received. “试验稿”, “先看看”, silence, or approval of the topic does not approve the script.

Exception for this installation: when the user personally supplies the complete final script or marked screenshot and explicitly requests production, their standing direct-generation authorization satisfies this gate. Do not ask for a version-approval reply. Record the exact supplied text, SHA-256, timestamp, and authorization basis in `approvals.json`. This exception ends immediately if the agent changes any spoken wording or if verified evidence would change the fixture or core conclusion.

After explicit approval, write a record into `approvals.json` with `script.approved=true`, version, timestamp, and a SHA-256 hash of the approved script. Any later change to the viewpoint, facts, score, CTA, or spoken wording invalidates approval and returns to this gate.

### 6. Create the clean presenter in HeyGen

Load and follow the installed HeyGen avatar/video skills and current tool schemas. Use the provided audio only as a voice-clone reference, not as final narration. Confirm that the user is authorized to clone it.

Read [references/production-memory-and-qa.md](references/production-memory-and-qa.md) completely. Resolve `presenter.json` before any paid action: record the exact avatar file hash or existing asset ID, approved persona name, voice name/ID, voice-reference hash, and brand search text. When the user says “上一次”, reuse the most recent explicitly approved matching profile; do not guess between 七姐 and 伟哥.

The user has authorized an automatic API fallback when the signed-in web workflow reports insufficient credits, an unavailable UI action, or a quota-only blocker. Reuse the same approved avatar, voice ID, exact script hash, resolution, aspect ratio, and clean caption-free source policy through the official HeyGen API. Do not ask again merely to switch transport. Never switch to a different presenter, voice, provider, or billable scope without authorization, and record the fallback route and returned job ID in the production state. API fallback is still blocked unless the cumulative worst-case API charge passes both hard caps.

Before submitting, write `generation-budget.json` from a current provider quote or a conservative upper-bound calculation that includes voice, avatar generation, transport, and any platform minimum. Use the lowest compatible photo-avatar model; do not default to a premium or high-motion model. Run `<skill>/scripts/check_generation_budget.py <job> --stage preflight`. Unknown pricing, an optimistic estimate without a safety margin, or a possible total above either cap is a stop condition. A user-authorized task-specific API ceiling above the default must include `api_budget_override` in `approvals.json` with the exact job scope, `HeyGen official API`, numeric USD cap, authorization text/timestamp, and `paid_retries_allowed=false`; it remains invalid for every other job. Do not shorten or rewrite the approved script to force it under budget. Do not make an automatic paid retry.

1. Upload local media through the supported HeyGen asset route when necessary.
2. Clone the voice and wait until it is ready.
3. Animate the supplied image or reuse the approved private avatar.
4. Generate the approved script in portrait 1080×1920.
5. Explicitly disable captions, titles, logos, text bands, watermarks when controllable, and auto-added visual packages.
6. Save the result as `avatar-clean.mp4`.

Choose the most natural low-cost motion setting available within the caps. Request restrained analysis-style delivery: varied but sparse hand gestures, hands sometimes raised and sometimes resting, subtle head/eye movement, neutral-to-engaged expression, no repeated gesture loop, no exaggerated smiling, and no theatrical motion. Cost limits take precedence over motion upgrades.

Do not animate isolated background people or objects from a still presenter image to simulate a live venue. Partial background motion behind an otherwise static plate was rejected as artificial. Prefer a coherent native avatar background; if the user explicitly wants a living stadium, use a properly licensed real moving background or a separately approved full-scene generation with believable global camera, lighting, and crowd motion.

Reject the result if it contains burned-in captions or unintended text. Regenerate clean rather than covering generated subtitles with a mask. Never add a bottom mask to a clean source.

Check lip-sync at the opening, midpoint, and ending; identity consistency; frame crop; pronunciation of club/player names; voice similarity; audio clarity; gesture repetition; and duration. Record the clean-source result. Pause for user review if the avatar or voice materially differs from the approved identity. After the provider reports its charge, update `generation-budget.json` and run the budget checker with `--stage postflight`; if a provider unexpectedly exceeds a cap, block all further paid calls and disclose it.

### 7. Build the HyperFrames project

Load and follow the installed HyperFrames, HyperFrames CLI, GSAP, captions, typography, motion, and transitions instructions. If HyperFrames is not installed or callable, pause with setup instructions; do not move the project to ChatCut automatically.

Run `npx hyperframes init <job>/hyperframes --video <job>/avatar-clean.mp4 --non-interactive`. Treat HTML as the editable source of truth.

Probe the clean source before building. Preserve its duration, frame rate, and audio start. If HyperFrames or the decoder reports sparse keyframes, verify that extracted frame count/coverage matches the expected source frames. If coverage is incomplete or frames freeze, create a visually lossless constant-frame-rate edit proxy at the same fps with frequent keyframes and copied audio; keep `avatar-clean.mp4` unchanged and use it as the synchronization reference. Do not ignore an incomplete-frame warning and do not convert 25 fps to 30 fps merely to silence it.

Create `DESIGN.md` using [references/visual-and-audio-spec.md](references/visual-and-audio-spec.md). Read and follow [references/cover-structure.md](references/cover-structure.md) completely for the default standalone cover asset. Export it separately and do not place it on the main video timeline unless the user explicitly requests an in-band cover. Use the official logos and verified supporting media. Never place an unlicensed arbitrary web image merely because it fits the narration; prefer official press images, competition assets, user-provided material, or generated non-deceptive background imagery without official marks.

### 8. Captions

Read [references/captions-and-sync.md](references/captions-and-sync.md) completely. Transcribe the clean presenter audio or use word timestamps returned by approved speech generation. Produce `caption-plan.json`, `caption-sync.json`, and `captions.srt`, then render captions as an independent HyperFrames layer.

- Keep punctuation in the approved spoken script and timestamp mapping when needed, but remove all punctuation from the displayed caption text and exported SRT cue text before grouping. This includes Chinese and ASCII commas, periods, colons, semicolons, quotation marks, brackets, dashes, ellipses, middle dots, slashes, and similar Unicode punctuation. Do not change the approved narration merely to satisfy this display rule.
- After punctuation removal, regroup captions by meaning; never leave an empty card. Replace punctuation-dependent notation with readable words when needed, such as `3-0` → `三比零`, rather than showing punctuation.
- Show one semantic group at a time, never duplicated.
- Choose each group's length from natural spoken phrasing and available screen width; do not force a fixed character count.
- Fit every complete group on one visual line inside the horizontal safe area. If it does not fit, re-segment the phrase before reducing type size; never wrap it into two lines.
- Reveal the complete group at once, not character by character.
- Place the caption block above platform description/UI obstruction, using the reference safe zone: approximately y=1540–1645 on a 1920px canvas, then visually verify on the actual shot.
- Use the approved v03 caption system by default: compact translucent navy rounded capsule, blue left rail, red right rail, white main text, restrained team-color keywords, and gold emphasis. Do not underline text or add a full-width permanent band. The canonical reference is `assets/approved-caption-reference-v01.png`.
- Never create a bottom subtitle or a top-layer mask when the clean source has no burned-in subtitle.
- Align each cue from its exact spoken phrase, including when the display phrase uses icons or initials. The default standalone cover contributes zero timeline delay. Apply a non-zero cover delay exactly once only when the user explicitly requests an in-band cover, use only a small animation-compensation lead when needed, and verify the result against the actual audio.
- Normalize Traditional/Simplified Chinese and Unicode variants only in a temporary alignment representation. Preserve the approved script and visible Simplified Chinese output. Correct club/player ASR substitutions through alignment against the exact script; do not lower the recognition-similarity gate just to force a pass. If similarity remains below the accepted threshold, rerun recognition or forced alignment.

Run `<skill>/scripts/validate_captions.py <job>/captions.srt` and `<skill>/scripts/validate_caption_sync.py <job>/caption-sync.json` after creating or revising captions. Fix every reported punctuation, multi-line, overflow, overlap, timing, or sync violation before the visual checkpoint and again before final rendering.

### 9. Fixture graphics, images, motion, and SFX

Use the reference style as a system, not a literal copy of Paris/Villa content:

- Standalone cover: use the fixed approved structure—upper-left competition pill, large two-line headline, analysis subtitle plus three topic cues, presenter on the center-right, and a bottom official-logo fixture panel. Keep the presenter's face, hair, and upper-body silhouette visually above decorative panels and unobstructed. Integrate the presenter through matched grading, scene-derived darkness, edge light, depth, and soft transitions; reject an obvious hard-edged pasted cutout. On 1080×1920, raise the fixture panel to a default 150px bottom margin and require `fixture_panel_bottom_y <= 1780`. Export it as a separate PNG/JPG for the platform cover slot. By default it must consume `0.00s` of the MP4; the presenter and source speech begin at video time `0.00s`.
- Top fixture bar: competition label, both current official logos, Chinese/official short team names, and VS. On 1080×1920, use default top y=120 and never y<110; also keep the bar bottom at least 24px above the measured presenter hair/head bound. If the available band is too short, compact the bar rather than moving it into phone UI or over the head.
- Search widget: keep a compact widget to the left of the presenter's head for the full presenter section. On 1080×1920, use default left x=64 and never x<56 so phone-edge cropping cannot clip it. Its title is `查看更多` with a clear view/search icon, never the English word `search`. Type the approved profile text, keep it visible, then clear and retype it every 10 seconds. It must not cover the face or fixture bar.
- Material cards: keep the approved translucent navy treatment with 0.50–0.65 outer-shell opacity, 8–12px backdrop blur, and 0.70–0.82 inner reading panes. The default large-card coverage ratio is `<=0.35`; presenter-only runtime is `>=0.65`. Each card normally lasts 2.5–4.5 seconds, has a hard maximum of 5 seconds, and must be followed by at least 3 seconds without another large card. Keep the first 4 seconds and last 5 seconds card-free. For a 60–90 second video, use only 3–4 large material cards by default. Small icon confirmations, the fixture bar, search widget, and caption capsules do not count as material cards.
- Add 4–6 meaningful visual beats per minute, but satisfy this with a mix of small icon/number accents and only a few large cards. Do not turn every significant sentence into a full material card.
- Tie every graphic to a spoken claim; avoid decorative data that is not narrated or sourced.
- Add one short, varied, motion-matched sound to every meaningful visual entrance: airy whoosh/swish for sliding cards, light tick or soft hit for logos and statistics, lock/click for shield or defensive emphasis, and a deeper accent for the final prediction. Align each sound to the motion onset within about two frames.
- Anchor each card to the same spoken phrase used by its caption. When caption timing changes, update the card and its sound effect in the same revision.
- Keep sound effects under speech and avoid stacking accents. Use fades and conservative gain.
- Use a matched reverse swish or soft exit accent when a major material card clearly leaves, and add restrained emphasis ticks or hits to selected stressed words and icon confirmations. Do not add a sound to ordinary caption changes.
- When an opening streak such as “17颗龙珠摘下15颗” is marked for icon treatment, default to a compact caption such as `⚽17✅15`, animate the success check at the spoken result, and do not duplicate it with a large center-screen record card.
- Avoid fake broadcast marks, bookmaker styling, excessive particles, or animation on every sentence.

### 10. Visual checkpoint

Render or preview the standalone cover asset separately, plus representative MP4 frames covering the presenter at `0.00s`, the settled top bar and search widget, an ordinary caption, every card type, and the final score. Measure and record the cover fixture-panel bottom y, in-video fixture-bar top/bottom y, presenter hair/head top y, search-widget left x, and material-card opacity/blur. If the composition exactly follows the approved baseline, record the baseline asset/revision hashes and standing authorization in `approvals.json` and continue without asking again. Present a visual sample only when there is a material style/layout deviation or the user requested one.

Any material change to placement, caption style, top bar, animation language, or score card invalidates visual approval.

### 11. Validate and render

Run, fix, and rerun:

```bash
npx hyperframes lint <job>/hyperframes
npx hyperframes validate <job>/hyperframes
npx hyperframes inspect <job>/hyperframes --samples 15
```

Inspect real pixels at opening, normal captions, each visual beat, final prediction, and outro. Check logo fidelity, safe zones, caption count and line count, absence of caption punctuation, subtitle duplication, burned-in text, mask absence, animation/SFX sync, speech intelligibility, spelling, source accuracy, and output duration. Run `<skill>/scripts/validate_captions.py <job>/captions.srt` and `<skill>/scripts/validate_caption_sync.py <job>/caption-sync.json` as final gates.

Write `<job>/card-coverage.json` from the authored large-card intervals and run `<skill>/scripts/validate_card_coverage.py <job>/card-coverage.json`. Any coverage above 35%, card longer than 5 seconds, adjacent-card gap under 3 seconds, missing opening/ending clean interval, or configured excessive card count blocks rendering unless the user explicitly requested a dense infographic cut and that exception is recorded in `approvals.json`.

Check at least five caption anchors spanning the opening, early section, midpoint, late section, and ending. At each anchor, confirm the complete caption is visible on one line when the phrase is spoken, the related card matches the narrated claim, and the sound transient lands within about two output frames of the motion onset. Verify that the MP4 starts on the presenter and source speech/content begins at `0.00s`; the standalone cover must not appear in or delay the video.

Then run `<skill>/scripts/verify_av_sync.py --source <job>/avatar-clean.mp4 --final <job>/final-vNN.mp4 --expected-delay 0.0 --face-roi X:Y:W:H --output <job>/av-sync-report.json`. If pauses were edited by retiming picture and clean speech together, compare against that pause-cleaned sync source and record it explicitly. The check must compare at least six distributed audio and picture anchors, prove a constant source-to-final delay, and keep postproduction audio-versus-picture offset and drift within one output frame. Do not rely on timeline metadata or casual playback alone. If the render shifts or prematurely mixes the source audio, rebuild the audio from the clean presenter track with the authored delay (zero by default) and retimed SFX, mux a new version, and rerun the measured check; never hide the problem by shifting captions away from lip-sync.

After the verified render, optionally mux the standalone cover as MP4 attached cover art/poster metadata only. Confirm that the main H.264 stream remains stream 0/default, the poster is marked `attached_pic` or the platform-equivalent, and the MP4 duration, presenter frame 0, audio start, and A/V report remain unchanged. If the target container or platform cannot represent zero-duration cover art safely, deliver only the separate cover image.

Run `<skill>/scripts/check_approvals.py <job> --stage render`. Render only after both approvals pass:

```bash
npx hyperframes render <job>/hyperframes --output <job>/final-vNN.mp4 --quality high --fps <source-fps> --strict
```

Run `<skill>/scripts/validate_delivery_contract.py <job>` only after `av-sync-report.json`, `qa-report.json`, `delivery.json`, and the budget ledger are current. Any failure blocks delivery.

### 12. Deliver

Deliver:

- H.264 1080×1920 final MP4.
- Independent SRT.
- Independent 1080×1920 cover image, also embedded as zero-duration poster metadata when safely supported.
- `avatar-clean.mp4`.
- Editable HyperFrames project.
- `research.md` and `sources.json` with official logo provenance.
- `qa.md` describing checks and any disclosed limitations.

Write `delivery.json` with explicit keys for `final_video` and `clean_avatar_source`; never make the user infer which MP4 is the edited final. Keep both files and label the raw avatar source as “数字人原始无剪辑版”.

Do not overwrite prior versions. Do not call an unapproved render “final”.

## Failure rules

- Missing/ambiguous fixture: stop before research.
- Material factual conflict: disclose and resolve before script approval.
- Missing official logo provenance: stop before visual composition.
- Unapproved script: stop before any paid generation.
- Unknown or over-cap generation quote: stop before submission; do not gamble on the actual charge.
- Failed generation or UI quota block: allow one transport change to the official API only after a fresh budget preflight; no automatic paid retry.
- Burned-in HeyGen subtitle: regenerate clean; do not mask it.
- Missing HyperFrames: report setup requirement and pause; do not default to ChatCut.
- Sentence-level proportional caption timing: reject and regenerate from word/token alignment.
- Low ASR/script alignment similarity caused by Traditional Chinese or misrecognized club/player names: normalize for alignment or rerun recognition; never lower the gate solely to make validation pass.
- Caption overflow or wrapping: re-segment and re-render; do not shrink blindly or accept two lines.
- Sparse-keyframe or frame-freeze warning with incomplete extraction coverage: create a same-fps frequent-keyframe edit proxy and rerender while preserving the clean source as the A/V reference.
- Post-render audio offset: rebuild and remux the audio in a new version, then repeat the six-anchor audio/picture sync check.
- Artificial background-person loops or a visibly pasted cover presenter: reject the visual and revert to the approved natural presenter plate or rebuild the whole background coherently.
- Failed measured audio/picture delay, drift, or correlation: do not deliver, even if captions look correct.
- Material cards exceed the saved coverage, duration, gap, opening/ending, or count limits: reduce or remove cards and recheck; opacity alone does not make excessive card time acceptable.
- Failed lint, validation, inspect, or visual QA: fix and rerun; do not deliver.

## Bundled resources

- [references/research-and-logo-policy.md](references/research-and-logo-policy.md): primary-source rules and logo manifest requirements.
- [references/editorial-and-script.md](references/editorial-and-script.md): writing, approval, and risk-language rules.
- [references/visual-and-audio-spec.md](references/visual-and-audio-spec.md): portrait layout, caption, Motion Graphics, image, and SFX specification.
- [references/cover-structure.md](references/cover-structure.md): mandatory default standalone-cover composition, content slots, zero-timeline policy, and QA.
- [references/captions-and-sync.md](references/captions-and-sync.md): semantic caption planning, sensitive display substitutions, word-level alignment, card/SFX retiming, and five-anchor sync QA.
- [references/production-memory-and-qa.md](references/production-memory-and-qa.md): installed spending caps, presenter/search defaults, no-regression checklist, measured A/V sync, and delivery naming.
- `scripts/check_approvals.py`: enforce approval records before generation or rendering. Run it by absolute skill-relative path.
- `scripts/check_generation_budget.py`: block any paid submit or retry whose conservative cumulative total could cross the default US$2/40-credit limits, or a validated single-job HeyGen API override up to US$4 while the 40-credit limit remains fixed.
- `scripts/align_caption_plan.py`: turn exact spoken phrases plus Whisper/generator token timestamps into aligned SRT and `caption-sync.json`; never use it with display text alone when icons replace spoken words.
- `scripts/validate_captions.py`: reject caption punctuation, multiple text lines, empty cues, invalid timing, overlaps, and forbidden visible terms.
- `scripts/validate_caption_sync.py`: enforce the authored timeline offset (zero by default), five distributed phrase anchors, caption/audio lead bounds, and card/SFX timing.
- `scripts/validate_card_coverage.py`: enforce presenter-first material-card coverage, maximum hold time, clean opening/ending windows, minimum gaps, and card count.
- `scripts/verify_logo_manifest.py`: validate official logo provenance and file hashes. Run it by absolute skill-relative path.
- `scripts/verify_av_sync.py`: measure source-to-final audio and face-region picture delay at distributed anchors and reject drift or postproduction desynchronization.
- `scripts/validate_delivery_contract.py`: final no-regression gate for specs, captions, search/fixture placement evidence, clean source, budget, sync report, and unambiguous delivery paths.
