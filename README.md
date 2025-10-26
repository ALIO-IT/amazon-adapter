# Amazon Auto Parts Adapter 🚗

A FastAPI web application that converts AutoZone-style auto parts CSV files into Amazon's upload format for listing products on Amazon.com.

## Features

- 🚀 **Fast & Modern**: Built with FastAPI for high performance
- 📊 **Flexible CSV Parsing**: Automatically detects and maps various column formats
- 🎨 **Beautiful Web Interface**: Drag-and-drop file upload with real-time progress
- 🔄 **Smart Data Transformation**: Converts auto parts data to Amazon's required format
- 📦 **Ready to Upload**: Generates Amazon-compatible CSV files
- 🏷️ **Auto Parts Optimized**: Handles fitment data (Year, Make, Model)

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ALIO-IT/amazon-adapter.git
cd amazon-adapter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

Start the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open your browser and navigate to: `http://localhost:8000`

## Usage

### Web Interface

1. Open the web interface at `http://localhost:8000`
2. Drag and drop your CSV file or click to browse
3. Click "Convert to Amazon Format"
4. Download the converted Amazon-ready CSV file

### API Endpoints

#### Convert CSV
```bash
POST /convert
Content-Type: multipart/form-data
Body: file (CSV file)

Response:
{
  "message": "File converted successfully",
  "output_file": "amazon_auto_parts_20231026_143022.csv",
  "rows_processed": 100,
  "rows_output": 100
}
```

#### Download Converted File
```bash
GET /download/{filename}
```

#### Health Check
```bash
GET /health
```

## Input CSV Format

The application supports flexible CSV formats. It will automatically detect and map common column names:

### Supported Column Names

| Data Type | Accepted Column Names |
|-----------|----------------------|
| **Part Number** | part number, part_number, sku, item number, part#, product_id |
| **Description** | description, title, product name, name, item description |
| **Brand** | brand, manufacturer, make, mfr, vendor |
| **Price** | price, unit price, cost, msrp, retail_price |
| **Quantity** | quantity, qty, stock, inventory, available |
| **Category** | category, type, product_type, classification |
| **UPC** | upc, barcode, ean, gtin |
| **Weight** | weight, item_weight, shipping_weight |
| **Dimensions** | length, width, height (with variations) |
| **Vehicle Fitment** | year, make, model (with variations) |
| **Condition** | condition, item_condition |

### Sample Input CSV

See `sample_autozone.csv` for an example:

```csv
Part Number,Description,Brand,Price,Quantity,Category,UPC,Weight,Year,Make,Model,Condition
BRK-001,Brake Pad Set - Ceramic Front,AutoZone,45.99,25,Brakes,012345678901,3.5,2020,Toyota,Camry,New
FLT-234,Engine Air Filter,K&N,24.99,50,Filters,012345678902,0.8,2018,Honda,Civic,New
```

## Output Format

The application generates a CSV file compatible with Amazon's auto parts template including:

- `product-id` (SKU or UPC)
- `product-id-type` (SKU, UPC, EAN)
- `item-name` (Product title)
- `brand-name`
- `manufacturer`
- `product-description`
- `item-type`
- `standard-price`
- `list-price`
- `quantity`
- `condition-type`
- `part-number`
- `item-weight`
- `item-dimensions` (length, width, height)
- `fitment-year`, `fitment-make`, `fitment-model` (when available)

## Project Structure

```
amazon-adapter/
├── main.py                 # FastAPI application
├── adapter/
│   ├── __init__.py
│   ├── csv_parser.py       # CSV parsing logic
│   └── amazon_transformer.py  # Amazon format transformation
├── uploads/                # Temporary upload directory
├── outputs/                # Generated Amazon CSV files
├── requirements.txt        # Python dependencies
├── sample_autozone.csv     # Sample input file
└── README.md
```

## Technologies

- **FastAPI**: Modern, fast web framework
- **Pandas**: Data manipulation and CSV processing
- **Uvicorn**: ASGI server
- **Python 3.8+**: Programming language

## Development

### Testing

You can test the API using curl:

```bash
curl -X POST "http://localhost:8000/convert" \
  -F "file=@sample_autozone.csv"
```

### Adding Custom Mappings

Edit `adapter/csv_parser.py` to add custom column mappings:

```python
self.column_mappings = {
    'part_number': ['your_custom_column_name', ...],
    ...
}
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on GitHub.
