# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document


class DocField(Document):
	def get_link_doctype(self):
		"""Returns the Link doctype for the docfield (if applicable)
		if fieldtype is Link: Returns "options"
		if fieldtype is Table MultiSelect: Returns "options" of the Link field in the Child Table
		"""
		if self.fieldtype == "Link":
			return self.options

		if self.fieldtype == "Table MultiSelect":
			table_doctype = self.options

			return frappe.db.get_value(
				"DocField",
				{
					"fieldtype": "Link",
					"parenttype": "DocType",
					"parent": table_doctype,
					"in_list_view": 1,
				},
				"options",
			)

	def get_select_options(self):
		if self.fieldtype == "Select":
			options = self.options or ""
			return [d for d in options.split("\n") if d]

	def __repr__(self):
		unsaved = "unsaved" if not self.name else ""
		doctype = self.__class__.__name__

		docstatus = f" docstatus={self.docstatus}" if self.docstatus else ""
		parent = f" parent={self.parent}" if getattr(self, "parent", None) else ""

		return f"<{self.fieldtype}{doctype}: {self.fieldname}{docstatus}{parent}{unsaved}>"
