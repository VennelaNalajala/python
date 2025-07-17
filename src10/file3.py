import pandas as pd
from connection import sqlserver

engine = sqlserver()

sales_dimensions = pd.read_sql("SELECT * FROM sales_dimensions", con=engine)

supplier_details = sales_dimensions[['supplier_id', 'supplier_name', 'contact_email','supplier_country','reliability_score']].drop_duplicates()
region_details = sales_dimensions[['region_id', 'region_name', 'region_country','regional_manager']].drop_duplicates()
promotion_details = sales_dimensions[['promotion_id', 'promotion_name', 'discount_percentage','start_date','end_date']].drop_duplicates()

supplier_details.to_sql('supplier_details', con=engine, if_exists='replace', index=False)
region_details.to_sql('region_details', con=engine, if_exists='replace', index=False)
promotion_details.to_sql('promotion_details', con=engine, if_exists='replace', index=False)

print(" Dimension tables created successfully.")
