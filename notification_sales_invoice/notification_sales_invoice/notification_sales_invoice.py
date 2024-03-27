import frappe
from frappe import _
import frappe.utils
from datetime import datetime


# @frappe.whitelist(allow_guest=True)
@frappe.whitelist()
def update_last_sales_date_for_customer(customer_name, new_last_sales_date):
    frappe.db.set_value('Customer', customer_name, 'last_sales_date', new_last_sales_date)
    frappe.db.commit()

    frappe.msgprint("Update Last Sales Invoice Date For Customer" , alert="info")

    # return "Last sales date updated successfully for Customer: {}".format(customer_name)


# @frappe.whitelist()
# def check_last_sales_date(doc, method=None):
#     today = frappe.utils.nowdate()
#
#     # Get the last sale date from the customer document
#     last_sales_date = frappe.get_value("Customer", doc.customer, "last_sales_date")
#
#     if last_sales_date and frappe.utils.days_between(today, last_sales_date) > 10:
#         frappe.msgprint(f"Customer {doc.customer_name} has not made a Sales Invoice in the last 10 days.", alert="info")


@frappe.whitelist()
def check_last_sales_date(doc, invoice_number):
    today = datetime.today().date()

    if isinstance(doc, str):
        doc = frappe.parse_json(doc)

    # Get the last sale date from the customer document
    customer = doc.get('customer')
    last_sales_date_str = frappe.get_value("Customer", customer, "last_sales_date")

    if last_sales_date_str:
        last_sales_date = datetime.strptime(str(last_sales_date_str), '%Y-%m-%d').date()
        days_diff = (today - last_sales_date).days

        if days_diff > 10:
            message = frappe.msgprint(f"Customer {doc.get('customer_name')} has not made a Sales Invoice in the last 10 days.")
            message_doctype = f"Customer {doc.get('customer_name')} has not made a Sales Invoice in the last 10 days."
            # # invoice_doc = frappe.get_doc('Sales Invoice', invoice_number)
            # return success_Log(message, invoice_number)
            success_Log(message_doctype, invoice_number)


def success_Log(message, invoice_number):
    try:
        current_time = frappe.utils.now()
        frappe.get_doc({
            "doctype": "Notification Success Log",
            "title": "Notification Successfully",
            "message": message,
            "invoice_number": invoice_number,
            "date": current_time
        }).insert(ignore_permissions=True)
    except Exception as e:
        frappe.throw("Error in success log  " + str(e))
