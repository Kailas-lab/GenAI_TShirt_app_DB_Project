few_shots = [
    {
        "Question": "How many t-shirts do we have left for Nike in XS size and white color?",
        "SQLQuery": "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
        "SQLResult": "91",
        "Answer": "91",
    },
    {
        "Question": "How much is the total price of the inventory for all S-size t-shirts?",
        "SQLQuery": "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE size = 'S'",
        "SQLResult": "22292",
        "Answer": "22292",
    },
    {
        "Question": "If we have to sell all the Levi’s T-shirts today with discounts applied, how much revenue will our store generate (post discounts)?",
        "SQLQuery": """SELECT SUM(price * stock_quantity * (1 - COALESCE(d.pct_discount, 0) / 100)) AS total_revenue 
                       FROM t_shirts t 
                       LEFT JOIN discounts d ON t.t_shirt_id = d.t_shirt_id 
                       WHERE brand = 'Levi';""",
        "SQLResult": "25441",
        "Answer": "25441",
    },
    {
        "Question": "If we have to sell all the Levi’s T-shirts today, how much revenue will our store generate without discount?",
        "SQLQuery": "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
        "SQLResult": "25441",
        "Answer": "25441",
    },
    {
        "Question": "How many white Levi's t-shirts do I have?",
        "SQLQuery": "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'",
        "SQLResult": "5",
        "Answer": "5",
    },
    {
        "Question": "How much sales revenue will be generated if we sell all large-size Nike t-shirts today after discounts?",
        "SQLQuery": """SELECT SUM(a.total_amount * ((100 - COALESCE(discounts.pct_discount, 0)) / 100)) AS total_revenue 
                       FROM (SELECT SUM(price * stock_quantity) AS total_amount, t_shirt_id 
                             FROM t_shirts 
                             WHERE brand = 'Nike' AND size = 'L' 
                             GROUP BY t_shirt_id) a 
                       LEFT JOIN discounts ON a.t_shirt_id = discounts.t_shirt_id""",
        "SQLResult": "7408",
        "Answer": "7408",
    },
    {
        "Question": "If we have to sell all the Nike’s T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?",
        "SQLQuery": """SELECT SUM(price * stock_quantity * (1 - COALESCE(pct_discount, 0) / 100)) 
                       FROM t_shirts LEFT JOIN discounts USING (t_shirt_id) WHERE brand = 'Nike'""",
        "SQLResult": "36608",
        "Answer": "36608",
    },
]
