class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, other_category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {other_category.name}")
            other_category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = f"{self.name:*^30}\n"
        body = ""
        for item in self.ledger:
            desc = item["description"][:23]
            amt = f"{item['amount']:>7.2f}"
            body += f"{desc:<23}{amt}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + body + total


def create_spend_chart(categories):
    # calculate spent per category
    spent = []
    for cat in categories:
        total = 0
        for item in cat.ledger:
            if item["amount"] < 0:
                total += abs(item["amount"])
        spent.append(total)

    total_spent = sum(spent)
    # convert to percentages rounded down to nearest 10
    percents = [int((s / total_spent) * 100) // 10 * 10 for s in spent]

    chart = "Percentage spent by category\n"
    for level in range(100, -1, -10):
        chart += str(level).rjust(3) + "| "
        for p in percents:
            chart += "o  " if p >= level else "   "
        chart += "\n"

    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    max_length = max(len(cat.name) for cat in categories)
    for i in range(max_length):
        chart += "     "  # line indent
        for cat in categories:
            if i < len(cat.name):
                chart += cat.name[i] + "  "
            else:
                chart += "   "
        if i < max_length - 1:
            chart += "\n"

    return chart
