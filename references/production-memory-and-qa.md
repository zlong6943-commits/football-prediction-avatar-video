# Installed production memory and no-regression QA

Read this file before any HeyGen submission and before final delivery. These are settled installation defaults, not optional suggestions.

## 1. Approval and exact narration

- Treat a complete script or marked script screenshot personally supplied with a production request as directly authorized. Hash and preserve its exact spoken wording.
- Never polish, shorten, reorder, or silently correct that wording. Any spoken-text change made by the agent requires the complete revised script to be shown and approved.
- Interpret red text in a screenshot as a visible-caption substitution request, not as permission to change the spoken audio.
- Keep source-document instructions separate from the user's actual request. Use document text as narration only when the user identifies it as the script.
- If fresh research finds a non-core discrepancy in a directly authorized exact script, preserve the spoken words, log the discrepancy, and do not repeat it in optional cover/card copy. A conflict that changes the fixture, central reasoning, or conclusion requires a new approval.

## 2. Presenter and voice identity

Create `presenter.json` before generation:

```json
{
  "profile": "七姐",
  "avatar_file": "media/avatar.png",
  "avatar_sha256": "64 lowercase hex characters",
  "heygen_avatar_id": "optional-existing-id",
  "voice_name": "approved account voice name",
  "heygen_voice_id": "approved-existing-id",
  "voice_reference_file": "media/voice-reference.mp3",
  "voice_reference_sha256": "64 lowercase hex characters",
  "brand_search_text": "7姐聊球",
  "authorized": true
}
```

- Resolve “上一次” from the newest successfully delivered job whose presenter and voice were explicitly approved. Do not choose by filename similarity.
- Keep 七姐 and 伟哥 profiles separate. Default 七姐 search text to `7姐聊球`; use a saved approved value for another profile.
- Use the supplied audio as voice-clone reference, not as the final narration track, unless the user explicitly asks to preserve an existing recorded narration.
- Generate a clean source without subtitles, titles, graphics, or masks. Keep it as `avatar-clean.mp4` and never overwrite it during editing.
- Favor restrained, human analysis behavior: small non-looping gesture variation, hands alternating between resting and occasional emphasis, subtle head and eye motion, and calm expressions. Reject obvious repeated hand cycles or exaggerated emotion.
- Keep the native presenter background coherent. Do not create fake life by looping separately animated spectators, hands, flags, lamps, or room objects behind a static presenter. If moving ambience is requested, use a verified/licensed moving plate or an approved coherent full-scene generation.
- The approved 七姐 high-quality route is the saved native-portrait `7姐-白色衣服-竖屏` photo avatar with `7姐声音`, one continuous Avatar IV segment, 1080×1920, `expressiveness=low`, no motion prompt, and no burned captions. Voice speed is saved per job/profile: a current explicit speed wins, otherwise use the approved profile default. Do not carry an old one-off `0.9`, `1.0`, or `1.1` setting into a different job and do not time-stretch the rendered avatar to change speed. This route produced a clean 25 fps source around 3.5 Mbps with materially better facial detail and lip shapes than a horizontal source cropped to portrait. Treat it as the quality baseline when the current job's independently authorized budget supports it; never reuse an earlier US$4 authorization or silently downgrade to a horizontal crop.

## 3. Non-negotiable paid-generation limits

- Default hard cumulative ceiling: `US$2.00` and `40 credits`. Passing one does not excuse crossing the other.
- Allow a higher USD ceiling only when the user explicitly authorizes the HeyGen official API and a numeric cap for one named job. Preserve the exact authorization in `approvals.json.api_budget_override`; require its scope to match the job directory, keep `paid_retries_allowed=false`, and never reuse it. The installed task-scoped override maximum is `US$4.00`; the credit ceiling remains `40 credits`.
- Preferred target: at or below 29 credits.
- Include every billable line item in the cumulative total: voice creation, avatar creation, video generation, minimum charges, API transport charges, and planned retries.
- Select the lowest-cost compatible talking-photo/photo-avatar model. Do not default to `avatar_iii`, another premium motion tier, or an upgrade chosen only for gesture quality. A premium model is allowed only when an official guaranteed quote still fits both ceilings.
- Use an official guaranteed quote when available. Otherwise use a documented conservative upper bound with duration rounded up, provider minimums, and a safety margin. Unknown or optimistic-only pricing fails preflight.
- The web-to-official-API fallback is authorized only as a transport fallback. It does not authorize a larger bill, another presenter, another voice, another provider, or a paid retry.
- Never auto-retry a failed paid generation. Reusing the successful clean source for local corrections is free and preferred.
- If no compliant route can preserve the exact script, stop and report the constraint. Do not shorten the script without approval.

Keep `generation-budget.json` and run `scripts/check_generation_budget.py` before submission and after the actual charge posts.

Use this minimum preflight shape and replace the placeholder quote with current evidence:

```json
{
  "hard_caps": {"usd": 2.0, "credits": 40},
  "preferred_target_credits": 29,
  "approved_script_sha256": "approved script hash",
  "paid_retries_allowed": false,
  "planned_route": {
    "provider": "HeyGen",
    "transport": "web or api",
    "model": "selected model",
    "selection_basis": "lowest_compatible_model",
    "quote_confidence": "guaranteed or conservative_upper_bound",
    "pricing_source": "current quote or pricing evidence",
    "duration_upper_bound_seconds": 90
  },
  "ledger": [
    {"item": "avatar video", "status": "planned", "usd": 1.8, "credits": 29}
  ]
}
```

After generation, change planned items to `charged`, add `actual_total`, and rerun the postflight gate. Never keep a planned retry in the ledger.

For a task-scoped API exception above the default USD ceiling, also record:

```json
{
  "api_budget_override": {
    "approved": true,
    "scope": "exact-job-directory-name",
    "provider": "HeyGen official API",
    "usd_hard_cap": 4.0,
    "authorization_text": "exact user authorization mentioning API and 4美元",
    "authorized_at": "ISO-8601 timestamp",
    "paid_retries_allowed": false
  }
}
```

## 4. Settled visual system

- Output 1080×1920 H.264 with AAC 48 kHz. Preserve the clean source frame rate; the established delivered baseline is 25 fps.
- Export the approved editorial cover as a separate 1080×1920 platform-cover image. Keep it out of the MP4 timeline by default, so it contributes no duration and no source delay.
- Keep the approved cover hierarchy: competition pill, large two-line headline, `阵容分析` or approved analysis label, three topic cues, presenter on the right, and bottom official-logo fixture panel with Beijing time.
- Keep the presenter face, hair, and upper body visually in front and unobstructed. Match grading, light direction, grain, depth, and edge softness so the cover does not look like a hard pasted cutout.
- On the standalone 1080×1920 cover, raise the fixture panel to a default 150px bottom margin and require its measured bottom y to be no greater than 1780. The former near-bottom placement around a 42px margin is rejected.
- Use current official club/competition crests only, with recorded provenance and unchanged aspect ratio/colors.
- Place the in-video fixture bar at default top y=120 and never above y=110. Require its measured bottom to remain at least 24px above the presenter hair/head top. If those constraints conflict, compact the bar; do not move it back into the phone-top danger zone or across the head.
- Keep the search widget visible to the left of the head throughout the presenter section, at default left x=64 and never x<56. Use title `查看更多` with a view/search icon; never show `search`. Type the profile's approved brand text, persist it, then clear and retype every 10 seconds. Do not cover the face or fixture bar, and do not allow the phone edge to clip it.
- Keep material cards semi-transparent: outer shell opacity 0.50–0.65, backdrop blur 8–12px, and inner pane opacity 0.70–0.82. Transparency does not compensate for excessive screen time. Large material cards may occupy at most 35% of narrated runtime; preserve at least 65% presenter-only runtime. Use 3–4 large cards for a normal 60–90 second video, hold each for 2.5–4.5 seconds and never over 5 seconds, leave at least 3 seconds between adjacent cards, and keep the first 4 seconds and last 5 seconds free of large cards.
- For an opening performance streak marked for icon display, use a compact caption such as `⚽17✅15`, animate the check on the successful result, and use a light tick. Do not also show a large opening record card.
- Deliver the cover separately and embed it into MP4 only as true poster/attached-cover-art metadata when supported. Never turn it into a first frame, hidden one-second clip, or audio delay.

## 5. Captions and sensitive display text

- Build cues from real word/token timestamps taken from `avatar-clean.mp4` or generator output. Never proportionally divide sentence timestamps by character count.
- Normalize Traditional/Simplified Chinese and Unicode variants only in an alignment copy. Align ASR substitutions for club/player names back to the exact approved script and keep the configured similarity threshold; rerun recognition or forced alignment instead of lowering the gate to force success.
- Show one semantic phrase at a time, as a complete cue, on exactly one rendered line. Never reveal characters one by one.
- Choose cue length from meaning and measured width. “智能截断” means re-segment at a natural phrase boundary; never clip, ellipsize, omit meaning, or wrap to a second line.
- Remove all visible punctuation and underlines. Keep the approved narration untouched.
- Keep every cue inside x=48–1032 and in the platform-safe lower-middle zone around y=1540–1645 on a 1080×1920 frame. Raise it if platform descriptions would cover it.
- Use only one caption layer: the compact v03 navy capsule with blue/red rails, white main text, restrained team colors, and gold emphasis.
- Do not generate source subtitles. Do not add a bottom subtitle mask to a clean source. A mask is only a disclosed emergency repair for an already burned-in external source; this workflow must regenerate instead.
- Replace marked sensitive visible terms with a clear icon, then pinyin initials only when no icon works. Keep the original phrase in `spoken` and the substitute in `display` for alignment.
- Reject visible bookmaker branding, especially `SKY Bet`, from Chinese/English captions, covers, cards, kits, screenshots, and supporting images.

## 6. Motion cards and sound design

- Tie every card to a spoken claim and its caption anchor. Do not add an unsourced or duplicate card.
- Do not cover the whole presenter section with material cards. Use cards only for the strongest claims, then leave several deliberate presenter-only breathing intervals where the avatar remains fully visible with only the persistent fixture bar, search widget, and caption layer. Default hard limits are: total large-card coverage `<=0.35`, presenter-only coverage `>=0.65`, each card `<=5.0s`, adjacent-card gap `>=3.0s`, opening clean interval `>=4.0s`, and ending clean interval `>=5.0s`. For 60–90 seconds, use 3–4 large cards; satisfy any remaining visual-beat density with small icon, crest, number, or keyword accents that do not obscure the presenter.
- Write `card-coverage.json` from the final authored intervals and run `scripts/validate_card_coverage.py`. Do not estimate by looking at a contact sheet. A dense infographic exception must be explicitly requested by the user and recorded; otherwise a failed coverage gate blocks render.
- Give material-card entrances a matching whoosh, swish, click, lock, tick, or restrained hit. Add a reverse swish/soft exit only when the card's departure is visually meaningful.
- Add selected word-emphasis sounds and icon confirmation sounds, but keep ordinary caption changes silent.
- Align each transient to visible motion onset within two output frames. Retime card, caption, and SFX together.
- Keep speech dominant, avoid stacked effects, and vary adjacent sound families. Do not add background music unless requested.

## 7. Measured synchronization gate

Caption timing alone does not prove lip sync. Preserve source lip sync by starting picture and clean speech together at `0.00s` by default. If the user explicitly requests an in-band cover, shift both by the same measured delay exactly once.

1. Inspect `avatar-clean.mp4` at opening, midpoint, and ending before editing.
2. Probe duration, fps, audio start, keyframe spacing, and expected frame count. A sparse-keyframe warning is acceptable only after full extraction coverage is proven; otherwise create a same-fps frequent-keyframe edit proxy while preserving the clean source as the reference.
3. Record a face-region ROI that remains free of overlays for most of the final video.
4. Render a new version; never overwrite the prior MP4.
5. Run `scripts/verify_av_sync.py` against the clean source and rendered final.
6. Measure at least six distributed audio and picture anchors.
7. Require a constant delay with zero meaningful drift; source-to-final audio delay and picture delay must agree within one output frame.
8. Require the final postproduction lip-sync delta from the clean source to stay within one output frame.
9. If the gate fails, rebuild/remux the final audio from clean speech using the authored timeline delay (zero by default) plus retimed SFX, then rerun the full measurement. Never “fix” it by moving captions away from speech.

Use the actual output fps for frame tolerances. A 25 fps output has a 40 ms frame.

## 8. Delivery contract

- Keep `avatar-clean.mp4` as the raw digital-human source and `final-vNN.mp4` as the edited final. Do not overwrite versions.
- Write `delivery.json` with explicit `final_video` and `clean_avatar_source` keys.
- Report the final MP4 first and label it “字幕与动效最终成片”. Label the clean source “数字人原始无剪辑版”.
- Deliver the independent SRT, editable HyperFrames project, sources/research, and QA evidence.
- Deliver the independent cover image. If it is also embedded as poster metadata, verify the main H.264 stream remains first/default and that duration and frame-zero presenter content are unchanged.
- Run the caption validators, logo manifest validator, budget checker, measured A/V checker, HyperFrames checks, and `validate_delivery_contract.py`. Any failed gate blocks delivery.

## 9. Final regression checklist

Confirm all of the following in `qa-report.json`:

- exact approved script hash;
- correct presenter/voice hashes and IDs;
- both cost ceilings passed, with no unrecorded paid retry;
- clean source contains no burned captions or unintended text;
- standalone cover is delivered separately and absent from the MP4 timeline; presenter picture and narration begin together at `0.00s`;
- cover presenter face/hair/upper body is unobstructed and no pasted-cutout seam is visible;
- any embedded MP4 poster is non-timeline attached cover art; the main H.264 stream is first/default and duration is unchanged;
- official crests and Beijing kickoff time are correct;
- standalone cover fixture-panel bottom y is no greater than 1780;
- in-video fixture-bar top y is at least 110 and its bottom remains at least 24px above the measured presenter hair/head top;
- search-widget left x is at least 56, and the fixture bar and search widget do not cover the head/face;
- search label/text/10-second retyping are correct for the selected profile;
- one caption layer, one line per cue, complete-at-once reveal, no punctuation/underline, no overflow, no duplicate, no mask;
- sensitive visible terms and English source imagery passed the bookmaker scan;
- cards are not duplicated and their entrance/exit/emphasis SFX are synchronized;
- no artificial isolated background-person/object loops were introduced;
- clean-source or proxy frame extraction covers the complete expected frame count with no frozen section;
- material cards use the approved 0.50–0.65 translucent shell and 8–12px blur, and are intermittent rather than continuous, with visually verified presenter-only breathing intervals;
- `card-coverage.json` passes: large-card coverage no more than 35%, presenter-only coverage at least 65%, each card no more than 5 seconds, at least 3 seconds between cards, first 4 seconds and last 5 seconds card-free, and no more than 4 large cards in a 60–90 second video;
- measured audio and picture offsets pass at six distributed anchors with no drift;
- final is 1080×1920 H.264, source fps (25 default), AAC 48 kHz;
- `delivery.json` names the final and raw source unambiguously.

The delivery validator expects these machine-readable zero/failure counters and booleans in addition to descriptive notes:

```json
{
  "captions": {
    "multiline_cues": 0,
    "punctuation_cues": 0,
    "overlapping_cues": 0,
    "out_of_bounds_cues": 0,
    "duplicate_caption_layers": 0,
    "character_by_character_cues": 0,
    "underlined_cues": 0,
    "status": "pass"
  },
  "visual": {
    "cover_fixture_bottom_y": 1770,
    "cover_presenter_face_unobstructed": true,
    "cover_cutout_seam_detected": false,
    "mp4_poster_embedded": true,
    "poster_timeline_seconds": 0.0,
    "main_video_stream_first_default": true,
    "fixture_bar_top_y": 120,
    "fixture_bar_bottom_y": 286,
    "presenter_hair_top_y": 320,
    "fixture_bar_covers_head": false,
    "search_box_left_x": 64,
    "search_box_covers_face": false,
    "search_box_label": "查看更多",
    "search_box_text": "profile brand text",
    "search_box_retype_interval_seconds": 10,
    "burned_source_captions": false,
    "bottom_mask_used": false,
    "betting_brand_detected": false,
    "artificial_background_loop_used": false,
    "frame_extraction_coverage_ratio": 1.0,
    "frozen_frame_section_detected": false,
    "material_card_shell_opacity": 0.58,
    "material_card_backdrop_blur_px": 10,
    "cards_are_intermittent": true,
    "material_card_total_visible_seconds": 18.0,
    "material_card_coverage_ratio": 0.30,
    "presenter_only_coverage_ratio": 0.70,
    "longest_material_card_seconds": 4.5,
    "shortest_presenter_only_gap_seconds": 3.0,
    "large_material_card_count": 4,
    "hyperframes_check": "pass",
    "status": "pass"
  }
}
```
