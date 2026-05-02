SELECT 
    Customer_Segment, 
    Region, 
    SUM(Revenue) AS Total_Revenue, 
    SUM(Profit) AS Total_Profit,
    ROUND(AVG(Profit_Margin) * 100, 2) AS Avg_Margin_Percent
FROM sales
GROUP BY Customer_Segment, Region
ORDER BY Total_Profit DESC;

SELECT 
    Discount_Percent,
    COUNT(Order_ID) AS Number_of_Orders,
    ROUND(AVG(Revenue), 2) AS Avg_Order_Value,
    ROUND(AVG(Profit_Margin) * 100, 2) AS Avg_Margin_Percent
FROM sales
GROUP BY Discount_Percent
ORDER BY Discount_Percent ASC;