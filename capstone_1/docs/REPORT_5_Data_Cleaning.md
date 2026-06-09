# Report 5: Data Cleaning

## Cleaning Operations

### 1. Name Normalization

Applied to match NUTS codes with FUA boundaries:

| Original | Normalized |
|----------|-----------|
| Wien | vienna |
| Praha | prague |
| Lefkosia | nicosia |
| Bruxelles | brussels |
| Bucuresti | bucharest |
| Grad Zagreb | zagreb |

### 2. NUTS Mapping

- Source: NUTS2021.xlsx Metropolitan sheet
- Logic: Map NUTS2 (first 4 chars) to city name
- Example: AT13 → Wien

### 3. FUA Matching

- Method: Normalized name matching
- Matched: 89 out of 212 regions
- Unmatched: Regions without FUA boundary data

### 4. Tree Extraction

- Use actual FUA geometry from Urban Atlas 2021
- Clip tree raster to FUA boundary
- Calculate: tree_km2 / area_km2 * 100 = percentage
- Limited to 500 features per FUA for performance

## Results

| Metric | Count |
|--------|-------|
| Total regions | 212 |
| With population | 212 |
| With FUA match | 89 |
| With tree data | 89 |

## Sample Results

| Rank | Region | Pop | Area km² | Tree km² | Tree % |
|------|--------|-----|----------|----------|-------|
| 1 | Brasov | 2.3M | 316 | 275 | 86.9% |
| 2 | Varna | 827K | 133 | 108 | 80.9% |
| 3 | Oslo | 2.1M | 121 | 95 | 78.8% |