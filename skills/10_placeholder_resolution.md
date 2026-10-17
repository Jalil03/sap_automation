# Skill — Placeholder Resolution
Detect placeholders such as `##`, relative dates, and source-relative references. Do not resolve `##` without a non-null explicit mapping in `mappings/placeholders.yaml`. Unresolved placeholders remain canonically valid; an unresolved mandatory placeholder blocks readiness with a structured reason.
