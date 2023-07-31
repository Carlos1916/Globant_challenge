from django.db import connection


quarter_query = """
    SELECT
        cd.department,
        cj.job,
        SUM(CASE WHEN EXTRACT(QUARTER FROM TO_DATE(ch.datetime, 'YYYY-MM-DD"T"HH24:MI:SS')) = 1 THEN 1 ELSE 0 END) AS Q1,
        SUM(CASE WHEN EXTRACT(QUARTER FROM TO_DATE(ch.datetime, 'YYYY-MM-DD"T"HH24:MI:SS')) = 2 THEN 1 ELSE 0 END) AS Q2,
        SUM(CASE WHEN EXTRACT(QUARTER FROM TO_DATE(ch.datetime, 'YYYY-MM-DD"T"HH24:MI:SS')) = 3 THEN 1 ELSE 0 END) AS Q3,
        SUM(CASE WHEN EXTRACT(QUARTER FROM TO_DATE(ch.datetime, 'YYYY-MM-DD"T"HH24:MI:SS')) = 4 THEN 1 ELSE 0 END) AS Q4
    FROM
        core_hiredemployee ch
        INNER JOIN core_department cd ON ch.department_id = cd.id
        INNER JOIN core_job cj ON ch.job_id = cj.id
    WHERE 
        TO_DATE(datetime, 'YYYY-MM-DD"T"HH24:MI:SS') >= '2021-01-01'
        AND TO_DATE(datetime, 'YYYY-MM-DD"T"HH24:MI:SS') < '2022-01-01'
    GROUP BY
        1, 2
    ORDER BY 
        1, 2
"""


department_query = """
WITH department_stats AS (
  SELECT
    department_id,
    COUNT(*) AS num_hired
  FROM
    core_hiredemployee
  WHERE
    EXTRACT(YEAR FROM TO_DATE(datetime, 'YYYY-MM-DD"T"HH24:MI:SS')) = 2021
  GROUP BY
    1
),
mean_hired AS (
  SELECT
    AVG(num_hired) AS mean_num_hired
  FROM
    department_stats
)
SELECT
  cd._id AS id,
  cd.department AS department,
  ds.num_hired AS hired
FROM
  department_stats ds
JOIN
  core_department cd ON ds.department_id = cd.id
JOIN
  mean_hired mh ON ds.num_hired > mh.mean_num_hired
ORDER BY
  ds.num_hired DESC;
"""


def run_sql_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

