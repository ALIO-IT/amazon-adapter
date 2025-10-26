#!/usr/bin/env python3
"""
Test script for Amazon Auto Parts Adapter
"""
import pandas as pd
from adapter.csv_parser import AutoPartsParser
from adapter.amazon_transformer import AmazonTransformer


def test_conversion():
    """Test the CSV conversion process"""
    print("Testing Amazon Auto Parts Adapter...")
    print("=" * 60)
    
    # Read sample file
    with open('sample_autozone.csv', 'rb') as f:
        contents = f.read()
    
    # Parse
    print("\n1. Parsing AutoZone CSV...")
    parser = AutoPartsParser()
    df = parser.parse(contents)
    print(f"   ✓ Parsed {len(df)} rows")
    print(f"   ✓ Columns: {', '.join(df.columns[:5])}...")
    
    # Transform
    print("\n2. Transforming to Amazon format...")
    transformer = AmazonTransformer()
    amazon_df = transformer.transform(df)
    print(f"   ✓ Generated {len(amazon_df)} rows")
    print(f"   ✓ Amazon columns: {', '.join(amazon_df.columns[:5])}...")
    
    # Save test output
    output_file = 'test_amazon_output.csv'
    amazon_df.to_csv(output_file, index=False)
    print(f"\n3. Saved output to: {output_file}")
    
    # Display sample
    print("\n4. Sample output (first 3 rows):")
    print("   " + "-" * 56)
    for idx, row in amazon_df.head(3).iterrows():
        print(f"   Product: {row['item-name'][:50]}")
        print(f"   Price: ${row['standard-price']} | Qty: {row['quantity']} | ID: {row['product-id']}")
        print()
    
    print("=" * 60)
    print("✓ Test completed successfully!")
    print(f"\nYou can now upload '{output_file}' to Amazon.")
    

if __name__ == "__main__":
    test_conversion()

