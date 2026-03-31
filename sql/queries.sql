-- Taxa geral de churn
SELECT
COUNT(*) AS total_clientes,
SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churn_clientes,
ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate
FROM churn;

-- Churn por tipo de contrato
SELECT
Contract,
COUNT(*) AS total,
SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churn,
ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate
FROM churn
GROUP BY Contract
ORDER BY churn_rate DESC;

-- Média de cobrança por churn
SELECT
Churn,
AVG(MonthlyCharges) AS avg_monthly_charge,
AVG(TotalCharges) AS avg_total_charge
FROM churn
GROUP BY Churn;

-- Tempo médio de permanência
SELECT
Churn,
AVG(tenure) AS avg_tenure
FROM churn
GROUP BY Churn;

-- Clientes com maior risco (baixo tempo + alto custo)
SELECT *
FROM churn
WHERE tenure < 12
AND MonthlyCharges > 70
AND Churn = 'Yes';
