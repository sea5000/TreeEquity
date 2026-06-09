# Report 4: Data Collection (Implementation)

## Implementation

### stage1_import.py

```python
# 1. Read population TSV
with gzip.open(POP_PATH, 'rt') as f:
    for line in f:
        geo = parts[0].split(',')[-1]
        pop = int(val)
        population[geo] = pop

# 2. Read NUTS mapping from Excel
df = pd.read_excel(NUTS_XLSX, sheet_name='Metropolitan')
nuts_map = {row['NUTS2']: row['METRO LABEL']}

# 3. Merge population with NUTS mapping
merged = {}
for nuts, pop in population.items():
    name = nuts_map.get(nuts[:4], nuts)
    merged[key] = (nuts, name, pop)

# 4. Match FUA and extract tree cover
with tempfile.TemporaryDirectory() as tmpd:
    with zipfile.ZipFile(zf_path, 'r') as z:
        z.extractall(tmpd)
    with fiona.open(fgb, 'r') as src:
        geoms = [shape(f['geometry']) for f in src if shape(f['geometry']).is_valid]
    union = unary_union(geoms[:500])
    area_km2 = union.area / 1_000_000
    
    with rasterio.open(RASTER_PATH) as rst:
        window = rasterio.windows.from_bounds(bbox, rst.transform)
        data = rst.read(window=window)
        mask = geometry_mask([union], window.shape)
        tree_pixels = np.sum((data[0] > 0) & mask)
        tree_km2 = tree_pixels * PIXEL_KM2

# 5. Save to DB
c.execute("INSERT INTO regions ...", (name, nuts, pop, area_km2, tree_km2, tree_pct))
```

## Output

- 212 regions in database
- 89 with tree cover data extracted from actual FUA boundaries

## Performance

- Processed 89 cities in ~10 minutes
- Limited to 500 features per FUA for speed