import pandas as pd
from llama_index.query_engine import PandasQueryEngine

class CalculationService:
    def __init__(self):
        self.data = pd.DataFrame()  # Initialize with empty DataFrame

    def load_data(self, data_source):
        # Load data from various sources (CSV, Excel, etc.)
        if data_source.endswith('.csv'):
            self.data = pd.read_csv(data_source)
        elif data_source.endswith('.xlsx'):
            self.data = pd.read_excel(data_source)
        # Add more data source types as needed

    async def execute(self, query):
        try:
            query_engine = PandasQueryEngine(self.data)
            response = query_engine.query(query)
            return str(response)
        except Exception as e:
            return f"Error in calculation: {str(e)}"

calculation_service = CalculationService()