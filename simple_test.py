import sys
print("START", flush=True)
print("Python:", sys.version, flush=True)
print("Working directory:", sys.path[0], flush=True)

try:
    import pandas as pd
    print("Pandas imported OK", flush=True)
    
    df = pd.read_csv('data/raw/sample_foods.csv')
    print(f"Data loaded: {len(df)} rows", flush=True)
    
    # Simple feature
    df['test_feature'] = df['total_carbs_g'] * 2
    print("Feature created", flush=True)
    
    # Save
    df.to_csv('data/processed/test_output.csv', index=False)
    print("File saved", flush=True)
    
    # Check file
    import pathlib
    path = pathlib.Path('data/processed/test_output.csv')
    print(f"File exists: {path.exists()}", flush=True)
    if path.exists():
        print(f"File size: {path.stat().st_size} bytes", flush=True)
    
    print("SUCCESS!", flush=True)
    
except Exception as e:
    print(f"ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()

print("END", flush=True)
