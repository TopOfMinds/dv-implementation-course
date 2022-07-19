--   ======================================================================================
--    AUTOGENERATED!!!! DO NOT EDIT!!!!
--   ======================================================================================

DROP VIEW IF EXISTS dv.sale_line_main_s;

CREATE VIEW dv.sale_line_main_s
AS
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
)
GROUP BY
  sale_line_key
  ,effective_ts
  ,item_cost
  ,item_quantity
  ,rec_src;