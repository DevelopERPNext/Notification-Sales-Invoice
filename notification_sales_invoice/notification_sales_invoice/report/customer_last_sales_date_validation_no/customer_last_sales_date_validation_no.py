# Copyright (c) 2024, khattab.com and contributors
# For license information, please see license.txt

# # import frappe
#
#
# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


import frappe

def execute(filters=None):
    columns = [
        {"fieldname": "name", "label": "Name", "fieldtype": "Link", "options": "Customer", "width": 120},
        {"fieldname": "last_sales_date", "label": "Last Sales Date", "fieldtype": "Date", "width": 120},
        {"fieldname": "today", "label": "Today", "fieldtype": "Date", "width": 120},
        {"fieldname": "days_difference", "label": "Days Difference", "fieldtype": "Int", "width": 100}
    ]

    data = frappe.db.sql("""
        SELECT 
            name, 
            last_sales_date, 
            CURDATE() AS today,
            DATEDIFF(CURDATE(), last_sales_date) AS days_difference
        FROM `tabCustomer`
        WHERE last_sales_date <= DATE_SUB(CURDATE(), INTERVAL 10 DAY);
    """, as_dict=1)

    return columns, data