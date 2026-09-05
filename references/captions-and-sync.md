# Caption planning and audiovisual synchronization

## Build a semantic caption plan

Create `caption-plan.json` before authoring the HyperFrames caption layer. Each cue must carry both the approved spoken phrase used for alignment and the visible display phrase:

```json
[
  {"spoken": "大家别忘了", "display": "大家别忘了"},
  {"spoken": "点赞加关注", "display": "👍⭐"},
  {"spoken": "我们一定能够", "display": "我们一定能够"},
  {"spoken": "成为老朋友", "display": "成为老朋友"}
]
```

- Partition the approved narration in order. Do not omit or duplicate spoken content across cue anchors.
- Segment at natural Mandarin phrase boundaries. Choose the visible length by meaning and measured screen fit, not a fixed character count.
- Show one complete display cue at a time on one rendered line. If it does not fit, split it at the nearest semantic boundary.
- Remove displayed punctuation without changing the spoken phrase. Convert punctuation-dependent scores to words.
- For an icon or pinyin-initial replacement, keep the full original words in `spoken` and only the substitute in `display`.

## Use the approved caption visual

Use `assets/approved-caption-reference-v01.png` as the default reference:

- compact translucent dark-navy rounded capsule;
- short blue left rail and red right rail;
- bold white main text, restrained team-color keywords, warm-gold emphasis;
- no underline, full-width band, bottom mask, duplicate layer, or character-by-character reveal;
- default vertical position near y=1540–1645 on a 1080×1920 canvas, adjusted only after real-frame platform-safe inspection.

Keep the complete cue inside the horizontal safe area. Re-segment before shrinking the type. Verify the widest cue over the most crowded presenter pose.
Set the caption text to `white-space: nowrap` and measure the rendered bounding box: its left edge must be at or beyond 48px and its right edge at or before 1032px on the 1080px canvas. CSS clipping or hidden overflow does not count as fitting.

## Align to the clean speech track

Use word/token timestamps returned by the speech generator or a local transcription of `avatar-clean.mp4`. Prefer the clean presenter audio without SFX.

1. Normalize the exact approved narration only for alignment: remove punctuation and spaces, preserve words and numbers.
2. Normalize Traditional/Simplified Chinese and Unicode compatibility variants in a temporary ASR/alignment copy only. Never convert or rewrite the approved script file as part of this step.
3. Align recognized tokens to the approved spoken text, tolerating recognition substitutions in club and player names. Keep the exact approved names as the authoritative output.
4. Require the script-to-ASR alignment similarity to meet the configured gate, normally at least `0.80`. If it fails, rerun recognition, normalize the alignment representation, or use forced alignment. Never lower the threshold merely to obtain a report marked as passed.
5. Map each plan item's `spoken` range to the aligned token range.
6. Use a `0.0` timeline shift for the default standalone cover. Add a non-zero cover delay exactly once only when the user explicitly requests an in-band cover; that exception changes video timeline position but not source-audio timestamps.
7. Apply a small visual lead only to compensate for the caption entrance animation. Start with 0.12–0.18 seconds, then verify against the rendered audio; synchronization, not a fixed lead value, is the requirement.
8. Derive the cue end from the next semantic phrase or the current phrase end. Avoid overlaps and unreadably short flashes.

Never split a sentence-level SRT block by character ratio. Speech speed varies within every sentence and proportional division produces changing lag.

Use `<skill>/scripts/align_caption_plan.py` when Whisper-compatible token JSON is available. Save its report as `caption-sync.json`.

## Keep captions, cards, and SFX on one clock

- Anchor each meaningful card to the same spoken phrase recorded in the caption plan.
- Let the card begin slightly before or at the claim onset so it settles while the claim is heard.
- Place its whoosh, swish, tick, click, or hit at the visible motion onset within two frames at the actual output fps.
- When caption timing changes, retime the related card and SFX in the same edit. Do not fix only the SRT.
- Keep one primary accent per beat and keep speech dominant.

## Five-anchor QA

Before rendering, run `validate_captions.py` and `validate_caption_sync.py`. After rendering, inspect at least five real frames or short playback ranges:

1. first spoken phrase at the beginning of the MP4;
2. an early phrase around 25% of the speech;
3. a midpoint phrase;
4. a late phrase around 75%;
5. the final phrase.

At every anchor verify:

- the displayed phrase matches what is being spoken;
- the complete cue is visible at once on one line and inside the safe width;
- the caption is neither perceptibly late nor prematurely showing the next phrase;
- the related card represents the current narrated claim;
- the sound transient matches the card motion and does not mask speech.

Also verify that the standalone cover is absent from the MP4 and that presenter picture and narration begin together at `0.00s`. If the rendered audio begins earlier or later than its authored `data-start`, rebuild the final mix from clean speech using the authored delay (zero by default) plus the retimed SFX, then mux it into a new version. Recheck all five anchors; never compensate for an audio-track defect by intentionally misaligning captions or lip movement.

An MP4 poster/attached-cover-art stream does not count as an in-band cover. It is acceptable only when it is marked as non-timeline cover art, leaves the main H.264 stream first/default, and does not change duration or frame-0 presenter content.

Caption anchors are not sufficient evidence of lip sync. After rendering, run `verify_av_sync.py` with a clean face-region ROI and require at least six distributed source-to-final audio/picture measurements. The measured audio delay and picture delay must stay constant and agree within one output frame.

## Required sync record

Keep `caption-sync.json` with the alignment method, cover delay, visual lead, cue timings, speech timings, and visual-beat timing:

```json
{
  "cover_shift_seconds": 0.0,
  "visual_lead_seconds": 0.16,
  "cues": [
    {"index": 1, "text": "欢迎来到7姐新家", "caption_start": 0.0, "caption_end": 1.5, "speech_start": 0.09, "speech_end": 1.51}
  ],
  "visual_beats": [
    {"id": "fixture", "speech_anchor": 0.09, "motion_start": 0.08, "sfx_start": 0.08}
  ]
}
```

Preserve the previous SRT and final MP4 before any timing correction. Deliver a new version and identify it unambiguously as the corrected final file.
