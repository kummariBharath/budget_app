# 📊 Budget App in Python — Daily Revision README

This README is designed so Bharath can **revise daily** and clearly understand the full Budget App program used in the FreeCodeCamp project.

It explains:

* The purpose of the program
* The `Category` class (whole program context)
* The `create_spend_chart` function **line by line**

The spend chart explanation below keeps the **same examples and logic** and is written in a professional but very understandable style.

# 🚀 Project Overview

This program builds a simple **budget tracking system** in Python. It allows you to:

* Create spending categories (Food, Clothing, Auto, etc.)
* Deposit money
* Withdraw money
* Transfer money between categories
* Print clean category summaries
* Generate a **text-based percentage spending chart**

This is a **logic-heavy project**, meant to improve:

* Looping
* Lists & dictionaries
* String formatting
* Object‑oriented thinking

---

## Part 1: The `Category` Class

The `Category` class is the core of this application. It represents a single budget category (like "Food", "Clothing", or "Auto").

### 1. Initialization (`__init__`)

```python
class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
```

**Concept: Classes and Objects**
- Think of a **Class** (`Category`) as a blueprint or template.
- Think of an **Object** (an instance) as a house built from that blueprint. You can build many houses (Food, Auto, Rent) from the same blueprint.

**How it works:**
- `__init__`: This is a special method (constructor). It runs *automatically* whenever you create a new category (e.g., `food = Category("Food")`).
- `self`: This variable refers to the *specific* object being created. If you create a "Food" category, `self` is that "Food" object.
- `self.name`: Stores the name ("Food") so the object "knows" what it is.
- `self.ledger`: Creates an empty list `[]`. This ledger will act like a bank statement, storing every transaction (deposits and withdrawals).

---

### 2. Making Deposits (`deposit`)

```python
    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
```

**How it works:**
- This method accepts an `amount` (number) and an optional `description` (text).
- If you don't provide a description, it defaults to an empty string `""`.
- `append()`: Adds an item to the end of the `ledger` list.
- The item added is a **Dictionary**: `{"amount": 50, "description": "Groceries"}`. This keeps the amount and description paired together.

---

### 3. Making Withdrawals (`withdraw`)

```python
    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False
```

**How it works:**
1. **Check Funds First**: Before withdrawing, it calls `self.check_funds(amount)` to ensure you have enough money.
2. **If Yes (True)**:
   - It adds a negative number (`-amount`) to the ledger. This is how we distinguish spending from earning.
   - It returns `True` to tell the caller "Success!".
3. **If No (False)**:
   - It returns `False` immediately. No transaction is recorded.

---

### 4. Getting the Balance (`get_balance`)

```python
    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)
```

**Concept: Generator Expression**
- `item["amount"] for item in self.ledger`: This acts like a loop. It goes through every transaction in the ledger and pulls out just the number associated with "amount".
- `sum(...)`: Adds all those numbers together.
- Since withdrawals are stored as negative numbers (e.g., -10) and deposits as positive (e.g., 50), adding them all up automatically gives you the correct current balance.

---

### 5. Transfers (`transfer`)

```python
    def transfer(self, amount, other_category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {other_category.name}")
            other_category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False
```

**How it works:**
- Moves money from `self` (this category) to `other_category` (the one passed in as an argument).
- **f-strings (`f"..."`)**: This is a way to insert variables directly into text. `{other_category.name}` is replaced by the actual name.
- It reuses the existing `withdraw` and `deposit` methods, so we don't have to rewrite code to add to the ledger manually.

---

### 6. Checking Funds (`check_funds`)

```python
    def check_funds(self, amount):
        return amount <= self.get_balance()
```

**How it works:**
- A simple helper. It compares the `amount` you want to spend against your current balance (`self.get_balance()`).
- Returns `True` if you can afford it, `False` otherwise.

---

### 7. Printing the Object (`__str__`)

This method is what makes `print(food)` output a nice looking table instead of `<Category object at 0x...>`.

```python
    def __str__(self):
        title = f"{self.name:*^30}\n"
```
- **`*^30`**: This creates the header.
  - `^`: Center align the name.
  - `30`: Make the total width 30 characters.
  - `*`: Fill the empty space with asterisks.
  - Result: `*************Food*************`

```python
        body = ""
        for item in self.ledger:
            desc = item["description"][:23]
            amt = f"{item['amount']:>7.2f}"
            body += f"{desc:<23}{amt}\n"
```
- **`[:23]`**: Slices string. Keeps only the first 23 characters of the description so it doesn't break the table layout.
- **`:>7.2f`**: Formats the number.
  - `>`: Right align.
  - `7`: Take up 7 spaces total.
  - `.2f`: Show exactly 2 decimal places (e.g., `10.00`).
- **`desc:<23`**: Left align the description in a 23-space block.
- **Combined**: This ensures the description and amount always line up perfectly to equal 30 characters (23 + 7).

---

# 📈 Part 2: `create_spend_chart(categories)` — Line by Line Deep Explanation

This function’s only job is to **build the percentage spending chart**.

It does 4 major things:

1. Finds how much money was spent in each category
2. Converts that into percentages rounded down to the nearest 10
3. Draws the vertical bar chart
4. Writes the category names vertically

---

## 🥄 Step 1: Finding spent money

```python
spent = []
for cat in categories:
    total = 0
    for item in cat.ledger:
        if item["amount"] < 0:
            total += abs(item["amount"])
    spent.append(total)
```

* `categories` is a list like `[food, clothing, auto]`
* Each `cat.ledger` is a list of dictionaries

Example ledger:

```python
{"amount": -50, "description": "pizza"}
{"amount": 100, "description": "salary"}
```

Only **negative values** matter (money spent).

* `if item["amount"] < 0:` → only withdrawals
* `abs()` → converts -50 to 50
* `spent.append(total)` → saves category spending

Result example:

```python
spent = [120, 90, 30]
```

---

## 🥄 Step 2: Convert to percentages

```python
total_spent = sum(spent)
percents = [int((s / total_spent) * 100) // 10 * 10 for s in spent]
```

Suppose:

```python
spent = [120, 90, 30]
total_spent = 240
```

For food:

```
120 / 240 = 0.5 → 50% → 50
```

Why this logic?

```python
int(...) // 10 * 10
```

This **rounds DOWN to nearest 10**:

* 57 → 50
* 99 → 90
* 10 → 10

Because the chart only supports:
0,10,20,30…100

Result:

```python
percents = [50, 30, 10]
```

---

## 🥄 Step 3: Chart title

```python
chart = "Percentage spent by category\n"
```

Creates the heading.

---

## 🥄 Step 4: Y‑axis numbers

```python
for level in range(100, -1, -10):
    chart += str(level).rjust(3) + "| "
```

Builds:

```
100|
 90|
 80|
...
  0|
```

`rjust(3)` aligns numbers vertically.

---

## 🥄 Step 5: Drawing the dots

```python
for p in percents:
    chart += "o  " if p >= level else "   "
```

This is the **core logic**.

For each level (100 → 0):

* If category percent ≥ that level → print `o`
* Else → print space

Example:

```python
percents = [50, 30, 10]
```

At `level = 40`:

* 50 ≥ 40 → o
* 30 ≥ 40 → space
* 10 ≥ 40 → space

Line becomes:

```
40| o
```

This repeats to form the vertical bars.

---

## 🥄 Step 6: Bottom horizontal line

```python
chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"
```

If 3 categories:

```
----------
```

This separates chart and labels.

---

## 🥄 Step 7: Longest name

```python
max_length = max(len(cat.name) for cat in categories)
```

Finds how many vertical rows are needed.

Example:
Food (4)
Clothing (8)
Auto (4)
→ max_length = 8

---

## 🥄 Step 8: Writing names vertically

```python
for i in range(max_length):
    chart += "     "
    for cat in categories:
        if i < len(cat.name):
            chart += cat.name[i] + "  "
        else:
            chart += "   "
```

This prints one character per row.

Builds:

```
F  C  A  
o  l  u  
o  o  t  
d  t  o  
   h     
   i     
   n     
   g
```

---

## 🥄 Step 9: Return the chart

```python
return chart
```

Sends the final formatted chart back to the program.

---

# 🧾 One‑Line Summary

This function reads spending data, converts it into rounded percentages, draws vertical bars using text, and writes category names vertically to create a full ASCII chart.

---

# ✅ Daily Revision Strategy

1. Read **Project Overview**
2. Review **Category class purpose**
3. Study **one spoon step per day**
4. Rewrite the function from memory
5. Print your own chart examples

---

If you can rebuild this from scratch without looking — you officially leveled up as a Python dev. 💻🔥
