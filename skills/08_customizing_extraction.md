# Skill — Customizing Extraction
Extract organizational and configuration objects separately from master/transactional/reference data. Examples: sales organization, distribution channel, sales division, sales area, and shipping point. Never use canonical `division`: French `secteur d'activité` is `sales_division`, while logistical `division` is the REFERENCE_DATA object `PLANT`.
Never treat a Customizing instruction as a transaction.
