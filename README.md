# CSV Data Extraction API

This API extracts data from CSV files based on a column mapping configuration.

## Setup

1. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the API:
   ```
   python app.py
   ```

The API will be available at `http://localhost:8000`.

## API Usage

### Extract Data Endpoint

**URL**: `/extract`
**Method**: `POST`
**Content-Type**: `application/json`

**Request Body**:
```json
{
  "excel_url": "https://example.com/path/to/your.csv",
  "excel_headers": [
    {
      "header": "Item No.",
      "selected": "bc_item_number"
    },
    {
      "header": "Description of Goods",
      "selected": "product_simple_description"
    },
    {
      "header": "Product size",
      "selected": "",
      "sub_header1": "(CM)",
      "selected1": "height"
    },
    {
      "header": "Measurement(cm)-1",
      "selected": "",
      "sub_header1": "L",
      "selected1": "cLength",
      "sub_header2": "W",
      "selected2": "cWidth",
      "sub_header3": "H",
      "selected3": "cHeight"
    }
  ]
}
```

**Response**:
```json
[
  {
    "bc_item_number": "123",
    "product_simple_description": "Example product",
    "height": "10",
    "cLength": "20",
    "cWidth": "15",
    "cHeight": "5"
  },
  {
    "bc_item_number": "456",
    "product_simple_description": "Another product",
    "height": "12",
    "cLength": "25",
    "cWidth": "18",
    "cHeight": "8"
  }
]
```

## API Documentation

After starting the server, you can access the Swagger UI documentation at:

```
http://localhost:8000/docs
```

This provides an interactive interface for testing the API. 