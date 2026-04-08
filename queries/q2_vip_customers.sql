/* Query 2: Finding VIP and Less Engaged Customers.
This identifies which customers drive the most profit.
*/

SELECT o.customerNumber, SUM(od.quantityOrdered * (od.priceEach - p.buyPrice)) AS total_profit
FROM orders o
JOIN orderdetails od ON o.orderNumber = od.orderNumber
JOIN products p ON od.productCode = p.productCode
GROUP BY o.customerNumber
ORDER BY total_profit DESC;