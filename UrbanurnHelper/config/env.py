config = {
    'USERNAME': '<superuser_username>',
    'PASSWORD': '<superuser_password>',
    'BASE_URL': r'http://localhost:9090',
    'PRODUCT_KEYS': ['sku_guid', 'name', 'description', 'product_data', 'is_fragile', 'price', 'business_guid'],
    'SKU_PARENT_KEYS': ['name', 'description', 'category'],
    'SKU_CHILD_KEYS': ['name', 'description', 'parent_sku_guid'],
    'PRODUCT_IMAGES': r'C:\Users\KH2021\Google Drive\Urban Urn\Images'
}

excel_config = {
    'PRODUCT_EXCEL': r'C:\Users\KH2021\Google Drive\Urban Urn\Products_table.xlsx',
    'SKU_PARENT_EXCEL': r'C:\Users\KH2021\Google Drive\Urban Urn\sku_parent.xlsx',
    'SKU_CHILD_EXCEL': r'C:\Users\KH2021\Google Drive\Urban Urn\sku_child.xlsx'
}
