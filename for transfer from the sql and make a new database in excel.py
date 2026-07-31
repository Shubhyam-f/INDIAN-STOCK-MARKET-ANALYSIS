import sqlite3
import pandas as pd

# 1. Connect to your database
conn = sqlite3.connect('indian_stocks.db')

# 2. Extract your 5 queries into DataFrames
df_max_var = pd.read_sql_query("""
    SELECT ticker, ROUND(high - low, 2) AS Jump, date
    FROM stock_prices
    ORDER BY ticker ASC, Jump DESC;
""", conn)

df_returns = pd.read_sql_query("""
    WITH earliest_data AS (
        SELECT ticker, MIN("date") AS Earliest_date, ROUND(close, 2) AS Earliest_close
        FROM stock_prices GROUP BY ticker
    ),
    latest_data AS (
        SELECT ticker, MAX("date") AS Latest_date, ROUND(close, 2) AS Latest_close
        FROM stock_prices GROUP BY ticker
    ),
    main_portion AS (
        SELECT e.Earliest_date || ' to ' || l.Latest_date AS Time_period,
               e.Earliest_close, l.Latest_close,
               (l.Latest_close - e.Earliest_close) AS Return_on_investment,
               l.ticker
        FROM latest_data l INNER JOIN earliest_data e ON e.ticker = l.ticker
    ),
    percentage_ranks AS (
        SELECT Time_period, Earliest_close, Latest_close, Return_on_investment,
               ROUND(((Return_on_investment / Earliest_close) * 100), 2) AS Percentage_return,
               ticker
        FROM main_portion
    )
    SELECT ROW_NUMBER() OVER(ORDER BY pr.Percentage_return DESC) AS company_rank,
           pr.ticker, pr.Time_period, pr.Earliest_close, pr.Latest_close,
           pr.Return_on_investment, pr.Percentage_return
    FROM percentage_ranks pr ORDER BY pr.Percentage_return DESC;
""", conn)

df_volume = pd.read_sql_query("""
    WITH average_volume_cte AS ( 
        SELECT ticker, ROUND(AVG(volume), 2) AS average_volume
        FROM stock_prices GROUP BY ticker
    )
    SELECT av.ticker, s.volume, ROUND(s.open, 2) AS open, ROUND(s.low, 2) AS low,
           ROUND(s.high, 2) AS high, ROUND(s.close, 2) AS close, s.date
    FROM average_volume_cte av
    INNER JOIN stock_prices s ON av.ticker = s.ticker
    WHERE s.volume > av.average_volume
    ORDER BY av.ticker ASC, s.volume DESC;
""", conn)

df_sectors = pd.read_sql_query("""
    WITH sectors AS (
        SELECT DISTINCT ticker,
            CASE ticker
                WHEN 'RELIANCE.NS' THEN 'ENERGY'
                WHEN 'TCS.NS' THEN 'IT'
                WHEN 'INFY.NS' THEN 'IT'
                ELSE 'BANKING'  
            END AS sector_name
        FROM stock_prices
    ),
    earliest_data AS (
        SELECT ticker, MIN("date") AS Earliest_date, ROUND(close, 2) AS Earliest_close
        FROM stock_prices GROUP BY ticker
    ),
    latest_data AS (
        SELECT ticker, MAX("date") AS Latest_date, ROUND(close, 2) AS Latest_close
        FROM stock_prices GROUP BY ticker
    ),
    main_portion AS (
        SELECT e.Earliest_date || ' to ' || l.Latest_date AS Time_period,
               e.Earliest_close, l.Latest_close,
               (l.Latest_close - e.Earliest_close) AS Return_on_investment,
               l.ticker
        FROM latest_data l INNER JOIN earliest_data e ON e.ticker = l.ticker
    ),
    percentage_ranks AS (
        SELECT Time_period, Earliest_close, Latest_close, Return_on_investment,
               ROUND(((Return_on_investment / Earliest_close) * 100), 2) AS Percentage_return,
               ticker
        FROM main_portion
    )
    SELECT ROW_NUMBER() OVER(ORDER BY pr.Percentage_return DESC) AS Company_rank,
           pr.ticker AS INDUSTRY, sc.sector_name AS SECTOR,
           pr.Time_period, pr.Earliest_close, pr.Latest_close,
           pr.Return_on_investment, pr.Percentage_return
    FROM percentage_ranks pr JOIN sectors sc ON sc.ticker = pr.ticker
    ORDER BY pr.Percentage_return DESC;
""", conn)

df_streaks = pd.read_sql_query("""
    WITH stock_data_cte AS (
        SELECT ticker, date, open, high, low, close, volume,
               ROUND(AVG(CAST(volume AS REAL)) OVER(PARTITION BY ticker), 2) AS average_volume,
               LAG(CAST(close AS REAL)) OVER(PARTITION BY ticker ORDER BY date) AS prev_close
        FROM stock_prices
    )
    SELECT ticker, volume,
           ROUND(CAST(open AS REAL), 2) AS open_price,
           ROUND(CAST(low AS REAL), 2) AS low_price,
           ROUND(CAST(high AS REAL), 2) AS high_price,
           ROUND(CAST(close AS REAL), 2) AS close_price,
           date, 'Yes' AS price_hike_over_2_pct
    FROM stock_data_cte
    WHERE CAST(volume AS REAL) > average_volume 
      AND prev_close IS NOT NULL 
      AND ((CAST(close AS REAL) - prev_close) / prev_close) > 0.02
    ORDER BY ticker ASC, CAST(volume AS REAL) DESC;
""", conn)

# 3. Write strictly to a RAW data file (Safe to overwrite anytime!)
with pd.ExcelWriter('raw_stock_data.xlsx', engine='openpyxl') as writer:
    df_max_var.to_excel(writer, sheet_name='Daily_Variation', index=False)
    df_returns.to_excel(writer, sheet_name='1Y_Returns', index=False)
    df_volume.to_excel(writer, sheet_name='Volume_Spikes', index=False)
    df_sectors.to_excel(writer, sheet_name='Sector_Performance', index=False)
    df_streaks.to_excel(writer, sheet_name='Volume_Price_Jump', index=False)

conn.close()
print('Success! raw_stock_data.xlsx updated safely.')
