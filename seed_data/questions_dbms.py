"""
DBMS / SQL interview questions for PlaceRight.
Uses compact template expansion to generate ~500 questions.
"""

from typing import List, Dict


def _make_q(topic: str, difficulty: str, level: str, text: str,
            follow_ups: List[str], points: List[str],
            company: str = "", tags: List[str] = None) -> Dict:
    rubric = {
        "1-3": "Cannot explain the concept or write basic syntax. No understanding of underlying theory.",
        "4-5": "Knows the keyword/concept name but gives incomplete or partially incorrect explanation. Cannot apply to a real scenario.",
        "6-7": "Explains correctly with a working example. Minor gaps in edge-case handling or optimization awareness.",
        "8-10": "Deep understanding with correct syntax, edge-case handling, performance implications, and real-world trade-offs.",
    }
    return {
        "domain": "dbms", "topic": topic, "difficulty": difficulty,
        "level": level, "question_text": text, "follow_ups": follow_ups,
        "expected_points": points, "scoring_rubric": rubric,
        "company_specific": company, "tags": tags or [topic],
    }


# ── Default follow-ups & points for compact entries ──
_FU_SQL = ["Can you write the query for that?", "What happens if there are NULL values?"]
_FU_THEORY = ["Can you explain with a real-world example?", "What are the trade-offs?"]
_FU_OPT = ["How would you optimize this for a large table?", "What does the execution plan look like?"]
_PT_SQL = ["Correct syntax", "Handles NULLs / edge cases", "Performance awareness"]
_PT_THEORY = ["Clear definition", "Real-world example", "Trade-off awareness"]
_PT_OPT = ["Identifies bottleneck", "Proposes index or rewrite", "Understands execution plan"]


def get_dbms_questions() -> List[Dict]:
    Q: List[Dict] = []

    # ====================================================================
    # SQL BASICS (60)
    # ====================================================================

    sql_basics_detailed = [
        ("Write a query to find employees whose salary is above the company average.",
         "easy",
         ["What if two employees have the same salary?", "Can you do this without a subquery?"],
         ["Subquery in WHERE", "Comparison operator", "Handles ties"]),

        ("How would you retrieve all unique department names from an employees table?",
         "easy",
         ["What is the difference between DISTINCT and GROUP BY for this?", "Which one is faster?"],
         ["DISTINCT keyword", "GROUP BY alternative", "Performance comparison"]),

        ("Write a query to display the top 5 highest-paid employees.",
         "easy",
         ["What if there are ties at the 5th position?", "How does this differ across MySQL, PostgreSQL, and Oracle?"],
         ["LIMIT / TOP / FETCH FIRST", "ORDER BY DESC", "Tie handling with RANK"]),

        ("Explain the difference between WHERE and HAVING with an example.",
         "easy",
         ["Can you use HAVING without GROUP BY?", "Which is evaluated first?"],
         ["WHERE filters rows", "HAVING filters groups", "Execution order"]),

        ("Write a query to count the number of employees in each department, showing only departments with more than 10 employees.",
         "easy",
         ["What if you also want to filter by location before grouping?", "Can you add the average salary too?"],
         ["GROUP BY", "HAVING COUNT(*) > 10", "Aggregate functions"]),

        ("What does the ORDER BY clause do, and can you sort by multiple columns?",
         "easy",
         ["What is the default sort order?", "Can you ORDER BY a column not in the SELECT list?"],
         ["Ascending/descending", "Multi-column sort precedence", "NULL ordering"]),

        ("Write a query using CASE WHEN to categorize employees as 'Junior', 'Mid', or 'Senior' based on years of experience.",
         "medium",
         ["Where else can you use CASE — in ORDER BY, GROUP BY?", "What is the difference between simple CASE and searched CASE?"],
         ["CASE WHEN syntax", "Multiple conditions", "ELSE clause"]),

        ("How do you select all columns from a table? When should you avoid SELECT *?",
         "easy",
         ["What problems can SELECT * cause in production?", "How does it affect query performance?"],
         ["SELECT * syntax", "Production risks — schema changes", "Network / memory overhead"]),

        ("Write a query to find employees whose name starts with 'A' and ends with 'n'.",
         "easy",
         ["What is the difference between LIKE and ILIKE?", "How do you escape a literal percent sign?"],
         ["LIKE with wildcards", "Pattern matching", "Case sensitivity"]),

        ("Explain what NULL means in SQL. How do you check for NULL?",
         "easy",
         ["Why can't you use = NULL?", "What happens when you add a number to NULL?"],
         ["IS NULL / IS NOT NULL", "Three-valued logic", "COALESCE / IFNULL"]),

        ("Write a query to find the second highest salary in the employees table.",
         "medium",
         ["What if multiple employees share the highest salary?", "Can you solve this with LIMIT OFFSET?"],
         ["Subquery approach", "DENSE_RANK approach", "LIMIT OFFSET approach"]),

        ("What is the difference between UNION and UNION ALL?",
         "easy",
         ["When would you prefer UNION ALL over UNION?", "Can you UNION tables with different column counts?"],
         ["Duplicate elimination", "Performance difference", "Column type compatibility"]),

        ("Write a query to display the current date and time in SQL.",
         "easy",
         ["How do you extract just the year from a date?", "What is the difference between NOW() and CURRENT_TIMESTAMP?"],
         ["Date functions", "Database-specific syntax", "Time zones"]),

        ("How do you rename a column in the output using an alias?",
         "easy",
         ["Can you use an alias in WHERE?", "What about in ORDER BY?"],
         ["AS keyword", "Alias scope in query execution", "Quoted aliases for spaces"]),

        ("Write a query to find all employees who were hired in the last 30 days.",
         "easy",
         ["How do you handle date arithmetic in MySQL vs PostgreSQL?", "What about time zone issues?"],
         ["Date subtraction", "INTERVAL / DATEADD", "Index usage on date columns"]),

        ("What is the difference between DELETE, TRUNCATE, and DROP?",
         "medium",
         ["Can you rollback a TRUNCATE?", "Which one is fastest for removing all rows?"],
         ["DELETE — row by row, logged", "TRUNCATE — deallocate pages", "DROP — removes structure"]),

        ("Write a query to update the salary of all employees in the 'Engineering' department by 10 percent.",
         "easy",
         ["How do you preview which rows will be updated before running UPDATE?", "What if you forget the WHERE clause?"],
         ["UPDATE SET WHERE", "Preview with SELECT", "Transaction safety"]),

        ("Explain the difference between CHAR and VARCHAR data types.",
         "easy",
         ["When would you choose CHAR over VARCHAR?", "What about NVARCHAR?"],
         ["Fixed vs variable length", "Storage difference", "Performance implications"]),

        ("Write a query to insert multiple rows into a table in a single statement.",
         "easy",
         ["What is INSERT INTO ... SELECT?", "How do you handle auto-increment columns?"],
         ["Multi-row INSERT syntax", "INSERT SELECT", "Default values"]),

        ("What is the purpose of the GROUP BY clause? Can you group by multiple columns?",
         "easy",
         ["What happens if you SELECT a non-aggregated column without grouping by it?", "Does the order of columns in GROUP BY matter?"],
         ["Grouping for aggregation", "Multi-column grouping", "SQL standard vs MySQL behavior"]),
    ]

    for text, diff, followups, points in sql_basics_detailed:
        Q.append(_make_q("sql_basics", diff, "fresher", text, followups, points))

    # More sql_basics (compact)
    sql_basics_compact = [
        ("Write a query to find employees with no manager assigned.", "easy"),
        ("How do you limit the number of rows returned by a query?", "easy"),
        ("Write a query to concatenate first name and last name into a single column.", "easy"),
        ("What is the difference between IN and EXISTS?", "medium"),
        ("Write a query to replace NULL values with a default using COALESCE.", "easy"),
        ("How do you find duplicate records in a table?", "medium"),
        ("Write a query to display the length of each employee's name.", "easy"),
        ("What is the difference between COUNT(*), COUNT(column), and COUNT(DISTINCT column)?", "easy"),
        ("Write a query to get the first and last record from a table.", "easy"),
        ("How do you convert a string to uppercase or lowercase in SQL?", "easy"),
        ("Write a query to remove duplicate rows from a result set without using DISTINCT.", "medium"),
        ("What are the different types of SQL commands — DDL, DML, DCL, TCL?", "easy"),
        ("Write a query to find employees whose salary is between 30000 and 60000.", "easy"),
        ("How do you add a new column to an existing table?", "easy"),
        ("Write a query to find the nth highest salary using a correlated subquery.", "hard"),
        ("What is the difference between a primary key and a unique key?", "easy"),
        ("Write a query to swap the values of two columns without a temporary variable.", "medium"),
        ("How do you create a table with a foreign key constraint?", "easy"),
        ("Write a query to find all employees who share the same salary.", "medium"),
        ("What is a composite key? When would you use one?", "easy"),
        ("Write a query to display row numbers alongside query results.", "easy"),
        ("How do you copy data from one table to another?", "easy"),
        ("Write a query to find the department with the highest total salary.", "easy"),
        ("What does the BETWEEN operator do? Is it inclusive?", "easy"),
        ("Write a query to list months where total sales exceeded one lakh.", "medium"),
        ("How do you enforce that a column cannot have NULL values?", "easy"),
        ("Write a query to calculate the running total of sales ordered by date.", "medium"),
        ("What is the difference between a stored procedure and a function?", "medium"),
        ("Write a query to find employees who earn more than their managers.", "medium"),
        ("How do you use the CAST or CONVERT function to change data types?", "easy"),
        ("Write a query to display only odd-numbered rows from a table.", "medium"),
        ("What happens when you divide by zero in SQL? How do you handle it?", "easy"),
        ("Write a query to split a full name column into first name and last name.", "medium"),
        ("How do you create a temporary table? When is it useful?", "easy"),
        ("Write a query to find the most recent order for each customer.", "medium"),
        ("What is the difference between ISNULL, NVL, and COALESCE?", "easy"),
        ("Write a query to generate a comma-separated list of employee names per department.", "medium"),
        ("How do you use the ANY and ALL operators with subqueries?", "medium"),
        ("Write a query to find gaps in a sequence of IDs.", "hard"),
        ("What is a CHECK constraint? Give an example.", "easy"),
    ]

    for text, diff in sql_basics_compact:
        Q.append(_make_q("sql_basics", diff, "fresher", text, _FU_SQL, _PT_SQL))

    # ====================================================================
    # SQL JOINS (50)
    # ====================================================================

    joins_detailed = [
        ("Explain the difference between INNER JOIN and LEFT JOIN with an example.",
         "easy",
         ["When would you choose LEFT JOIN over INNER JOIN?", "What happens to non-matching rows?"],
         ["INNER returns only matches", "LEFT returns all from left table", "NULL padding"]),

        ("Write a query to find all customers who have never placed an order using a LEFT JOIN.",
         "easy",
         ["Can you do this with NOT EXISTS instead?", "Which approach is faster and why?"],
         ["LEFT JOIN with IS NULL", "NOT EXISTS alternative", "Performance comparison"]),

        ("What is a CROSS JOIN? Give a practical use case.",
         "medium",
         ["How many rows does a CROSS JOIN produce?", "When would you actually use this in production?"],
         ["Cartesian product", "Row count = m * n", "Use cases: calendar generation, size/color combos"]),

        ("Write a query to find employees and their managers using a self join.",
         "medium",
         ["How do you handle employees who have no manager?", "Can you display the full management chain?"],
         ["Self join on same table", "LEFT JOIN for no-manager case", "Alias usage"]),

        ("What is the difference between LEFT JOIN and LEFT OUTER JOIN?",
         "easy",
         ["Is there a RIGHT INNER JOIN?", "Why do some databases support only certain outer joins?"],
         ["They are identical", "OUTER is optional keyword", "Standard SQL syntax"]),

        ("Write a query to join three tables: employees, departments, and locations.",
         "medium",
         ["Does the order of joins matter?", "How does the optimizer handle multi-table joins?"],
         ["Chained JOIN syntax", "Join order optimization", "Foreign key relationships"]),

        ("Explain FULL OUTER JOIN. Which databases support it natively?",
         "medium",
         ["How do you simulate a FULL OUTER JOIN in MySQL?", "When do you need one in practice?"],
         ["Returns all rows from both tables", "MySQL workaround with UNION", "Practical scenarios"]),

        ("Write a query using a JOIN to find the department name for each employee.",
         "easy",
         ["What if an employee has no department assigned?", "What if a department has no employees?"],
         ["Basic INNER JOIN", "LEFT JOIN for orphan rows", "Data integrity"]),

        ("What happens when you join on a column that contains NULL values?",
         "medium",
         ["How do you handle this?", "Does NULL = NULL evaluate to TRUE?"],
         ["NULL never equals NULL", "Rows with NULL join keys are excluded", "COALESCE workaround"]),

        ("Write a query to find common records between two tables without using INTERSECT.",
         "medium",
         ["What is the difference between INNER JOIN and INTERSECT?", "Which is more readable?"],
         ["INNER JOIN approach", "Duplicate handling difference", "Set operation vs join"]),
    ]

    for text, diff, followups, points in joins_detailed:
        Q.append(_make_q("sql_joins", diff, "fresher", text, followups, points))

    joins_compact = [
        ("Write a query to display all departments along with the count of employees in each, including departments with zero employees.", "medium"),
        ("How do you join a table to itself to find pairs of employees in the same department?", "medium"),
        ("Write a query using a natural join. Why is it generally discouraged?", "easy"),
        ("What is the USING clause in a JOIN? How does it differ from ON?", "easy"),
        ("Write a query to find all products that have never been ordered using a LEFT JOIN.", "easy"),
        ("How do you perform a join between tables in different schemas or databases?", "medium"),
        ("Write a query to find employees who work in the same department as 'Priya'.", "easy"),
        ("What is a semi join? Can you write one using EXISTS?", "medium"),
        ("Write a query to find the customer who placed the most orders using a JOIN and GROUP BY.", "medium"),
        ("How do you handle many-to-many relationships with a junction table?", "medium"),
        ("Write a query to join employees with their latest performance review.", "hard"),
        ("What is an anti join? How do you express it in SQL?", "medium"),
        ("Write a query to find all students who are enrolled in both 'DBMS' and 'OS' courses.", "medium"),
        ("How do you optimize a slow JOIN query?", "medium"),
        ("Write a query that joins four tables to display order details with customer name, product name, and category.", "hard"),
        ("What is a hash join vs a nested loop join vs a merge join?", "hard"),
        ("Write a query to find managers who manage more than 5 employees using a self join.", "medium"),
        ("How does JOIN performance change with and without indexes on the join columns?", "medium"),
        ("Write a query to get the second most recent order for each customer using a JOIN.", "hard"),
        ("Explain the difference between equi join and non-equi join with examples.", "medium"),
        ("Write a query to find employees whose salary is higher than the average salary of their department using a JOIN.", "medium"),
        ("What is a lateral join or CROSS APPLY? When is it useful?", "hard"),
        ("Write a query to find pairs of products that are frequently bought together.", "hard"),
        ("How do you join a table with a subquery? Give an example.", "medium"),
        ("Write a query to find the most expensive product in each category using a JOIN.", "medium"),
        ("What is the performance impact of joining on non-indexed columns?", "medium"),
        ("Write a query to find all employees who have the same job title and department as another employee.", "medium"),
        ("How do you join tables when the column names are different in each table?", "easy"),
        ("Write a query to find customers who placed orders in every month of 2024.", "hard"),
        ("Explain how the database engine decides the join order when multiple tables are involved.", "hard"),
        ("Write a query to list all teacher-student pairs where the teacher teaches at least one course the student is enrolled in.", "medium"),
        ("How do you perform a conditional join where the join condition depends on a column value?", "hard"),
        ("Write a query to find all orders placed on the same day by different customers.", "medium"),
        ("What is a theta join? How does it differ from a standard equi join?", "medium"),
        ("Write a query to display the salary rank of each employee within their department using a self join.", "hard"),
        ("How do you join a large fact table with a small dimension table efficiently?", "hard"),
        ("Write a query to find all employees who joined on the same date.", "easy"),
        ("What happens if you accidentally omit the ON clause in a JOIN?", "easy"),
        ("Write a query to combine two result sets with different columns into one using a FULL OUTER JOIN.", "hard"),
        ("How do you decide between a subquery and a JOIN for a given problem?", "medium"),
    ]

    for text, diff in joins_compact:
        Q.append(_make_q("sql_joins", diff, "fresher", text, _FU_SQL, _PT_SQL))

    # ====================================================================
    # SQL SUBQUERIES (40)
    # ====================================================================

    subq_detailed = [
        ("What is a correlated subquery? How does it differ from a regular subquery?",
         "medium",
         ["Can you show the execution flow of a correlated subquery?", "Why are they often slower?"],
         ["Depends on outer query", "Executed once per outer row", "Performance implications"]),

        ("Write a query using EXISTS to find departments that have at least one employee earning more than one lakh.",
         "medium",
         ["How does EXISTS differ from IN here?", "Which is more efficient for large datasets?"],
         ["EXISTS returns TRUE/FALSE", "Short-circuit evaluation", "Performance vs IN"]),

        ("Write a query to find employees who earn more than the average salary of their own department using a correlated subquery.",
         "medium",
         ["Can you solve this with a JOIN instead?", "Which approach would you use in production?"],
         ["Correlated subquery syntax", "JOIN alternative", "Readability vs performance"]),

        ("Explain the difference between IN, ANY, and ALL with subqueries.",
         "medium",
         ["When would you use ALL instead of a MAX subquery?", "What happens if the subquery returns NULL?"],
         ["IN matches any value in set", "ANY — at least one match", "ALL — every value must match"]),

        ("Write a query using a subquery in the FROM clause to find the average of department averages.",
         "medium",
         ["What is this type of subquery called?", "Can you use a CTE instead?"],
         ["Derived table / inline view", "Two-level aggregation", "CTE alternative"]),
    ]

    for text, diff, followups, points in subq_detailed:
        Q.append(_make_q("sql_subqueries", diff, "fresher", text, followups, points))

    subq_compact = [
        ("Write a query to find the employee with the highest salary in each department using a subquery.", "medium"),
        ("How do you use a subquery inside an INSERT statement?", "easy"),
        ("Write a query using NOT EXISTS to find customers who have not placed any orders.", "medium"),
        ("What is a scalar subquery? Where can you use it?", "easy"),
        ("Write a query to find products whose price is above the average price of their category.", "medium"),
        ("How do you rewrite a correlated subquery as a JOIN for better performance?", "medium"),
        ("Write a query using IN with a subquery to find employees in departments located in Chennai.", "easy"),
        ("What happens if a subquery used with = returns more than one row?", "easy"),
        ("Write a query to find the top 3 departments by total salary using a subquery.", "medium"),
        ("How do you use a subquery in the SELECT clause?", "easy"),
        ("Write a query to find all employees whose salary is greater than ALL employees in the 'Sales' department.", "medium"),
        ("What is the difference between a subquery and a CTE in terms of readability and performance?", "medium"),
        ("Write a query to find employees who earn the minimum salary in their department.", "medium"),
        ("How do you use a subquery with UPDATE to set values based on another table?", "medium"),
        ("Write a query to find the most recent order for each product using a correlated subquery.", "hard"),
        ("What is a nested subquery? How many levels of nesting are practical?", "medium"),
        ("Write a query to delete all orders placed by customers from a specific city using a subquery.", "medium"),
        ("How do you use EXISTS vs IN when the subquery may return NULLs?", "hard"),
        ("Write a query to find pairs of employees in the same department where one earns exactly double the other.", "hard"),
        ("What is a multi-row subquery? Give an example with ANY.", "medium"),
        ("Write a query using a subquery to find months where sales were below the yearly average.", "medium"),
        ("How do you optimize a slow subquery — what are the common techniques?", "medium"),
        ("Write a query to find students whose marks are above average in every subject they took.", "hard"),
        ("What is the difference between a subquery in WHERE versus a subquery in FROM?", "easy"),
        ("Write a query to find the department with the smallest salary range using a subquery.", "hard"),
        ("How do you convert a NOT IN subquery to a LEFT JOIN?", "medium"),
        ("Write a query to find the latest hired employee in each department using a correlated subquery.", "medium"),
        ("What problems can arise when using NOT IN with a subquery that returns NULLs?", "medium"),
        ("Write a query to find customers who have placed orders for every product in a specific category.", "hard"),
        ("How do you use a subquery with the HAVING clause?", "medium"),
        ("Write a query to find all employees who have the same salary as at least one employee in another department.", "medium"),
        ("What is a row subquery? How do you compare multiple columns with a subquery?", "hard"),
        ("Write a query to rank employees by salary within their department without using window functions.", "hard"),
        ("How do you handle performance issues with deeply nested subqueries?", "medium"),
        ("Write a query using a subquery to find the second most expensive product in each category.", "hard"),
    ]

    for text, diff in subq_compact:
        Q.append(_make_q("sql_subqueries", diff, "fresher", text, _FU_SQL, _PT_SQL))

    # ====================================================================
    # SQL AGGREGATION (30)
    # ====================================================================

    agg_detailed = [
        ("Write a query to find the total salary expenditure per department.",
         "easy",
         ["How do you exclude departments with only one employee?", "Can you add the department name using a JOIN?"],
         ["SUM with GROUP BY", "HAVING clause", "JOIN for department name"]),

        ("What is the difference between COUNT(*) and COUNT(column_name)?",
         "easy",
         ["What does COUNT(DISTINCT column) do?", "How does COUNT handle NULLs?"],
         ["COUNT(*) counts all rows", "COUNT(col) skips NULLs", "DISTINCT eliminates duplicates"]),

        ("Write a query to find departments where the average salary exceeds fifty thousand.",
         "easy",
         ["Can you also show the max and min salary for those departments?", "What if you want this per location per department?"],
         ["AVG with GROUP BY", "HAVING for filtering", "Multiple aggregates"]),

        ("How does GROUP BY work with multiple columns?",
         "easy",
         ["Does the order of columns in GROUP BY affect the result?", "How is it different from DISTINCT on the same columns?"],
         ["Grouping by combinations", "Order does not affect result", "Difference from DISTINCT"]),

        ("Write a query to find the percentage contribution of each department's salary to the total company salary.",
         "medium",
         ["Can you do this without a subquery?", "How would you use a window function for this?"],
         ["SUM per group / SUM total", "Subquery for total", "Window function alternative"]),
    ]

    for text, diff, followups, points in agg_detailed:
        Q.append(_make_q("sql_aggregation", diff, "fresher", text, followups, points))

    agg_compact = [
        ("Write a query to find the maximum salary in each department along with the employee name.", "medium"),
        ("How do you calculate a running average of sales over the last 7 days?", "hard"),
        ("Write a query to count the number of orders placed in each month of the current year.", "easy"),
        ("What is the difference between SUM and TOTAL in SQLite?", "easy"),
        ("Write a query to find the median salary in a table without using a built-in MEDIAN function.", "hard"),
        ("How do you use GROUP BY with ROLLUP to get subtotals?", "medium"),
        ("Write a query to find the department with the second highest average salary.", "medium"),
        ("What is the CUBE operator in GROUP BY? How does it differ from ROLLUP?", "medium"),
        ("Write a query to find customers whose total purchase amount exceeds the overall average total purchase.", "medium"),
        ("How do you count distinct values across multiple columns?", "medium"),
        ("Write a query to find the mode (most frequent value) of a column.", "medium"),
        ("What is GROUPING SETS? When would you use it?", "medium"),
        ("Write a query to find the top 3 products by total revenue in each category.", "hard"),
        ("How do you handle NULL values in GROUP BY — are they grouped together?", "easy"),
        ("Write a query to calculate year-over-year growth in sales.", "hard"),
        ("What is the difference between HAVING and a subquery in WHERE for filtering aggregates?", "medium"),
        ("Write a query to find the average order value per customer, excluding their smallest order.", "hard"),
        ("How do you concatenate grouped values into a single string per group?", "medium"),
        ("Write a query to pivot monthly sales data into columns — one column per month.", "hard"),
        ("What is the STRING_AGG or GROUP_CONCAT function? Give an example.", "easy"),
        ("Write a query to find employees whose salary is above the average but below the maximum in their department.", "medium"),
        ("How do you calculate a weighted average in SQL?", "medium"),
        ("Write a query to find the percentage of NULL values in each column of a table.", "medium"),
        ("What is the FILTER clause in aggregate functions? Which databases support it?", "medium"),
        ("Write a query to find the first and last order date for each customer.", "easy"),
    ]

    for text, diff in agg_compact:
        Q.append(_make_q("sql_aggregation", diff, "fresher", text, _FU_SQL, _PT_SQL))

    # ====================================================================
    # SQL WINDOW FUNCTIONS (30)
    # ====================================================================

    window_detailed = [
        ("Write a query to rank employees by salary within each department using RANK().",
         "medium",
         ["What is the difference between RANK, DENSE_RANK, and ROW_NUMBER?", "What happens when there are ties?"],
         ["PARTITION BY department", "ORDER BY salary DESC", "Gap behavior in RANK vs DENSE_RANK"]),

        ("Write a query to find the second highest salary in each department without using a subquery.",
         "medium",
         ["Which window function would you use?", "How do you handle departments with only one employee?"],
         ["DENSE_RANK with PARTITION BY", "Filter with outer query", "Edge case handling"]),

        ("Explain the difference between ROWS and RANGE in a window frame.",
         "hard",
         ["Give an example where ROWS and RANGE give different results.", "What is the default window frame?"],
         ["ROWS — physical rows", "RANGE — logical value range", "Default: RANGE UNBOUNDED PRECEDING"]),

        ("Write a query using LAG to find the difference in sales between consecutive months.",
         "medium",
         ["What value does LAG return for the first row?", "How do you specify a default value?"],
         ["LAG syntax with PARTITION and ORDER", "Default value parameter", "Month-over-month calculation"]),

        ("Write a query to calculate a running total of sales ordered by date.",
         "medium",
         ["What window frame does this use?", "How do you reset the running total per year?"],
         ["SUM OVER with ORDER BY", "PARTITION BY for reset", "Frame: UNBOUNDED PRECEDING to CURRENT ROW"]),
    ]

    for text, diff, followups, points in window_detailed:
        Q.append(_make_q("sql_window_functions", diff, "fresher", text, followups, points))

    window_compact = [
        ("Write a query using ROW_NUMBER to assign a unique sequence to employees per department.", "medium"),
        ("How do you use NTILE to divide employees into 4 salary quartiles?", "medium"),
        ("Write a query using LEAD to show each employee's salary alongside the next higher salary in their department.", "medium"),
        ("What is the OVER clause? Can you use it without PARTITION BY?", "easy"),
        ("Write a query to find the cumulative percentage of total sales per product.", "hard"),
        ("How do you use FIRST_VALUE and LAST_VALUE in a window function?", "medium"),
        ("Write a query to find the moving average of stock prices over the last 5 days.", "hard"),
        ("What is the difference between a window function and GROUP BY?", "easy"),
        ("Write a query to find the top 2 earners in each department using a window function.", "medium"),
        ("How do you use PERCENT_RANK and CUME_DIST?", "medium"),
        ("Write a query to number each order for a customer in chronological sequence.", "easy"),
        ("What is a named window? How do you define one with the WINDOW clause?", "medium"),
        ("Write a query to find employees whose salary is above the department average using a window function.", "medium"),
        ("How do you calculate a 3-month rolling sum of revenue?", "hard"),
        ("Write a query to find the gap in days between consecutive orders for each customer.", "medium"),
        ("What happens if you omit ORDER BY inside a window function?", "easy"),
        ("Write a query to detect duplicate rows and keep only the first occurrence using ROW_NUMBER.", "medium"),
        ("How do you compute the ratio of each row's value to the partition total using a window function?", "medium"),
        ("Write a query to compare each employee's salary to the department median using window functions.", "hard"),
        ("What is the performance impact of window functions on large datasets?", "medium"),
        ("Write a query using DENSE_RANK to find products with the top 3 highest sales in each region.", "medium"),
        ("How do you partition by multiple columns in a window function?", "easy"),
        ("Write a query to identify the longest streak of consecutive days with sales above a threshold.", "hard"),
        ("What is a frame exclusion clause? When would you use EXCLUDE CURRENT ROW?", "hard"),
        ("Write a query to find the difference between each employee's salary and the maximum salary in their department using a window function.", "medium"),
    ]

    for text, diff in window_compact:
        Q.append(_make_q("sql_window_functions", diff, "fresher", text, _FU_SQL, _PT_SQL))

    # ====================================================================
    # SQL ADVANCED (30)
    # ====================================================================

    adv_detailed = [
        ("What is a Common Table Expression? Write a query using a CTE to find the top department by headcount.",
         "medium",
         ["Can a CTE be recursive?", "How does a CTE differ from a subquery in terms of readability and performance?"],
         ["WITH clause syntax", "CTE scope and reusability", "Performance vs subquery"]),

        ("Write a recursive CTE to generate a hierarchy of employees and managers.",
         "hard",
         ["How do you prevent infinite loops in a recursive CTE?", "What is the termination condition?"],
         ["Anchor member", "Recursive member", "MAXRECURSION / UNION ALL termination"]),

        ("What is a stored procedure? Write a simple stored procedure to insert a new employee.",
         "medium",
         ["What are the advantages of stored procedures over inline SQL?", "What are the disadvantages?"],
         ["CREATE PROCEDURE syntax", "Parameters IN/OUT", "Advantages: security, performance"]),

        ("What is a trigger in SQL? Write an AFTER INSERT trigger to log new employees.",
         "medium",
         ["What is the difference between BEFORE and AFTER triggers?", "Can triggers cause performance issues?"],
         ["CREATE TRIGGER syntax", "Trigger timing and events", "Performance and debugging concerns"]),

        ("Explain the difference between a view and a materialized view.",
         "medium",
         ["When would you use a materialized view?", "How do you refresh a materialized view?"],
         ["View — stored query", "Materialized view — stored result", "Refresh strategies"]),
    ]

    for text, diff, followups, points in adv_detailed:
        Q.append(_make_q("sql_advanced", diff, "fresher", text, followups, points))

    adv_compact = [
        ("Write a query using a recursive CTE to generate numbers from 1 to 100.", "medium"),
        ("What are the advantages of using views? Can you update data through a view?", "medium"),
        ("Write a stored procedure that accepts a department name and returns the average salary.", "medium"),
        ("What is dynamic SQL? When would you use EXEC or EXECUTE IMMEDIATE?", "hard"),
        ("Write a trigger that prevents deleting an employee who is a manager.", "hard"),
        ("What is a cursor? Why are cursors generally discouraged in SQL?", "medium"),
        ("Write a query to pivot rows into columns — showing each product's sales per quarter.", "hard"),
        ("What is the MERGE statement? Write one to upsert employee data.", "hard"),
        ("How do you create an index on a view? What is an indexed view?", "hard"),
        ("Write a query using UNPIVOT to convert columns back into rows.", "hard"),
        ("What is a user-defined function in SQL? How does it differ from a stored procedure?", "medium"),
        ("Write a CTE to find all subordinates of a given manager at any level.", "hard"),
        ("What are table-valued functions? Give an example.", "medium"),
        ("How do you handle errors in a stored procedure using TRY-CATCH or exception handling?", "medium"),
        ("Write a query using APPLY (CROSS APPLY / OUTER APPLY) to get the top 3 orders per customer.", "hard"),
        ("What is a sequence in SQL? How does it differ from an auto-increment column?", "medium"),
        ("Write a query to implement a soft delete using a trigger and a deleted_at column.", "medium"),
        ("What is the difference between a temp table, a table variable, and a CTE?", "medium"),
        ("Write a query using a recursive CTE to compute the Fibonacci sequence up to 20 terms.", "hard"),
        ("How do you schedule a stored procedure to run automatically?", "easy"),
        ("Write a stored procedure with output parameters to return multiple values.", "medium"),
        ("What is SQL injection? How do parameterized queries prevent it?", "medium"),
        ("Write a query to transpose a table so that rows become columns.", "hard"),
        ("What is a synonym in SQL? When is it useful?", "easy"),
        ("How do you implement pagination in SQL — compare OFFSET-FETCH vs keyset pagination?", "medium"),
    ]

    for text, diff in adv_compact:
        Q.append(_make_q("sql_advanced", diff, "fresher", text, _FU_SQL, _PT_SQL))

    # ====================================================================
    # NORMALIZATION (40)
    # ====================================================================

    norm_detailed = [
        ("What is normalization? Why do we normalize a database?",
         "easy",
         ["What are the disadvantages of normalization?", "When would you intentionally denormalize?"],
         ["Reduce redundancy", "Prevent anomalies", "Data integrity"]),

        ("Explain First Normal Form with an example of a table that violates 1NF.",
         "easy",
         ["How do you fix a multi-valued attribute?", "Is a table with repeating groups in 1NF?"],
         ["Atomic values", "No repeating groups", "Example transformation"]),

        ("Explain Second Normal Form. What is a partial dependency?",
         "medium",
         ["Give an example of a table in 1NF but not in 2NF.", "How do you remove partial dependencies?"],
         ["Full functional dependency on entire key", "Partial dependency on part of composite key", "Table decomposition"]),

        ("Explain Third Normal Form. What is a transitive dependency?",
         "medium",
         ["Give a real-world example of a transitive dependency.", "What is the relationship between 3NF and BCNF?"],
         ["No transitive dependencies", "A→B→C means A→C transitively", "Decomposition example"]),

        ("What is Boyce-Codd Normal Form? How is it stricter than 3NF?",
         "hard",
         ["Give an example of a table in 3NF but not in BCNF.", "Is BCNF always achievable without losing dependencies?"],
         ["Every determinant is a candidate key", "3NF allows non-candidate-key determinants", "Dependency preservation trade-off"]),

        ("What are insertion, deletion, and update anomalies? Give examples.",
         "medium",
         ["How does normalization prevent each type?", "Can anomalies still occur in a normalized database?"],
         ["Insertion — cannot add data without unrelated data", "Deletion — losing unrelated data", "Update — inconsistency from partial updates"]),

        ("What is denormalization? When and why would you denormalize?",
         "medium",
         ["What are the risks of denormalization?", "How do you maintain consistency in a denormalized table?"],
         ["Intentional redundancy for performance", "Fewer JOINs at read time", "Risks: inconsistency, storage"]),

        ("Explain functional dependency with an example.",
         "easy",
         ["What is a trivial functional dependency?", "How do you find all functional dependencies in a table?"],
         ["X determines Y means X→Y", "If X is known, Y is uniquely determined", "Closure of attributes"]),
    ]

    for text, diff, followups, points in norm_detailed:
        Q.append(_make_q("normalization", diff, "fresher", text, followups, points))

    norm_compact = [
        ("What is a candidate key? How does it differ from a super key?", "easy"),
        ("Given a table with student_id, course_id, student_name, and course_name — normalize it to 3NF.", "medium"),
        ("What is a prime attribute and a non-prime attribute?", "easy"),
        ("Explain the concept of lossless decomposition.", "medium"),
        ("What is dependency preservation? Why is it important during normalization?", "medium"),
        ("Give an example of a relation that is in BCNF but was originally in 2NF.", "hard"),
        ("What is Fourth Normal Form? What is a multi-valued dependency?", "hard"),
        ("What is Fifth Normal Form? When is it relevant?", "hard"),
        ("How do you determine the highest normal form of a given table?", "medium"),
        ("What is Armstrong's axioms? List and explain each.", "medium"),
        ("Given FDs A→B, B→C, C→D — what is the closure of A?", "medium"),
        ("What is a canonical cover of a set of functional dependencies?", "hard"),
        ("How do you find all candidate keys given a set of functional dependencies?", "hard"),
        ("What is the difference between a key and a superkey?", "easy"),
        ("Explain the trade-offs between normalization and query performance in a real application.", "medium"),
        ("What is a decomposition? When is it lossless-join?", "medium"),
        ("How does normalization affect write performance vs read performance?", "medium"),
        ("What normal form do most production databases aim for and why?", "medium"),
        ("Give an example of a real-world scenario where denormalization is the right choice.", "medium"),
        ("What is a derived attribute? Should it be stored or computed?", "easy"),
        ("How do you normalize a table that stores a student's multiple phone numbers?", "easy"),
        ("What is the difference between a primary key and an alternate key?", "easy"),
        ("If a table has no composite key, can it violate 2NF?", "medium"),
        ("What is domain-key normal form? Is it practically achievable?", "hard"),
        ("Explain how you would normalize an e-commerce order table with repeating product details.", "medium"),
        ("What is a surrogate key? When is it better than a natural key?", "easy"),
        ("How do you handle a many-to-many relationship during normalization?", "easy"),
        ("What is full functional dependency vs partial functional dependency?", "medium"),
        ("Given R(A,B,C,D) with FDs AB→C, C→D, D→A — find the candidate keys and highest normal form.", "hard"),
        ("What is the minimal cover of a set of functional dependencies? How do you compute it?", "hard"),
        ("How does normalization interact with indexing strategies?", "medium"),
        ("What is attribute closure? Compute the closure of {A,B} given A→C, BC→D, D→E.", "medium"),
    ]

    for text, diff in norm_compact:
        Q.append(_make_q("normalization", diff, "fresher", text, _FU_THEORY, _PT_THEORY))

    # ====================================================================
    # ER MODELING (30)
    # ====================================================================

    er_detailed = [
        ("What is an Entity-Relationship diagram? Why is it used in database design?",
         "easy",
         ["What are the components of an ER diagram?", "How do you convert an ER diagram to a relational schema?"],
         ["Entities, attributes, relationships", "Visual design tool", "Maps to tables"]),

        ("Explain the difference between an entity and an attribute with examples.",
         "easy",
         ["When should something be modeled as a separate entity vs an attribute?", "What is a composite attribute?"],
         ["Entity — real-world object", "Attribute — property of entity", "Entity vs attribute decision criteria"]),

        ("What are the different types of relationships — one-to-one, one-to-many, many-to-many?",
         "easy",
         ["Give a real-world example of each.", "How is each type represented in a relational schema?"],
         ["1:1 — Passport to Person", "1:N — Department to Employees", "M:N — Students to Courses"]),

        ("What is a weak entity? Give an example and explain how it is represented.",
         "medium",
         ["What is a partial key?", "How does a weak entity differ from a strong entity in the schema?"],
         ["Depends on identifying entity", "Partial key + owner key = full key", "Double rectangle notation"]),

        ("What is cardinality? How is it different from participation constraints?",
         "medium",
         ["What is the difference between total and partial participation?", "How do you represent minimum and maximum cardinality?"],
         ["Cardinality — max count of relationships", "Participation — min count", "Total vs partial"]),
    ]

    for text, diff, followups, points in er_detailed:
        Q.append(_make_q("er_modeling", diff, "fresher", text, followups, points))

    er_compact = [
        ("What is a derived attribute? Give an example.", "easy"),
        ("How do you represent a multi-valued attribute in an ER diagram and in a relational schema?", "medium"),
        ("What is generalization and specialization in ER modeling?", "medium"),
        ("Explain the concept of aggregation in ER diagrams.", "hard"),
        ("Design an ER diagram for a library management system.", "medium"),
        ("What is the difference between a relationship attribute and an entity attribute?", "medium"),
        ("How do you convert a ternary relationship into binary relationships?", "hard"),
        ("Design an ER diagram for a hospital management system with doctors, patients, and appointments.", "medium"),
        ("What is an identifying relationship? How does it connect to weak entities?", "medium"),
        ("How do you handle recursive relationships in an ER diagram?", "medium"),
        ("Design an ER diagram for an online course platform like Udemy.", "medium"),
        ("What is the difference between total and partial participation? Show both in an ER diagram.", "easy"),
        ("How do you represent inheritance (IS-A relationship) in an ER diagram?", "medium"),
        ("Design an ER diagram for a food delivery app like Swiggy.", "medium"),
        ("What is a role in a relationship? Give an example with a recursive relationship.", "medium"),
        ("How do you decide between a ternary relationship and three binary relationships?", "hard"),
        ("Design an ER diagram for a college placement system.", "medium"),
        ("What is an associative entity? When do you use one?", "medium"),
        ("How do you convert an ER diagram with a many-to-many relationship into a relational schema?", "easy"),
        ("Design an ER diagram for a banking system with accounts, customers, and transactions.", "medium"),
        ("What are the limitations of ER diagrams?", "medium"),
        ("How do you represent optional vs mandatory attributes in an ER diagram?", "easy"),
        ("Design an ER diagram for an inventory management system.", "medium"),
        ("What is the difference between Chen notation and crow's foot notation?", "easy"),
        ("How do you model a self-referencing relationship in an ER diagram — like an employee managing other employees?", "medium"),
    ]

    for text, diff in er_compact:
        Q.append(_make_q("er_modeling", diff, "fresher", text, _FU_THEORY, _PT_THEORY))

    # ====================================================================
    # TRANSACTIONS & ACID (40)
    # ====================================================================

    txn_detailed = [
        ("What are the ACID properties? Explain each one with a real-world banking example.",
         "easy",
         ["What happens if one of the ACID properties is violated?", "Which property is hardest to achieve in a distributed system?"],
         ["Atomicity — all or nothing", "Consistency — valid state transitions", "Isolation — concurrent independence", "Durability — survives crashes"]),

        ("What is a transaction? Write a SQL transaction that transfers money between two accounts.",
         "easy",
         ["What happens if the system crashes after the debit but before the credit?", "How does the database recover?"],
         ["BEGIN/COMMIT/ROLLBACK syntax", "Both operations or neither", "Write-ahead logging for recovery"]),

        ("Explain the different transaction isolation levels.",
         "medium",
         ["What anomalies does each level prevent?", "What is the default isolation level in PostgreSQL? In MySQL?"],
         ["READ UNCOMMITTED, COMMITTED, REPEATABLE READ, SERIALIZABLE", "Dirty reads, non-repeatable reads, phantom reads", "Default levels per database"]),

        ("What is a dirty read? Give an example and explain which isolation level prevents it.",
         "medium",
         ["What is the difference between a dirty read and a non-repeatable read?", "Is READ COMMITTED sufficient for most applications?"],
         ["Reading uncommitted data", "T1 writes, T2 reads, T1 rolls back", "READ COMMITTED prevents it"]),

        ("What is a deadlock? How does a database detect and resolve it?",
         "medium",
         ["Can you give a simple two-transaction deadlock scenario?", "How do you prevent deadlocks in your application code?"],
         ["Circular wait condition", "Wait-for graph detection", "Victim selection and rollback"]),

        ("What is a phantom read? How does SERIALIZABLE isolation level prevent it?",
         "hard",
         ["Give a concrete example of a phantom read.", "Why doesn't REPEATABLE READ prevent phantoms?"],
         ["New rows appear in repeated query", "Range locks or predicate locks", "SERIALIZABLE uses stricter locking"]),

        ("What is the difference between optimistic and pessimistic concurrency control?",
         "medium",
         ["When would you use optimistic over pessimistic?", "How does optimistic concurrency handle conflicts?"],
         ["Pessimistic — lock before access", "Optimistic — check at commit", "Use case depends on conflict rate"]),

        ("What is a savepoint? How do you use partial rollback in a transaction?",
         "medium",
         ["When is a savepoint useful?", "Can you have nested savepoints?"],
         ["SAVEPOINT name", "ROLLBACK TO savepoint", "Nested savepoint support"]),
    ]

    for text, diff, followups, points in txn_detailed:
        Q.append(_make_q("transactions_acid", diff, "fresher", text, followups, points))

    txn_compact = [
        ("What is the difference between a committed and an uncommitted transaction?", "easy"),
        ("How does write-ahead logging (WAL) help in crash recovery?", "medium"),
        ("What is a non-repeatable read? How is it different from a phantom read?", "medium"),
        ("Write a transaction to batch-update salaries with a rollback if any update fails.", "medium"),
        ("What is the two-phase commit protocol? When is it used?", "hard"),
        ("How does MVCC (Multi-Version Concurrency Control) work?", "medium"),
        ("What is a log-based recovery mechanism? Explain undo and redo logging.", "medium"),
        ("What is the difference between implicit and explicit transactions?", "easy"),
        ("How do you set the isolation level for a specific transaction in SQL?", "easy"),
        ("What is a compensating transaction?", "medium"),
        ("Explain the concept of serializability. What is a serializable schedule?", "medium"),
        ("What is the difference between conflict serializability and view serializability?", "hard"),
        ("How do you check if a schedule is conflict serializable using a precedence graph?", "hard"),
        ("What is a cascading rollback? How do you prevent it?", "medium"),
        ("What is strict two-phase locking? How does it differ from basic 2PL?", "hard"),
        ("How does the database handle concurrent reads and writes to the same row?", "medium"),
        ("What is transaction starvation? How can it be prevented?", "medium"),
        ("Explain the concept of a checkpoint in database recovery.", "medium"),
        ("What is the difference between system failure and media failure? How does recovery differ?", "medium"),
        ("How do long-running transactions affect database performance?", "medium"),
        ("What is snapshot isolation? How does it differ from SERIALIZABLE?", "hard"),
        ("Write a transaction that demonstrates the lost update problem.", "medium"),
        ("What is the write skew anomaly? Which isolation level prevents it?", "hard"),
        ("How do distributed transactions work across multiple databases?", "hard"),
        ("What is the difference between AUTOCOMMIT ON and OFF?", "easy"),
        ("How does PostgreSQL implement MVCC internally?", "hard"),
        ("What is a transaction log? How does it ensure durability?", "medium"),
        ("Explain the ARIES recovery algorithm at a high level.", "hard"),
        ("What are the trade-offs between higher isolation levels and performance?", "medium"),
        ("How do you monitor and diagnose deadlocks in a production database?", "medium"),
        ("What is the difference between a shared lock and an exclusive lock?", "easy"),
        ("How do you handle transaction timeouts in a web application?", "medium"),
    ]

    for text, diff in txn_compact:
        Q.append(_make_q("transactions_acid", diff, "fresher", text, _FU_THEORY, _PT_THEORY))

    # ====================================================================
    # INDEXING (40)
    # ====================================================================

    idx_detailed = [
        ("What is an index in a database? Why does it speed up queries?",
         "easy",
         ["Does an index speed up all queries?", "What is the overhead of maintaining an index?"],
         ["Data structure for fast lookup", "Trade-off: fast reads vs slow writes", "Storage overhead"]),

        ("What is the difference between a clustered and a non-clustered index?",
         "medium",
         ["How many clustered indexes can a table have?", "When would you choose non-clustered over clustered?"],
         ["Clustered — physical row order", "Non-clustered — separate structure with pointers", "One clustered per table"]),

        ("Explain how a B-tree index works.",
         "medium",
         ["Why B-tree and not binary tree for databases?", "What is the time complexity of a B-tree lookup?"],
         ["Balanced tree with high branching factor", "Minimizes disk I/O", "O(log n) lookup"]),

        ("What is a composite index? How does column order matter?",
         "medium",
         ["If you have an index on (A, B), can it help a query filtering only on B?", "What is the leftmost prefix rule?"],
         ["Index on multiple columns", "Leftmost prefix used for queries", "Column order based on query patterns"]),

        ("What is a covering index? How does it avoid table lookups?",
         "hard",
         ["How do you identify if an index is covering for a query?", "What is the trade-off of making indexes wider?"],
         ["All queried columns in the index", "Avoids heap/table lookup", "Index size vs lookup savings"]),

        ("What is a hash index? When would you use it instead of a B-tree?",
         "medium",
         ["Can a hash index support range queries?", "Which databases support hash indexes?"],
         ["O(1) exact match lookup", "No range query support", "Memory-based indexes — PostgreSQL, InnoDB adaptive"]),
    ]

    for text, diff, followups, points in idx_detailed:
        Q.append(_make_q("indexing", diff, "fresher", text, followups, points))

    idx_compact = [
        ("When should you NOT create an index?", "easy"),
        ("What is the difference between a unique index and a non-unique index?", "easy"),
        ("How do you see which indexes exist on a table?", "easy"),
        ("Write a CREATE INDEX statement for a composite index on (department_id, hire_date).", "easy"),
        ("What is a partial index? Give a use case.", "medium"),
        ("How does an index affect INSERT, UPDATE, and DELETE performance?", "medium"),
        ("What is an expression index or functional index?", "medium"),
        ("How do you decide which columns to index based on query patterns?", "medium"),
        ("What is index fragmentation? How do you fix it?", "medium"),
        ("What is the difference between a B-tree and a B+ tree?", "medium"),
        ("How does a database use an index for an ORDER BY clause?", "medium"),
        ("What is an index scan vs a full table scan? When does the optimizer choose each?", "medium"),
        ("Write a query and the corresponding index that would make it an index-only scan.", "medium"),
        ("What is a bitmap index? When is it appropriate?", "medium"),
        ("How do multi-column indexes interact with the query optimizer?", "medium"),
        ("What is the selectivity of an index? Why does it matter?", "medium"),
        ("How do you analyze whether your index is actually being used — EXPLAIN ANALYZE?", "medium"),
        ("What is index cardinality? How does low cardinality affect index usefulness?", "medium"),
        ("What is a filtered index? How does it differ from a partial index?", "medium"),
        ("How do you create an index on a text column for pattern matching?", "medium"),
        ("What is the difference between creating an index during or after data load?", "easy"),
        ("What is a GIN or GiST index? When would you use one?", "hard"),
        ("How does the B-tree index handle NULL values?", "medium"),
        ("What is index bloat? How do you detect and fix it in PostgreSQL?", "hard"),
        ("How do you create a descending index? When is it useful?", "easy"),
        ("What is the impact of indexing foreign key columns?", "medium"),
        ("How do you handle indexing for LIKE queries with a leading wildcard?", "hard"),
        ("What is a spatial index? Give a use case for geographic data.", "medium"),
        ("How does the database maintain index consistency during concurrent writes?", "hard"),
        ("What is the difference between a primary index and a secondary index?", "medium"),
        ("How do you benchmark the performance improvement from adding an index?", "medium"),
        ("What is a skip scan optimization for composite indexes?", "hard"),
        ("How many indexes is too many on a single table?", "medium"),
        ("What is an invisible index? When would you use one?", "medium"),
    ]

    for text, diff in idx_compact:
        Q.append(_make_q("indexing", diff, "fresher", text, _FU_OPT, _PT_OPT))

    # ====================================================================
    # CONCURRENCY (30)
    # ====================================================================

    conc_detailed = [
        ("What is a lock in database systems? Explain shared and exclusive locks.",
         "medium",
         ["Can two transactions hold shared locks on the same row?", "What happens when one wants to upgrade to exclusive?"],
         ["Shared — multiple readers", "Exclusive — single writer", "Lock compatibility matrix"]),

        ("What is the two-phase locking protocol?",
         "medium",
         ["What are the two phases?", "Does 2PL guarantee freedom from deadlocks?"],
         ["Growing phase — acquire locks", "Shrinking phase — release locks", "Prevents non-serializable schedules"]),

        ("Explain MVCC. How does PostgreSQL implement it?",
         "hard",
         ["What is the advantage of MVCC over locking?", "How does VACUUM relate to MVCC?"],
         ["Multiple versions of rows", "Readers don't block writers", "Transaction ID visibility"]),

        ("What is lock granularity? Compare row-level, page-level, and table-level locks.",
         "medium",
         ["What is lock escalation?", "Which granularity does InnoDB use by default?"],
         ["Fine-grained — more concurrency, more overhead", "Coarse-grained — less overhead, less concurrency", "Lock escalation"]),

        ("What is a livelock? How does it differ from a deadlock?",
         "hard",
         ["Give an example of a livelock scenario.", "How do you prevent livelocks?"],
         ["Processes keep retrying without progress", "Unlike deadlock — processes are not blocked", "Random backoff prevention"]),
    ]

    for text, diff, followups, points in conc_detailed:
        Q.append(_make_q("concurrency", diff, "fresher", text, followups, points))

    conc_compact = [
        ("What is the difference between pessimistic and optimistic locking? When do you use each?", "medium"),
        ("How does SELECT FOR UPDATE work? Give a use case.", "medium"),
        ("What is lock escalation? When does it happen?", "medium"),
        ("How do you implement optimistic locking using a version column?", "medium"),
        ("What is the difference between blocking and non-blocking reads?", "medium"),
        ("How does InnoDB handle row-level locking internally?", "hard"),
        ("What is a gap lock? How does it prevent phantom reads?", "hard"),
        ("What is a next-key lock in InnoDB?", "hard"),
        ("How do you diagnose lock contention in a production database?", "medium"),
        ("What is the difference between advisory locks and regular locks?", "medium"),
        ("How does timestamp-based concurrency control work?", "medium"),
        ("What is a read-write lock? How does it improve concurrency?", "medium"),
        ("How do you handle hot rows — rows that are updated by many transactions simultaneously?", "hard"),
        ("What is the difference between intent locks and regular locks?", "hard"),
        ("How does the database decide which transaction to abort during a deadlock?", "medium"),
        ("What is connection pooling? How does it relate to concurrency?", "medium"),
        ("How do you prevent lost updates in a concurrent web application?", "medium"),
        ("What is the difference between a read lock and a write lock at the application level?", "easy"),
        ("How does MVCC handle write-write conflicts?", "hard"),
        ("What is the isolation level that provides the best performance with acceptable consistency?", "medium"),
        ("How do you test your application for concurrency bugs?", "medium"),
        ("What is a spin lock? When is it used in database internals?", "hard"),
        ("How does a database handle concurrent DDL and DML operations?", "medium"),
        ("What is the difference between cooperative and preemptive concurrency?", "hard"),
        ("How do you implement a distributed lock using a database?", "hard"),
    ]

    for text, diff in conc_compact:
        Q.append(_make_q("concurrency", diff, "fresher", text, _FU_THEORY, _PT_THEORY))

    # ====================================================================
    # NOSQL (30)
    # ====================================================================

    nosql_detailed = [
        ("What is NoSQL? How does it differ from a relational database?",
         "easy",
         ["When would you choose NoSQL over SQL?", "Can you use SQL with a NoSQL database?"],
         ["Schema-less / flexible schema", "Horizontal scaling", "Different data models"]),

        ("Explain the CAP theorem. Why can't a distributed system have all three properties?",
         "medium",
         ["Give an example of a CP system and an AP system.", "How does eventual consistency relate to the CAP theorem?"],
         ["Consistency, Availability, Partition tolerance", "Can only guarantee two of three during a partition", "Real-world trade-offs"]),

        ("What are the different types of NoSQL databases? Give an example of each.",
         "easy",
         ["When would you use a document store vs a key-value store?", "What about graph databases?"],
         ["Key-value: Redis", "Document: MongoDB", "Column-family: Cassandra", "Graph: Neo4j"]),

        ("What is eventual consistency? How does it differ from strong consistency?",
         "medium",
         ["Give a real-world scenario where eventual consistency is acceptable.", "How do you handle stale reads?"],
         ["All replicas converge eventually", "Strong consistency — read always returns latest write", "Trade-off with availability"]),

        ("What is sharding in a NoSQL database? How is a shard key chosen?",
         "medium",
         ["What happens if you choose a bad shard key?", "How does MongoDB decide which shard a document goes to?"],
         ["Horizontal data partitioning", "Shard key determines distribution", "Hot spots from bad key choice"]),
    ]

    for text, diff, followups, points in nosql_detailed:
        Q.append(_make_q("nosql", diff, "fresher", text, followups, points))

    nosql_compact = [
        ("How does MongoDB store data internally? What is BSON?", "easy"),
        ("What is a replica set in MongoDB? How does failover work?", "medium"),
        ("When would you choose Redis over a relational database?", "easy"),
        ("What is the difference between a document store and a column-family store?", "medium"),
        ("How do you model relationships in MongoDB without foreign keys?", "medium"),
        ("What is a wide-column store? How does Cassandra organize data?", "medium"),
        ("What is a graph database? When is it more suitable than SQL?", "medium"),
        ("How do you handle transactions in MongoDB?", "medium"),
        ("What is the difference between embedding and referencing documents in MongoDB?", "easy"),
        ("How does Cassandra achieve high write throughput?", "hard"),
        ("What is a key-value store? Give three real-world use cases for Redis.", "easy"),
        ("How do you migrate data from a relational database to MongoDB?", "medium"),
        ("What is a document database's equivalent of a JOIN?", "medium"),
        ("How does DynamoDB's partition key and sort key model work?", "medium"),
        ("What is the BASE model? How does it contrast with ACID?", "medium"),
        ("How do you handle schema evolution in a schema-less database?", "medium"),
        ("What is the role of a write-ahead log in NoSQL databases?", "medium"),
        ("How do you choose between MongoDB and PostgreSQL for a new project?", "medium"),
        ("What is tunable consistency in Cassandra?", "hard"),
        ("How does a NoSQL database handle secondary indexes?", "medium"),
        ("What is a time-series database? When would you use InfluxDB or TimescaleDB?", "medium"),
        ("How do you perform aggregations in MongoDB using the aggregation pipeline?", "medium"),
        ("What is the difference between horizontal scaling and vertical scaling?", "easy"),
        ("How does Redis persistence work — RDB vs AOF?", "medium"),
        ("What are the consistency models in DynamoDB — eventually consistent vs strongly consistent reads?", "medium"),
    ]

    for text, diff in nosql_compact:
        Q.append(_make_q("nosql", diff, "fresher", text, _FU_THEORY, _PT_THEORY))

    # ====================================================================
    # PERFORMANCE & QUERY OPTIMIZATION (30)
    # ====================================================================

    perf_detailed = [
        ("How do you read an EXPLAIN plan? What key metrics do you look for?",
         "medium",
         ["What is the difference between estimated and actual cost?", "What does a sequential scan indicate?"],
         ["Cost, rows, width", "Scan types: seq, index, bitmap", "Nested loop vs hash join"]),

        ("What is query optimization? How does the database optimizer choose a plan?",
         "medium",
         ["What is cost-based optimization vs rule-based optimization?", "Can you force the optimizer to use a specific index?"],
         ["Cost-based — estimates I/O and CPU", "Statistics and histograms", "Index hints"]),

        ("What is database partitioning? Explain horizontal vs vertical partitioning.",
         "medium",
         ["When would you partition a table?", "What is the difference between partitioning and sharding?"],
         ["Horizontal — row-based split", "Vertical — column-based split", "Partition pruning"]),

        ("What is database sharding? How does it differ from replication?",
         "medium",
         ["What are the challenges of sharding?", "How do you handle queries that span multiple shards?"],
         ["Data split across servers", "Each shard has unique data", "Cross-shard joins are expensive"]),

        ("How do you identify and optimize a slow query in production?",
         "medium",
         ["What tools would you use?", "Walk me through your debugging process."],
         ["Slow query log", "EXPLAIN ANALYZE", "Index analysis and query rewrite"]),
    ]

    for text, diff, followups, points in perf_detailed:
        Q.append(_make_q("performance", diff, "fresher", text, followups, points))

    perf_compact = [
        ("What is the difference between EXPLAIN and EXPLAIN ANALYZE?", "easy"),
        ("How does adding an index change the EXPLAIN plan?", "medium"),
        ("What is a sequential scan? When does the optimizer prefer it over an index scan?", "medium"),
        ("How do you optimize a query that uses OR conditions?", "medium"),
        ("What is query plan caching? How does it affect parameterized queries?", "medium"),
        ("How do you optimize a query that joins five or more tables?", "hard"),
        ("What is the N+1 query problem? How do you fix it?", "medium"),
        ("How does the database use statistics and histograms for query optimization?", "hard"),
        ("What is a materialized view and how does it improve read performance?", "medium"),
        ("How do you optimize a COUNT query on a large table?", "medium"),
        ("What is partition pruning? How does it speed up queries?", "medium"),
        ("How do you handle pagination efficiently — OFFSET vs keyset?", "medium"),
        ("What is a covering index scan and why is it fast?", "medium"),
        ("How do you optimize a query with multiple subqueries?", "medium"),
        ("What is database connection pooling? How does it improve performance?", "medium"),
        ("How do you optimize bulk INSERT operations?", "medium"),
        ("What is read replication? How does it help scale reads?", "medium"),
        ("How do you identify unused indexes that are slowing down writes?", "medium"),
        ("What is the difference between a hot standby and a warm standby?", "medium"),
        ("How do you optimize a query that uses LIKE with a leading wildcard?", "hard"),
        ("What is the impact of data types on query performance — INT vs VARCHAR for join keys?", "medium"),
        ("How do you use EXPLAIN to detect a missing index?", "medium"),
        ("What is table bloat? How does it affect performance in PostgreSQL?", "medium"),
        ("How do you optimize a query that returns too many rows?", "easy"),
        ("What is the difference between lazy loading and eager loading at the database level?", "medium"),
    ]

    for text, diff in perf_compact:
        Q.append(_make_q("performance", diff, "fresher", text, _FU_OPT, _PT_OPT))

    # ====================================================================
    # COMPANY-SPECIFIC: ORACLE (~15)
    # ====================================================================

    oracle_questions = [
        ("What is Oracle PL/SQL? How does it differ from standard SQL?",
         "medium",
         ["What are PL/SQL blocks?", "How does PL/SQL handle exceptions?"],
         ["Procedural extension to SQL", "Block structure: DECLARE, BEGIN, EXCEPTION, END", "Oracle-specific syntax"],
         "Oracle"),

        ("Explain the difference between Oracle's ROWNUM and ROW_NUMBER() window function.",
         "medium",
         ["Why can't you use ROWNUM > 5 directly?", "How do you do pagination in Oracle?"],
         ["ROWNUM assigned before ORDER BY", "ROW_NUMBER is post-sort", "Pagination with subquery"],
         "Oracle"),

        ("What is the Oracle Data Dictionary? Name some important views.",
         "easy",
         ["What is the difference between USER_, ALL_, and DBA_ views?", "How do you find all tables in your schema?"],
         ["Metadata about database objects", "USER_TABLES, ALL_TABLES, DBA_TABLES", "V$ views for performance"],
         "Oracle"),

        ("How does Oracle handle NULL differently from other databases?",
         "medium",
         ["Is an empty string the same as NULL in Oracle?", "How does this affect VARCHAR2 comparisons?"],
         ["Empty string equals NULL in Oracle", "NVL and NVL2 functions", "Different from PostgreSQL/MySQL"],
         "Oracle"),

        ("What is an Oracle sequence? How do you use it for auto-incrementing IDs?",
         "easy",
         ["What is the difference between NEXTVAL and CURRVAL?", "How does this differ from MySQL AUTO_INCREMENT?"],
         ["CREATE SEQUENCE syntax", "NEXTVAL generates next value", "No automatic column binding"],
         "Oracle"),

        ("What is a tablespace in Oracle? Why is it important for database administration?",
         "medium",
         ["What is the difference between a tablespace and a schema?", "How do you manage tablespace storage?"],
         ["Logical storage grouping", "Maps to physical data files", "Space management"],
         "Oracle"),

        ("What is Oracle's CONNECT BY clause? Write a hierarchical query.",
         "hard",
         ["What is LEVEL in a hierarchical query?", "How does CONNECT BY PRIOR work?"],
         ["Hierarchical query syntax", "START WITH root condition", "LEVEL pseudo-column for depth"],
         "Oracle"),

        ("Explain Oracle's DECODE function. How does it compare to CASE WHEN?",
         "easy",
         ["When would you use DECODE over CASE?", "Is DECODE available in other databases?"],
         ["Inline if-then-else", "Oracle-specific function", "CASE is ANSI standard"],
         "Oracle"),

        ("What is Oracle RAC? How does it provide high availability?",
         "hard",
         ["What is the difference between RAC and Data Guard?", "How does cache fusion work?"],
         ["Real Application Clusters", "Multiple instances, one database", "Shared storage architecture"],
         "Oracle"),

        ("What are Oracle hints? Write a query using an index hint.",
         "medium",
         ["When should you use hints?", "Why are hints generally considered a last resort?"],
         ["/*+ INDEX(table index_name) */", "Override optimizer decisions", "Maintenance risk"],
         "Oracle"),

        ("What is Oracle's flashback technology? Give a use case.",
         "medium",
         ["What is the difference between Flashback Query and Flashback Table?", "How is flashback different from backup/restore?"],
         ["Undo-based point-in-time recovery", "Flashback Query, Table, Database", "Quick recovery from human errors"],
         "Oracle"),

        ("How do you handle exceptions in PL/SQL? Write a block with exception handling.",
         "medium",
         ["What are predefined exceptions like NO_DATA_FOUND?", "How do you define custom exceptions?"],
         ["EXCEPTION block", "WHEN OTHERS THEN", "RAISE_APPLICATION_ERROR"],
         "Oracle"),

        ("What is a PL/SQL cursor? Explain explicit and implicit cursors.",
         "medium",
         ["When do you use an explicit cursor?", "What is a cursor FOR loop?"],
         ["Implicit — single-row queries", "Explicit — DECLARE, OPEN, FETCH, CLOSE", "Cursor attributes: %FOUND, %NOTFOUND"],
         "Oracle"),

        ("What is Oracle's EXPLAIN PLAN? How do you read it?",
         "medium",
         ["What is the cost column?", "How do you use DBMS_XPLAN for formatted output?"],
         ["EXPLAIN PLAN FOR statement", "SELECT from PLAN_TABLE", "Cost, cardinality, access paths"],
         "Oracle"),

        ("What is the difference between Oracle's VARCHAR2 and VARCHAR?",
         "easy",
         ["Why does Oracle recommend VARCHAR2?", "What is the maximum length?"],
         ["VARCHAR2 is Oracle standard", "VARCHAR may change behavior in future", "Max 4000 bytes or 32767 in PL/SQL"],
         "Oracle"),
    ]

    for text, diff, followups, points, company in oracle_questions:
        Q.append(_make_q("sql_advanced", diff, "fresher", text, followups, points, company=company, tags=["oracle", "sql_advanced"]))

    # ====================================================================
    # COMPANY-SPECIFIC: AMAZON (~10)
    # ====================================================================

    amazon_questions = [
        ("Design a database schema for an e-commerce order management system. How would you handle millions of orders per day?",
         "hard",
         ["How would you partition the orders table?", "What indexes would you create?"],
         ["Schema design for orders, items, payments", "Partitioning by date", "Indexing strategy for common queries"],
         "Amazon"),

        ("How would you design a URL shortener's database? What are the scaling considerations?",
         "hard",
         ["How do you generate unique short codes?", "How do you handle high read throughput?"],
         ["Key-value storage model", "Read-heavy workload optimization", "Caching layer"],
         "Amazon"),

        ("Explain how you would choose between DynamoDB and RDS for a given use case.",
         "medium",
         ["What are the pros and cons of each?", "When would you use both together?"],
         ["DynamoDB — key-value, serverless, scale", "RDS — relational, ACID, complex queries", "Polyglot persistence"],
         "Amazon"),

        ("How would you design the database for a real-time leaderboard with millions of users?",
         "hard",
         ["What data structure would you use?", "How do you handle ties?"],
         ["Sorted set in Redis", "Read/write trade-offs", "Pagination of leaderboard"],
         "Amazon"),

        ("Write a query to find the top 5 most frequently purchased product pairs from an orders table.",
         "hard",
         ["How would you optimize this for a table with billions of rows?", "Can you use a probabilistic approach?"],
         ["Self-join on order items", "GROUP BY and COUNT", "Optimization: sampling, approximate"],
         "Amazon"),

        ("How would you implement a database audit trail that records every change to every table?",
         "medium",
         ["What is Change Data Capture?", "How does this affect write performance?"],
         ["Trigger-based vs CDC", "Separate audit schema", "Performance impact mitigation"],
         "Amazon"),

        ("What is Amazon Aurora? How does it differ from standard MySQL/PostgreSQL?",
         "medium",
         ["How does Aurora achieve 5x throughput?", "What is Aurora's storage architecture?"],
         ["Cloud-native relational DB", "Distributed storage layer", "Auto-scaling replicas"],
         "Amazon"),

        ("How would you migrate a large Oracle database to PostgreSQL on AWS?",
         "hard",
         ["What tools would you use?", "How do you handle PL/SQL to PL/pgSQL conversion?"],
         ["AWS DMS for migration", "Schema conversion tool", "Testing and validation strategy"],
         "Amazon"),

        ("Design a database schema for a recommendation engine. How do you store user-item interactions?",
         "hard",
         ["How do you handle cold-start users?", "What is the role of the database vs the ML model?"],
         ["User-item interaction table", "Feature store design", "Read patterns for ML inference"],
         "Amazon"),

        ("How would you handle a database that grows by 1 TB per month? What is your archival strategy?",
         "hard",
         ["How do you decide what to archive?", "How do you make archived data queryable?"],
         ["Partitioning by time", "Archive to S3 / cold storage", "Lifecycle policies"],
         "Amazon"),
    ]

    for text, diff, followups, points, company in amazon_questions:
        Q.append(_make_q("performance", diff, "fresher", text, followups, points, company=company, tags=["amazon", "system_design", "dbms"]))

    # ====================================================================
    # COMPANY-SPECIFIC: BANKING (~15)
    # ====================================================================

    banking_questions = [
        ("Write a SQL query to find all accounts that had a negative balance at any point in the last 90 days.",
         "medium",
         ["How do you handle timezone differences?", "What index would speed this up?"],
         ["Date filtering with transaction history", "Aggregate minimum balance per account", "Index on account_id + transaction_date"],
         "Banking"),

        ("Design a database schema for a core banking system with accounts, transactions, and customers.",
         "hard",
         ["How do you handle multi-currency accounts?", "What is the role of a general ledger table?"],
         ["Accounts, customers, transactions schema", "Double-entry bookkeeping", "Multi-currency with exchange rates"],
         "Banking"),

        ("How do you ensure ACID compliance for a funds transfer between two accounts?",
         "medium",
         ["What isolation level would you use?", "How do you handle a failure after debiting but before crediting?"],
         ["Single transaction for both operations", "SERIALIZABLE or at least READ COMMITTED", "Rollback on failure"],
         "Banking"),

        ("Write a query to detect potential fraudulent transactions — more than three transactions of over fifty thousand in a single day from the same account.",
         "medium",
         ["How would you make this run in near real-time?", "What if the threshold needs to be configurable?"],
         ["GROUP BY account_id, date", "HAVING COUNT and SUM conditions", "Streaming alternative"],
         "Banking"),

        ("How do you handle concurrent withdrawals from the same account to prevent overdraft?",
         "hard",
         ["What locking strategy would you use?", "How does this work in a distributed database?"],
         ["SELECT FOR UPDATE on balance", "Pessimistic locking", "Distributed lock challenges"],
         "Banking"),

        ("Write a query to calculate the daily closing balance for each account over the last month.",
         "medium",
         ["How do you handle days with no transactions?", "Can you use a window function for this?"],
         ["Running sum of transactions per account", "Window function with ORDER BY date", "Fill missing dates"],
         "Banking"),

        ("What is the difference between OLTP and OLAP in the context of banking systems?",
         "easy",
         ["Can the same database serve both?", "What is a data warehouse?"],
         ["OLTP — high-frequency, small transactions", "OLAP — complex analytics, large scans", "Separate systems for each"],
         "Banking"),

        ("How do you design a database for regulatory compliance — storing transaction history for 7 years?",
         "hard",
         ["How do you balance storage cost with query performance?", "What is table partitioning's role here?"],
         ["Partitioning by year/quarter", "Archive to cold storage", "Compliance query requirements"],
         "Banking"),

        ("Write a query to find customers who have accounts in multiple branches.",
         "easy",
         ["How would you also find the total balance across all their accounts?", "How do you handle joint accounts?"],
         ["GROUP BY customer_id with COUNT DISTINCT branch", "HAVING COUNT > 1", "SUM of balances with JOIN"],
         "Banking"),

        ("How do you implement row-level security so that a branch manager can only see their branch's data?",
         "hard",
         ["What is a row-level security policy?", "How does this work in PostgreSQL vs Oracle?"],
         ["CREATE POLICY syntax", "Security predicate based on user context", "Performance implications"],
         "Banking"),

        ("Write a query to generate a monthly bank statement — opening balance, all transactions, and closing balance.",
         "medium",
         ["How do you compute the opening balance?", "How do you paginate a large statement?"],
         ["Opening = sum of all prior transactions", "Transactions in date order", "Running balance column"],
         "Banking"),

        ("How do you handle database encryption for sensitive banking data — at rest and in transit?",
         "medium",
         ["What is Transparent Data Encryption?", "How do you encrypt specific columns?"],
         ["TDE for at-rest encryption", "Column-level encryption for PII", "TLS for in-transit"],
         "Banking"),

        ("Write a query to identify dormant accounts — no transaction in the last 12 months.",
         "easy",
         ["How do you exclude system-generated transactions like interest credits?", "What action should the database trigger for dormant accounts?"],
         ["LEFT JOIN with IS NULL or NOT EXISTS", "Date comparison with MAX transaction_date", "Exclude specific transaction types"],
         "Banking"),

        ("How do you implement a maker-checker approval workflow at the database level?",
         "hard",
         ["What is a status-based workflow?", "How do you handle concurrent approvals?"],
         ["Pending/approved/rejected status column", "Separate maker and checker IDs", "Audit trail for approvals"],
         "Banking"),

        ("Write a query to calculate the compound interest on all fixed deposit accounts for a quarterly compounding period.",
         "medium",
         ["How do you handle different interest rates for different tenures?", "What about premature withdrawal?"],
         ["P * (1 + r/n)^(nt) formula in SQL", "JOIN with rate table", "POWER function for exponentiation"],
         "Banking"),
    ]

    for text, diff, followups, points, company in banking_questions:
        Q.append(_make_q("transactions_acid", diff, "fresher", text, followups, points, company=company, tags=["banking", "transactions", "sql"]))

    return Q


# ── Quick validation ──
if __name__ == "__main__":
    qs = get_dbms_questions()
    print(f"Total DBMS questions: {len(qs)}")
    from collections import Counter
    topics = Counter(q["topic"] for q in qs)
    for topic, count in sorted(topics.items(), key=lambda x: -x[1]):
        print(f"  {topic:25s} {count:4d}")
    companies = Counter(q["company_specific"] for q in qs if q["company_specific"])
    print("\nCompany-specific:")
    for comp, count in sorted(companies.items(), key=lambda x: -x[1]):
        print(f"  {comp:25s} {count:4d}")
