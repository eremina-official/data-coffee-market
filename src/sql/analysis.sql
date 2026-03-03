-- aggregation view of products count
CREATE VIEW vw_product_count AS
SELECT 
    COUNT(*) AS total_products
FROM products;


-- products count by category
CREATE VIEW vw_product_count_by_category AS
SELECT
	c.name, 
    COUNT(*) AS products_count_by_category
FROM products p
JOIN categories c ON p.category_id = c.id 
GROUP BY category_id;


-- single vs mixed origin view
CREATE VIEW vw_product_count_by_origin_type AS
SELECT
    CASE 
        WHEN origin_count = 0 THEN 'no_origin'
        WHEN origin_count = 1 THEN 'single_origin'
        ELSE 'mixed_origin'
    END AS origin_type,
    COUNT(*) AS product_count
FROM (
    SELECT 
        p.id AS product_id,
        COUNT(DISTINCT pv.label) AS origin_count
    FROM products p
    LEFT JOIN product_parameter_values ppv
        ON p.id = ppv.product_id
    LEFT JOIN parameter_values pv 
        ON ppv.value_id = pv.id AND pv.parameter_id = '247497'
    GROUP BY p.id
) AS product_origins
GROUP BY origin_type;


-- Products by brand view
CREATE VIEW vw_products_by_brand AS
SELECT pv.label as Marka, COUNT(*) as product_count FROM product_parameter_values ppv 
JOIN parameter_values pv ON ppv.value_id = pv.id 
WHERE pv.parameter_id = '248811'
GROUP BY ppv.value_id 
ORDER BY product_count DESC;


-- products count by package size view
CREATE VIEW products_count_by_package_size
WITH categorized AS (
  SELECT
    CASE
      WHEN pv.label NOT IN ('1000 g', '250 g', '500 g', '200 g') THEN 'Other'
      ELSE pv.label
    END AS package_group
  FROM product_parameter_values ppv
  JOIN parameter_values pv
    ON ppv.value_id = pv.id
  WHERE pv.parameter_id = '128453'
)
SELECT
  package_group,
  COUNT(*) AS product_count
FROM categorized
GROUP BY package_group
HAVING COUNT(*) > 1
ORDER BY product_count DESC;


-- single origin products view
CREATE VIEW vw_single_origin_products AS
WITH single_origin_products AS (
    SELECT ppv.product_id
    FROM product_parameter_values ppv
    JOIN parameter_values pv ON ppv.value_id = pv.id
    WHERE pv.parameter_id = '247497'
    GROUP BY ppv.product_id
    HAVING COUNT(*) = 1
)
SELECT
    pv.label,
    COUNT(*) AS product_count
FROM product_parameter_values ppv
JOIN parameter_values pv ON ppv.value_id = pv.id
JOIN single_origin_products sop ON sop.product_id = ppv.product_id
WHERE pv.parameter_id = '247497'
GROUP BY ppv.value_id, pv.label
ORDER BY product_count DESC;


-- countries count in mixed origin products view
-- this shows how often each country appears in products that have multiple countries of origin
CREATE VIEW vw_mixed_origin_products AS
WITH mixed_origin_products AS (
    SELECT ppv.product_id
    FROM product_parameter_values ppv
    JOIN parameter_values pv ON ppv.value_id = pv.id
    WHERE pv.parameter_id = '247497'
    GROUP BY ppv.product_id
    HAVING COUNT(*) > 1
)
SELECT
    pv.label,
    COUNT(*) AS product_count
FROM product_parameter_values ppv
JOIN parameter_values pv ON ppv.value_id = pv.id
JOIN mixed_origin_products mop ON mop.product_id = ppv.product_id
WHERE pv.parameter_id = '247497'
GROUP BY ppv.value_id, pv.label
ORDER BY product_count DESC;

WITH mixed_products_count as (
	SELECT ppv.product_id as id, COUNT(ppv.product_id )
    FROM product_parameter_values ppv
    JOIN parameter_values pv ON ppv.value_id = pv.id
    WHERE pv.parameter_id = '247497'
    GROUP BY ppv.product_id
    HAVING COUNT(ppv.product_id) > 1
)
select count(*) from mixed_products_count;
    
    
-- Roast level view
CREATE VIEW vw_product_count_by_roast_level AS
SELECT pv.label as roast_level, COUNT(*) as product_count FROM product_parameter_values ppv 
JOIN parameter_values pv ON ppv.value_id = pv.id
WHERE pv.parameter_id = '249806'
GROUP BY ppv.value_id;


-- Product type view
CREATE VIEW vw_product_count_by_type AS
WITH categorized AS (
  SELECT 
  	CASE 
  	  WHEN ppv.value_id NOT IN ('249805_1742591', '249805_1742592') THEN 'arabica/robusta'
  	  ELSE pv.label
  	END AS type_group
  FROM product_parameter_values ppv 
  JOIN parameter_values pv ON ppv.value_id = pv.id
  WHERE pv.parameter_id = '249805'
)
SELECT 
  type_group,
  COUNT(*) AS product_count
FROM categorized 
GROUP BY type_group
ORDER BY product_count DESC;


-- caffeine content by country view
CREATE VIEW vw_caffeine_content_by_country AS
SELECT
    caffeine.value_id       AS caffeine_id,
    caffeine_pv.label       AS caffeine_content,
    country.value_id,
    country_pv.label as country_name,
    COUNT(DISTINCT caffeine.product_id) AS product_count,
    COUNT(DISTINCT caffeine.product_id)
        / SUM(COUNT(DISTINCT caffeine.product_id)) OVER (PARTITION BY country_pv.label)
        * 100 AS pct_of_country
FROM product_parameter_values caffeine
JOIN parameter_values caffeine_pv
    ON caffeine.value_id = caffeine_pv.id
   AND caffeine_pv.parameter_id = '249807'
   AND caffeine_pv.id <> '249807_1743993'  -- filter out products without caffeine
JOIN product_parameter_values country
    ON caffeine.product_id = country.product_id
JOIN parameter_values country_pv
    ON country.value_id = country_pv.id
   AND country_pv.parameter_id = '247497'
GROUP BY
    caffeine.value_id,
    caffeine_pv.label,
    country.value_id,
    country_pv.label
ORDER BY country_name, caffeine_content;


-- intensywnosc smaku (body) by country
CREATE VIEW vw_body_by_country AS
SELECT
    caffeine.value_id       AS caffeine_id,
    caffeine_pv.label       AS caffeine_content,
    country.value_id,
    country_pv.label as country_name,
    COUNT(DISTINCT caffeine.product_id) AS product_count,
    COUNT(DISTINCT caffeine.product_id)
        / SUM(COUNT(DISTINCT caffeine.product_id)) OVER (PARTITION BY country_pv.label)
        * 100 AS pct_of_country
FROM product_parameter_values caffeine
JOIN parameter_values caffeine_pv
    ON caffeine.value_id = caffeine_pv.id
   AND caffeine_pv.parameter_id = '249810'
   AND caffeine_pv.id <> '249807_1743993'  -- filter out products without caffeine
JOIN product_parameter_values country
    ON caffeine.product_id = country.product_id
JOIN parameter_values country_pv
    ON country.value_id = country_pv.id
   AND country_pv.parameter_id = '247497'
GROUP BY
    caffeine.value_id,
    caffeine_pv.label,
    country.value_id,
    country_pv.label
ORDER BY country_name, caffeine_content;


-- acidity content by country
CREATE VIEW vw_acidity_by_country AS
SELECT
    acidity.value_id       AS acidity_id,
    acidity_pv.label       AS acidity_level,
    country.value_id,
    country_pv.label as country_name,
    COUNT(DISTINCT acidity.product_id) AS product_count,
    COUNT(DISTINCT acidity.product_id)
        / SUM(COUNT(DISTINCT acidity.product_id)) OVER (PARTITION BY country_pv.label)
        * 100 AS pct_of_country
FROM product_parameter_values acidity
JOIN parameter_values acidity_pv
    ON acidity.value_id = acidity_pv.id
   AND acidity_pv.parameter_id = '249808'
   AND acidity_pv.id <> '249807_1743993'  -- filter out products without caffeine
JOIN product_parameter_values country
    ON acidity.product_id = country.product_id
JOIN parameter_values country_pv
    ON country.value_id = country_pv.id
   AND country_pv.parameter_id = '247497'
GROUP BY
    acidity.value_id,
    acidity_pv.label,
    country.value_id,
    country_pv.label
ORDER BY country_name, acidity_level;


-- queries to verify data correctness:
-- single origin products sum from vsop view should be equal to that in vw_product_count_by_origin_type
select sum(product_count) from vw_single_origin_products vsop 


-- mixed origin products sum should be equal to that in vw_product_count_by_origin_type
WITH mixed_products_count as (
	SELECT ppv.product_id as id, COUNT(ppv.product_id )
    FROM product_parameter_values ppv
    JOIN parameter_values pv ON ppv.value_id = pv.id
    WHERE pv.parameter_id = '247497'
    GROUP BY ppv.product_id
    HAVING COUNT(ppv.product_id) > 1
)
select count(*) from mixed_products_count;












