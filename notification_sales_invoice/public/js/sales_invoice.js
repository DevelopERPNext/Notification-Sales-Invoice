
//frappe.ui.form.on("Sales Invoice", {
//    refresh: function(frm) {
//});


//// Call the function on Sales Invoice `before_submit` event
//frappe.ui.form.on('Sales Invoice', {
//    before_submit: before_submit_sales_invoice
//})

frappe.ui.form.on('Sales Invoice', {
    before_submit: function(frm) {
        var customer = frm.doc.customer;
        var postingDate = frm.doc.posting_date;

        if (customer && postingDate) {
            frappe.call({
                method: 'notification_sales_invoice.notification_sales_invoice.notification_sales_invoice.update_last_sales_date_for_customer',
                args: {
                    customer_name: customer,
                    new_last_sales_date: postingDate
                },
                callback: function(response) {
                    if (response.message) {
                        console.log('Posting Date updated in Sales Invoice');
                    } else {
                        console.log('Error updating Posting Date');
                    }
                }
            });
        }
    }
});



frappe.ui.form.on("Sales Invoice", {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Check Date'), function() {
                frm.events.get_call(frm);
            });
        }
    },

    get_call: function(frm) {
        frappe.call({
            method: "notification_sales_invoice.notification_sales_invoice.notification_sales_invoice.check_last_sales_date",
            args: {
                doc: frm.doc,
                invoice_number: frm.doc.name
            },
            callback: function(response) {
                if (response.message) {
                    frappe.msgprint(response.message, "info");
                }
            }
        });
        frappe.show_alert({
            message:__('Get Function'),
            indicator:'green'
        }, 5);
    }
});