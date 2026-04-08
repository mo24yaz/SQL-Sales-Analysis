/* Query 1: Which products should we order more of or less of?
Look for products with a high stock-to-sales ratio (Low Stock) 
and high product performance (Revenue).
*/

WITH low_stock_table AS (
	SELECT productCode, 
					  ROUND(SUM(quantityOrdered) * 1.0 / (SELECT quantityInStock 
																									 FROM products p 
																									 WHERE p.productCode = od.productCode), 2) AS low_stock
	FROM orderdetails od
	GROUP BY productCode
	ORDER BY low_stock DESC
	LIMIT 10
),

product_performance AS (
	SELECT productCode, SUM(quantityOrdered * priceEach) AS revenue
	FROM orderdetails
	GROUP BY productCode
)

SELECT ls.productCode, p.productName, p.productLine, ls.low_stock, pp.revenue
FROM low_stock_table ls
JOIN product_performance pp ON ls.productCode = pp.productCode
JOIN products p ON ls.productCode = p.productCode
ORDER BY ls.low_stock DESC;