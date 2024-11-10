class Flatmate:
    def __init__(self, name):
        self.name = name
        self.expenses = []  # List to hold individual and common expenses

    def add_expense(self, description, amount, is_common=False):
        """Add an expense with a flag for common or individual."""
        self.expenses.append({"description": description, "amount": amount,
                              "is_common": is_common})

    def total_individual_expenses(self):
        """Calculate the total of individual expenses."""
        return sum(expense['amount'] for expense in self.expenses
                   if not expense['is_common'])

    def total_common_expenses(self):
        """Calculate the total of common expenses."""
        return sum(expense['amount'] for expense in self.expenses
                   if expense['is_common'])