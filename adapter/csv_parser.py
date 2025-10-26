"""
CSV Parser for AutoZone-style auto parts data
"""
import pandas as pd
import io
from typing import Union


class AutoPartsParser:
    """
    Parses AutoZone-style CSV files containing auto parts data.
    
    Expected columns (flexible, will adapt to various formats):
    - Part Number / SKU / Item Number
    - Description / Product Name / Title
    - Brand / Manufacturer
    - Price / Unit Price / Cost
    - Quantity / Stock / Inventory
    - Category / Type
    - UPC / Barcode / EAN
    - Weight
    - Dimensions
    - Year / Make / Model / Fitment (optional)
    """
    
    def __init__(self):
        # Common column name mappings (lowercase for matching)
        self.column_mappings = {
            'part_number': ['part number', 'part_number', 'partnumber', 'sku', 'item number', 
                           'item_number', 'itemnumber', 'part#', 'item#', 'product_id', 'product id'],
            'title': ['description', 'title', 'product name', 'product_name', 'productname', 
                     'name', 'item description', 'item_description'],
            'brand': ['brand', 'manufacturer', 'mfr', 'vendor'],
            'price': ['price', 'unit price', 'unit_price', 'unitprice', 'cost', 'msrp', 'retail_price'],
            'quantity': ['quantity', 'qty', 'stock', 'inventory', 'available', 'on_hand', 'on hand'],
            'category': ['category', 'type', 'product_type', 'product type', 'classification'],
            'upc': ['upc', 'barcode', 'ean', 'gtin', 'upc_code', 'upc code'],
            'weight': ['weight', 'item_weight', 'item weight', 'shipping_weight', 'shipping weight'],
            'length': ['length', 'item_length', 'item length'],
            'width': ['width', 'item_width', 'item width'],
            'height': ['height', 'item_height', 'item height'],
            'year': ['year', 'model_year', 'model year', 'vehicle_year'],
            'make': ['make', 'vehicle_make', 'vehicle make', 'car_make', 'car make'],
            'model': ['model', 'vehicle_model', 'vehicle model', 'car_model', 'car model'],
            'condition': ['condition', 'item_condition', 'item condition'],
            'notes': ['notes', 'comments', 'description2', 'additional_info', 'additional info'],
        }
    
    def parse(self, file_content: Union[bytes, str]) -> pd.DataFrame:
        """
        Parse CSV file content and return a standardized DataFrame
        
        Args:
            file_content: CSV file content as bytes or string
            
        Returns:
            DataFrame with standardized column names
        """
        # Read CSV with flexible options
        if isinstance(file_content, bytes):
            df = pd.read_csv(io.BytesIO(file_content), encoding='utf-8', low_memory=False)
        else:
            df = pd.read_csv(io.StringIO(file_content), low_memory=False)
        
        # Strip whitespace from column names
        df.columns = df.columns.str.strip()
        
        # Standardize column names
        df = self._standardize_columns(df)
        
        # Clean and validate data
        df = self._clean_data(df)
        
        return df
    
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Map various column names to standardized names
        """
        new_columns = {}
        used_standard_names = set()
        
        for col in df.columns:
            col_lower = col.lower().strip()
            mapped = False
            
            # Try to find matching standard column
            for standard_name, variations in self.column_mappings.items():
                if col_lower in variations:
                    # Avoid duplicate column names
                    if standard_name in used_standard_names:
                        # If standard name already used, keep original with suffix
                        new_columns[col] = f"{col}_original"
                    else:
                        new_columns[col] = standard_name
                        used_standard_names.add(standard_name)
                    mapped = True
                    break
            
            # Keep original if no mapping found
            if not mapped:
                new_columns[col] = col.lower()
        
        df = df.rename(columns=new_columns)
        
        return df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize data values
        """
        # Remove completely empty rows
        df = df.dropna(how='all')
        
        # Clean price fields
        if 'price' in df.columns:
            df['price'] = df['price'].astype(str).str.replace('$', '').str.replace(',', '').str.strip()
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
        
        # Clean quantity fields
        if 'quantity' in df.columns:
            df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0).astype(int)
        
        # Clean weight fields
        if 'weight' in df.columns:
            df['weight'] = df['weight'].astype(str).str.replace('lbs', '').str.replace('lb', '').str.strip()
            df['weight'] = pd.to_numeric(df['weight'], errors='coerce')
        
        # Strip whitespace from string columns
        for col in df.columns:
            if pd.api.types.is_object_dtype(df[col]):
                df[col] = df[col].astype(str).str.strip()
                # Replace 'nan' strings with empty strings
                df[col] = df[col].replace(['nan', 'None', 'NaN', 'null'], '')
        
        return df

