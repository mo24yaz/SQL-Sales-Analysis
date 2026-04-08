/* Query 3: Average Customer Lifetime Value (LTV).
Total Profit / Total Number of Customers.
*/

WITH customer_profit_table AS (
	SELECT o.customerNumber, SUM(od.quantityOrdered * (od.priceEach - p.buyPrice)) AS profit
	FROM orders o
	JOIN orderdetails od ON o.orderNumber = od.orderNumber
	JOIN products p ON od.productCode = p.productCode
	GROUP BY o.customerNumber
)

SELECT AVG(profit) AS ltv
FROM customer_profit_table;