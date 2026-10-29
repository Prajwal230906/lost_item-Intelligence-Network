# Matching model

The weighted model follows Part 7 of the supplied project instructions. The Review 1 slide deck names the four factors but does not print numeric weights.

| Component | Weight | Score range | Rule |
|---|---:|---:|---|
| Category | 25% | 0–100 | normalized exact category or documented synonym group gives 100; otherwise 0 |
| Item text | 35% | 0–100 | 40% title similarity plus 60% description similarity; each uses Sørensen–Dice overlap of normalized word tokens |
| Location | 25% | 0–100 | normalized exact string gives 100; containment in either direction gives 75; otherwise token overlap uses Sørensen–Dice |
| Date/time | 15% | 0–100 | date component declines linearly across a 30-day window; if both times exist, combine 70% date and 30% time similarity |

The total is the weighted sum of these four component scores and is bounded to 0–100. A score of 55 or higher is stored as a potential match. The threshold and all weights are environment-configurable. Weights must sum to 1.00, the threshold must be between 0 and 1, and the date window must be positive.

Text normalization removes diacritics, folds case, trims whitespace, and tokenizes on punctuation. Sørensen–Dice is `200 × shared unique tokens / (tokens in A + tokens in B)`, so a shorter description that is fully contained in a longer description receives more credit than it did under Jaccard. Titles contribute to the existing text component because reporters often use different wording in descriptions but similar item names. Repeated tokens do not inflate scores. Category synonym groups currently include phone/mobile/cell phone/laptop/computer/tablet as electronics; wallet/purse/keychain as accessories; and backpack/rucksack/handbag as bags. Other categories must match after normalization. Location overlap is lexical; the application does not calculate geographic distance.

When either approximate time is omitted, the date-only score is used. If both times are present, local wall-clock time difference is measured on a 24-hour clock and linearly reduced over a 12-hour half-day. The explanation stores component scores, including title and description sub-scores, elapsed calendar days, and time difference where supplied. Scores only identify suggestions; they do not establish ownership. The person who submitted the LOST report can submit proof details against a suggested FOUND report. Administrators review the proof and approve or reject the claim. Approving a claim resolves both reports and creates an audit event; rejecting a claim leaves both reports open and lets the claimant submit a new request with additional proof.

This model is deterministic and interpretable. It is not machine learning. A 55% threshold is a configurable demonstration value, not a validated institutional operating policy. It should be calibrated against reviewed historical examples before real deployment.
