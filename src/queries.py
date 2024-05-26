"Queries to be used during the import process"

DELETE_ROWS = """
DELETE FROM {table}
WHERE {where_condition}
"""

FULL_DF = """
SELECT * 
FROM bcra_final
"""

INSERT_ROWS = """
INSERT INTO {target_table}
SELECT * 
FROM {source_table} 
ORDER BY fecha
"""

MIN_DATE = """
SELECT 
    MIN(fecha) AS min_date
FROM {table}
"""

LAST_AVAILABLE_VALUE = """
SELECT
    fecha as date
    , valor AS last_value
FROM bcra_final
WHERE variable = '{variable}'
AND valor IS NOT NULL
ORDER BY fecha DESC
LIMIT 1
"""
