--   ======================================================================================
--    AUTOGENERATED!!!! DO NOT EDIT!!!!
--   ======================================================================================

INSERT INTO dv.sale_line_main_s
SELECT
  sale_line_key
  ,max(load_dts) AS load_dts
  ,effective_ts
  ,item_cost
  ,item_quantity
  ,rec_src
FROM (
  
  SELECT
    sales_line_id AS sale_line_key
    ,current_timestamp() AS load_dts
    ,date AS effective_ts
    ,price AS item_cost
    ,quantity AS item_quantity
    ,'datalake.sales_line' AS rec_src
  FROM
    datalake.sales_line
  WHERE
    {{start_ts}} <= current_timestamp()
    AND current_timestamp() < {{end_ts}}
)
q
WHERE
  NOT EXISTS (
    SELECT 1
    FROM dv.sale_line_main_s t
    WHERE t.sale_line_key = q.sale_line_key
      AND t.effective_ts = q.effective_ts
      AND t.item_cost = q.item_cost
      AND t.item_quantity = q.item_quantity
  )
GROUP BY
  sale_line_key
  ,effective_ts
  ,item_cost
  ,item_quantity
  ,rec_src;