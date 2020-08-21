# coding: utf-8

class Operation:
    def __init__(self, date_operation, date_value, description, value_credit, value_debit, category):
        self.date_operation = date_operation
        self.description = description
        self.value_debit = value_debit

class Category:
    def __init__(self, name, parent, description_list):
        self.name = name
        self.parent = parent
        self.description_list = description_list

class Bank_Statement:
    def __init__(self, operation_list):
        self.operation_list = operation_list

class Brain:
    def __init__(self, category_list):
        self.category_list = category_list



