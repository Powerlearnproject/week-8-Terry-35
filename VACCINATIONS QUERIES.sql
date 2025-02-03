USE VACCINATIONS;

-- Retrieve all vaccination records for a specific community (e.g., Greenfield)
SELECT 
    C.name, D.age_group, V.vaccine_name, R.date_administered, R.doses_administered
FROM 
    Vaccination_Record R
    JOIN Community C ON R.community_id = C.community_id
    JOIN Demographic D ON R.demographic_id = D.demographic_id
    JOIN Vaccination_Type V ON R.vaccine_id = V.vaccine_id
WHERE 
    C.name = 'Greenfield';

-- Summarize total doses administered per vaccination type
SELECT 
    V.vaccine_name,
    SUM(R.doses_administered) AS total_doses
FROM 
    Vaccination_Record R
    JOIN Vaccination_Type V ON R.vaccine_id = V.vaccine_id
GROUP BY 
    V.vaccine_name;
    
    -- Find vaccination trends over time (grouped by month)
    SELECT 
    DATE_FORMAT(date_administered, '%Y-%m') AS month,
    SUM(doses_administered) AS total_doses
FROM 
    Vaccination_Record
GROUP BY 
    DATE_FORMAT(date_administered, '%Y-%m')
ORDER BY 
    month;
    
    -- Identify communities with vaccination rates lower than a defined threshold (assume threshold doses per population)
    SELECT 
    C.name, 
    SUM(R.doses_administered) AS total_doses, 
    C.population,
    (SUM(R.doses_administered) / C.population * 100) AS vaccination_rate_percentage
FROM 
    Vaccination_Record R
    JOIN Community C ON R.community_id = C.community_id
GROUP BY 
    C.name, C.population
HAVING 
    (SUM(R.doses_administered) / C.population * 100) < 50;  -- example threshold
    
    -- Compare vaccination numbers across different demographic groups
    SELECT 
    D.age_group,
    SUM(R.doses_administered) AS total_doses
FROM 
    Vaccination_Record R
    JOIN Demographic D ON R.demographic_id = D.demographic_id
GROUP BY 
    D.age_group;