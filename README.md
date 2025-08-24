# TDLR Project Enrichment

## Usage
1. Upload this repo to GitHub.
2. Go to Actions → **TDLR Enrich & Map — Clean Start** → Run workflow.
3. Inputs:
   - `geocode`: true/false (geocode not yet implemented here).
   - `limit`: number of rows (0=all).
   - `sleep`: delay seconds between requests.
   - `commit_results`: true/false.
4. Results appear in workflow artifacts as `tdlr_enriched_outputs/projects_enriched.csv`.
5. Debug HTML of first pages is saved to `output/debug_*.html`.
