import pytesseract
from PIL import Image
import pandas as pd
import sqlalchemy as sa
import json
import xml.etree.ElementTree as ET

class DataProcessor:
    def __init__(self):
        self.engine = sa.create_engine('sqlite:///jarvis_data.db')

    def process_text(self, text):
        # Implement NLP to extract numerical data
        # For simplicity, let's assume it extracts key-value pairs
        data = {'value1': 10, 'value2': 20}  # Placeholder
        return self._store_data(data)

    def process_image(self, image_path):
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        # Process the extracted text similar to process_text
        data = {'value1': 30, 'value2': 40}  # Placeholder
        return self._store_data(data)

    def process_structured_data(self, data, format_type):
        if format_type == 'csv':
            df = pd.read_csv(data)
        elif format_type == 'json':
            df = pd.read_json(data)
        elif format_type == 'xml':
            root = ET.fromstring(data)
            # Convert XML to DataFrame (simplified)
            df = pd.DataFrame([elem.attrib for elem in root.iter()])
        else:
            raise ValueError(f"Unsupported format: {format_type}")

        return self._store_data(df)

    def _store_data(self, data):
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        elif isinstance(data, pd.DataFrame):
            df = data
        else:
            raise ValueError("Unsupported data type")

        table_name = f"data_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"
        df.to_sql(table_name, self.engine, if_exists='replace', index=False)
        return table_name

    def query_data(self, table_name, query):
        with self.engine.connect() as conn:
            result = conn.execute(sa.text(query))
            return pd.DataFrame(result.fetchall(), columns=result.keys())