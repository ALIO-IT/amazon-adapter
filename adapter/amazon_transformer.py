"""
Amazon Transformer - Converts auto parts data to Amazon upload format
"""
import pandas as pd
from typing import Dict, Any


class AmazonTransformer:
    """
    Transforms auto parts data to Amazon's product upload format.
    
    Amazon Auto Parts Template typically requires:
    - product-id (SKU)
    - product-id-type (SKU, UPC, EAN, etc.)
    - item-name (Product title)
    - brand-name
    - manufacturer
    - product-description
    - item-type (Product type)
    - standard-price
    - quantity
    - product-tax-code
    - condition-type (New, Used, Refurbished)
    - part-number
    - item-weight
    - item-length
    - item-width
    - item-height
    - list-price
    """
    
    def __init__(self):
        # Amazon required fields
        self.required_fields = [
            'product-id',
            'product-id-type',
            'item-name',
            'brand-name',
            'standard-price',
            'quantity',
            'condition-type',
        ]
        
        # Amazon recommended fields
        self.recommended_fields = [
            'manufacturer',
            'product-description',
            'item-type',
            'part-number',
            'item-weight',
            'item-length',
            'item-width',
            'item-height',
            'list-price',
        ]
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform input DataFrame to Amazon upload format
        
        Args:
            df: Input DataFrame with standardized columns
            
        Returns:
            DataFrame in Amazon upload format
        """
        amazon_df = pd.DataFrame()
        
        # Map product-id (SKU)
        amazon_df['product-id'] = self._get_column_or_default(
            df, ['part_number', 'sku', 'product_id'], 'AUTO-PART-{index}'
        )
        
        # Generate index-based SKUs if needed
        if amazon_df['product-id'].str.contains('{index}').any():
            amazon_df['product-id'] = amazon_df['product-id'].apply(
                lambda x: x.format(index='{:06d}'.format(amazon_df.index[amazon_df['product-id'] == x][0]))
            )
        
        # Product ID type
        has_upc = 'upc' in df.columns and df['upc'].notna().any()
        if has_upc:
            amazon_df['product-id-type'] = df['upc'].apply(
                lambda x: 'UPC' if pd.notna(x) and str(x).strip() != '' else 'SKU'
            )
            # Use UPC as product-id if available
            original_product_ids = amazon_df['product-id'].copy()
            amazon_df['product-id'] = df.apply(
                lambda row: str(row['upc']).strip() if pd.notna(row.get('upc')) and str(row['upc']).strip() != '' 
                else original_product_ids[row.name], axis=1
            )
        else:
            amazon_df['product-id-type'] = 'SKU'
        
        # Item name (title)
        amazon_df['item-name'] = self._build_title(df)
        
        # Brand name
        amazon_df['brand-name'] = self._get_column_or_default(
            df, ['brand', 'manufacturer'], 'Generic'
        )
        
        # Manufacturer (can be same as brand)
        amazon_df['manufacturer'] = amazon_df['brand-name']
        
        # Product description
        amazon_df['product-description'] = self._build_description(df)
        
        # Item type (category)
        amazon_df['item-type'] = self._get_column_or_default(
            df, ['category', 'type'], 'AutoPart'
        )
        
        # Standard price
        amazon_df['standard-price'] = self._get_column_or_default(
            df, ['price'], 0.00
        )
        
        # List price (MSRP, typically same or higher than standard-price)
        amazon_df['list-price'] = amazon_df['standard-price'] * 1.2  # 20% markup as default
        amazon_df['list-price'] = amazon_df['list-price'].round(2)
        
        # Quantity
        amazon_df['quantity'] = self._get_column_or_default(
            df, ['quantity', 'stock'], 0
        )
        
        # Product tax code (auto parts standard)
        amazon_df['product-tax-code'] = 'A_GEN_TAX'
        
        # Condition type
        amazon_df['condition-type'] = self._get_column_or_default(
            df, ['condition'], 'New'
        )
        # Standardize condition values
        amazon_df['condition-type'] = amazon_df['condition-type'].apply(
            lambda x: self._standardize_condition(str(x))
        )
        
        # Part number (manufacturer part number)
        amazon_df['part-number'] = self._get_column_or_default(
            df, ['part_number', 'sku'], ''
        )
        
        # Dimensions and weight
        amazon_df['item-weight'] = self._get_column_or_default(
            df, ['weight'], ''
        )
        amazon_df['item-length'] = self._get_column_or_default(
            df, ['length'], ''
        )
        amazon_df['item-width'] = self._get_column_or_default(
            df, ['width'], ''
        )
        amazon_df['item-height'] = self._get_column_or_default(
            df, ['height'], ''
        )
        
        # Fulfillment channel (default to merchant fulfilled)
        amazon_df['fulfillment-channel'] = 'DEFAULT'
        
        # Additional automotive-specific fields
        if 'year' in df.columns or 'make' in df.columns or 'model' in df.columns:
            amazon_df['fitment-year'] = self._get_column_or_default(df, ['year'], '')
            amazon_df['fitment-make'] = self._get_column_or_default(df, ['make'], '')
            amazon_df['fitment-model'] = self._get_column_or_default(df, ['model'], '')
        
        return amazon_df
    
    def _get_column_or_default(self, df: pd.DataFrame, column_names: list, default: Any) -> pd.Series:
        """
        Try to get data from multiple possible column names, return default if none exist
        """
        for col in column_names:
            if col in df.columns:
                series = df[col].copy()
                # Replace empty/null values with default
                if isinstance(default, str):
                    series = series.fillna(default)
                    # Convert to string and replace empty strings
                    series = series.astype(str)
                    series = series.apply(lambda x: default if x.strip() == '' or x == 'nan' else x)
                elif isinstance(default, (int, float)):
                    series = pd.to_numeric(series, errors='coerce').fillna(default)
                return series
        
        # No matching column found, return series of defaults
        return pd.Series([default] * len(df), index=df.index)
    
    def _build_title(self, df: pd.DataFrame) -> pd.Series:
        """
        Build product title from available fields
        Format: Brand + Part Number + Description
        """
        titles = []
        
        for idx, row in df.iterrows():
            parts = []
            
            # Add brand if available
            if 'brand' in df.columns and pd.notna(row.get('brand')) and str(row['brand']).strip():
                parts.append(str(row['brand']).strip())
            
            # Add part number if available
            if 'part_number' in df.columns and pd.notna(row.get('part_number')) and str(row['part_number']).strip():
                parts.append(str(row['part_number']).strip())
            
            # Add title/description
            if 'title' in df.columns and pd.notna(row.get('title')) and str(row['title']).strip():
                parts.append(str(row['title']).strip())
            
            # If no title components, use generic
            if not parts:
                parts.append('Auto Part')
            
            title = ' - '.join(parts)
            
            # Limit to Amazon's title length (200 characters)
            if len(title) > 200:
                title = title[:197] + '...'
            
            titles.append(title)
        
        return pd.Series(titles, index=df.index)
    
    def _build_description(self, df: pd.DataFrame) -> pd.Series:
        """
        Build product description from available fields
        """
        descriptions = []
        
        for idx, row in df.iterrows():
            desc_parts = []
            
            # Start with main description if available
            if 'title' in df.columns and pd.notna(row.get('title')):
                desc_parts.append(str(row['title']).strip())
            
            # Add brand and part number info
            if 'brand' in df.columns and pd.notna(row.get('brand')):
                desc_parts.append(f"Brand: {row['brand']}")
            
            if 'part_number' in df.columns and pd.notna(row.get('part_number')):
                desc_parts.append(f"Part Number: {row['part_number']}")
            
            # Add category if available
            if 'category' in df.columns and pd.notna(row.get('category')):
                desc_parts.append(f"Category: {row['category']}")
            
            # Add fitment information if available
            fitment_parts = []
            if 'year' in df.columns and pd.notna(row.get('year')) and str(row['year']).strip():
                fitment_parts.append(str(row['year']))
            if 'make' in df.columns and pd.notna(row.get('make')) and str(row['make']).strip():
                fitment_parts.append(str(row['make']))
            if 'model' in df.columns and pd.notna(row.get('model')) and str(row['model']).strip():
                fitment_parts.append(str(row['model']))
            
            if fitment_parts:
                desc_parts.append(f"Fits: {' '.join(fitment_parts)}")
            
            # Add notes if available
            if 'notes' in df.columns and pd.notna(row.get('notes')) and str(row['notes']).strip():
                desc_parts.append(str(row['notes']).strip())
            
            description = '. '.join(desc_parts)
            
            # If no description, use generic
            if not description or description.strip() == '':
                description = 'Quality auto part for your vehicle.'
            
            # Limit to reasonable length (2000 characters for Amazon)
            if len(description) > 2000:
                description = description[:1997] + '...'
            
            descriptions.append(description)
        
        return pd.Series(descriptions, index=df.index)
    
    def _standardize_condition(self, condition: str) -> str:
        """
        Standardize condition values to Amazon's acceptable values
        """
        condition_lower = condition.lower().strip()
        
        if condition_lower in ['new', 'brand new', 'brand-new', '']:
            return 'New'
        elif condition_lower in ['used', 'pre-owned', 'preowned']:
            return 'Used'
        elif condition_lower in ['refurbished', 'rebuilt', 'remanufactured']:
            return 'Refurbished'
        else:
            return 'New'  # Default to New

