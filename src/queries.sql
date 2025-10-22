-- =============================
-- Department KPI summary
-- =============================
CREATE TEMP VIEW IF NOT EXISTS department_kpis AS
SELECT
  department,
  ROUND(AVG(rating), 2)           AS avg_rating,
  ROUND(AVG(tasks_completed), 2)  AS avg_tasks,
  ROUND(SUM(hours_worked), 2)     AS total_hours,
  SUM(tasks_completed)            AS total_tasks,
  ROUND(AVG(CASE WHEN absences = 1 THEN 1.0 ELSE 0.0 END), 4) AS absence_rate
FROM employees
GROUP BY department;

-- =============================
-- Employee summary across period
-- =============================
CREATE TEMP VIEW IF NOT EXISTS employee_summary AS
SELECT
  employee_id,
  name,
  department,
  role,
  SUM(tasks_completed)                                AS tasks_total,
  ROUND(SUM(hours_worked), 2)                         AS hours_total,
  ROUND(AVG(rating), 2)                               AS avg_rating,
  SUM(projects)                                       AS projects_total,
  SUM(absences)                                       AS absences_total,
  ROUND(SUM(tasks_completed) / NULLIF(SUM(hours_worked), 0), 2) AS tasks_per_hour
FROM employees
GROUP BY employee_id, name, department, role;

-- =============================
-- Daily productivity (per-row)
-- =============================
CREATE TEMP VIEW IF NOT EXISTS daily_productivity AS
SELECT
  date,
  employee_id,
  department,
  tasks_completed,
  hours_worked,
  CASE
    WHEN hours_worked > 0 THEN tasks_completed * 1.0 / hours_worked
    ELSE 0
  END AS tasks_per_hour
FROM employees;

-- Final SELECTs consumed by analyze_performance.py
SELECT * FROM department_kpis ORDER BY avg_rating DESC;
SELECT * FROM employee_summary ORDER BY tasks_per_hour DESC;
SELECT * FROM daily_productivity;
