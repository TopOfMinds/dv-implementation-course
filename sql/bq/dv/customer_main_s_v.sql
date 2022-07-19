--   ======================================================================================
--    AUTOGENERATED!!!! DO NOT EDIT!!!!
--   ======================================================================================

DROP VIEW IF EXISTS dv.customer_main_s;

CREATE VIEW dv.customer_main_s
AS
SELECT
  customer_key
  ,max(load_dts) AS load_dts
  ,effective_ts
  ,first_name
  ,last_name
  ,email_address
  ,home_phone
  ,rec_src
FROM (
  
  SELECT
    customer_id AS customer_key
    ,current_timestamp() AS load_dts
    ,date AS effective_ts
    ,first_name AS first_name
    ,last_name AS last_name
    ,email AS email_address
    ,cell_number AS home_phone
    ,'datalake.customer' AS rec_src
  FROM
    datalake.customer
)
GROUP BY
  customer_key
  ,effective_ts
  ,first_name
  ,last_name
  ,email_address
  ,home_phone
  ,rec_src;