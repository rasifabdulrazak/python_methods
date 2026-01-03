# Class Methods vs Static Methods in Python

A comprehensive guide to understanding and using `@classmethod` and `@staticmethod` decorators in Python, with real-world examples.

## Table of Contents

- [Overview](#overview)
- [Instance Methods (Regular Methods)](#instance-methods-regular-methods)
- [Class Methods](#class-methods)
- [Static Methods](#static-methods)
- [Comparison Table](#comparison-table)
- [When to Use What](#when-to-use-what)
- [Real-World Use Cases](#real-world-use-cases)
- [Common Patterns](#common-patterns)
- [Best Practices](#best-practices)

## Overview

Python provides three types of methods you can define in a class:

1. **Instance Methods** - Operate on an instance of the class
2. **Class Methods** - Operate on the class itself
3. **Static Methods** - Utility functions that belong to the class namespace

Understanding when to use each is crucial for writing clean, maintainable code.

## Instance Methods (Regular Methods)

Instance methods are the most common type. They take `self` as the first parameter and can access/modify instance attributes.

```python
class BankAccount:
    def __init__(self, balance):
        self.balance = balance
    
    def deposit(self, amount):  # Instance method
        self.balance += amount
        return self.balance
```

**Key characteristics:**
- First parameter is `self` (the instance)
- Can access and modify instance attributes (`self.balance`)
- Can access class attributes through `self.__class__` or the class name
- Must be called on an instance: `account.deposit(100)`

## Class Methods

Class methods are decorated with `@classmethod` and take `cls` as the first parameter. They operate on the class itself, not instances.

```python
class Employee:
    company_name = "TechCorp"
    
    @classmethod
    def set_company_name(cls, name):
        cls.company_name = name
    
    @classmethod
    def from_string(cls, emp_string):
        name, salary = emp_string.split('-')
        return cls(name, float(salary))  # Creates new instance
```

**Key characteristics:**
- Decorated with `@classmethod`
- First parameter is `cls` (the class itself)
- Can access and modify class attributes (`cls.company_name`)
- Can create instances using `cls(...)`
- Called on the class: `Employee.set_company_name("NewCorp")`
- Can also be called on instances: `employee.set_company_name("NewCorp")`

### Common Use Cases for Class Methods

#### 1. Alternative Constructors (Factory Methods)

One of the most powerful uses of class methods is creating alternative constructors:

```python
class Employee:
    @classmethod
    def from_string(cls, emp_string):
        """Create employee from CSV string"""
        name, salary, date = emp_string.split('-', max_split=2)
        return cls(name, float(salary), datetime.strptime(date, '%Y-%m-%d'))
    
    @classmethod
    def from_dict(cls, data):
        """Create employee from JSON/dictionary"""
        return cls(data['name'], data['salary'], data['hire_date'])
```

**Why this matters:** Different data sources (CSV, JSON, databases) can each have their own constructor method, keeping your code organized and flexible.

#### 2. Managing Class-Level State

Class methods are ideal for operations that affect all instances:

```python
class DatabaseConnection:
    _connection_pool = []
    
    @classmethod
    def get_connection(cls):
        """Manage shared connection pool"""
        if len(cls._connection_pool) < cls.max_connections:
            conn = cls()
            cls._connection_pool.append(conn)
            return conn
        return cls._connection_pool[0]
    
    @classmethod
    def close_all_connections(cls):
        """Clean up all connections"""
        for conn in cls._connection_pool:
            conn.close()
        cls._connection_pool.clear()
```

**Real-world application:** Connection pooling, caching, singleton patterns, resource management.

#### 3. Class Configuration

Modifying class-level settings that affect all instances:

```python
class Product:
    tax_rate = 0.08
    
    @classmethod
    def update_tax_rate(cls, new_rate):
        """Update tax rate for all products"""
        cls.tax_rate = new_rate
```

#### 4. Querying/Aggregating Class Data

```python
class Employee:
    all_employees = []
    
    @classmethod
    def get_total_employees(cls):
        return len(cls.all_employees)
    
    @classmethod
    def get_average_salary(cls):
        if not cls.all_employees:
            return 0
        return sum(e.salary for e in cls.all_employees) / len(cls.all_employees)
```

## Static Methods

Static methods are decorated with `@staticmethod` and don't take `self` or `cls` as parameters. They're essentially regular functions that belong to the class namespace.

```python
class Employee:
    @staticmethod
    def is_valid_salary(salary):
        return salary >= 30000 and salary <= 1000000
    
    @staticmethod
    def calculate_annual_bonus(salary, rating):
        bonus_rates = {5: 0.20, 4: 0.15, 3: 0.10}
        return salary * bonus_rates.get(rating, 0.10)
```

**Key characteristics:**
- Decorated with `@staticmethod`
- No `self` or `cls` parameter
- Cannot access instance or class attributes
- Purely a utility function that logically belongs to the class
- Called on the class: `Employee.is_valid_salary(50000)`
- Can also be called on instances: `employee.is_valid_salary(50000)`

### Common Use Cases for Static Methods

#### 1. Validation Functions

```python
class Product:
    @staticmethod
    def is_valid_sku(sku):
        """Validate SKU format before creating product"""
        return bool(re.match(r'^[A-Z]{3}\d{5}$', sku))
    
    @staticmethod
    def is_valid_price(price):
        return isinstance(price, (int, float)) and price > 0
```

**Use case:** Validate data before creating objects, ensuring data quality.

#### 2. Calculations and Transformations

```python
class Employee:
    @staticmethod
    def calculate_annual_bonus(salary, performance_rating):
        """Calculate bonus based on salary and rating"""
        bonus_percentage = {5: 0.20, 4: 0.15, 3: 0.10, 2: 0.05}
        return salary * bonus_percentage.get(performance_rating, 0)
    
    @staticmethod
    def format_currency(amount):
        return f"${amount:,.2f}"
```

#### 3. Parsing and Formatting Utilities

```python
class DatabaseConnection:
    @staticmethod
    def parse_connection_string(conn_string):
        """Parse 'host:port/database' format"""
        pattern = r'([^:]+):(\d+)/(.+)'
        match = re.match(pattern, conn_string)
        if match:
            return {
                'host': match.group(1),
                'port': int(match.group(2)),
                'database': match.group(3)
            }
        return None
```

#### 4. Pure Utility Functions

```python
class DateUtils:
    @staticmethod
    def is_business_day(date):
        return date.weekday() < 5
    
    @staticmethod
    def get_business_days_between(start, end):
        days = 0
        current = start
        while current <= end:
            if DateUtils.is_business_day(current):
                days += 1
            current += timedelta(days=1)
        return days
```

**Philosophy:** If a function is logically related to a class but doesn't need access to instance or class data, make it a static method. This keeps related functionality organized together.

## Comparison Table

| Feature | Instance Method | Class Method | Static Method |
|---------|----------------|--------------|---------------|
| **Decorator** | None | `@classmethod` | `@staticmethod` |
| **First Parameter** | `self` | `cls` | None |
| **Access Instance Data** | ✅ Yes | ❌ No | ❌ No |
| **Access Class Data** | ✅ Yes | ✅ Yes | ❌ No |
| **Modify Instance Data** | ✅ Yes | ❌ No | ❌ No |
| **Modify Class Data** | ✅ Yes | ✅ Yes | ❌ No |
| **Create Instances** | ✅ Yes | ✅ Yes | ❌ No (well, technically yes but awkward) |
| **Call on Class** | ❌ No | ✅ Yes | ✅ Yes |
| **Call on Instance** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Main Purpose** | Work with instance | Work with class | Utility function |

## When to Use What

### Use Instance Methods When:
- You need to access or modify instance-specific data
- The operation is specific to one object
- You're implementing the core functionality of the class

**Example:** `bank_account.withdraw(100)` - operates on THIS specific account

### Use Class Methods When:
- Creating alternative constructors/factory methods
- Managing class-level state or resources
- Modifying class attributes that affect all instances
- Querying or aggregating data across all instances
- Implementing singleton or factory patterns

**Example:** `Employee.from_csv_file("employees.csv")` - creates instances from different data formats

### Use Static Methods When:
- The function is related to the class conceptually but doesn't need class/instance data
- You're creating utility functions for validation, formatting, or calculations
- The function could be a module-level function but you want to keep it organized within the class
- You want to namespace related functions together

**Example:** `Employee.is_valid_email(email)` - validates email format, doesn't need any employee data

## Real-World Use Cases

### 1. Employee Management System

**Scenario:** Building an HR system that needs to handle employee data from multiple sources.

```python
class Employee:
    @classmethod
    def from_csv_row(cls, csv_row):
        """Import from CSV file"""
        return cls(csv_row[0], float(csv_row[1]), csv_row[2])
    
    @classmethod
    def from_api_response(cls, json_data):
        """Import from external API"""
        return cls(json_data['fullName'], json_data['annualSalary'], 
                   json_data['department'])
    
    @staticmethod
    def validate_salary_range(salary):
        """Check if salary is within company guidelines"""
        return 30000 <= salary <= 500000
```

**Why:** Class methods handle different data formats cleanly, static method validates regardless of source.

### 2. Database Connection Pool

**Scenario:** Managing a pool of database connections to avoid creating too many connections.

```python
class DatabaseConnection:
    _pool = []
    
    @classmethod
    def get_connection(cls):
        """Get from pool or create new"""
        if cls._pool:
            return cls._pool.pop()
        return cls()
    
    @classmethod
    def return_connection(cls, conn):
        """Return connection to pool"""
        cls._pool.append(conn)
    
    @staticmethod
    def validate_connection_string(conn_str):
        """Validate format before attempting connection"""
        return '://' in conn_str and '@' in conn_str
```

**Why:** Class methods manage the shared pool, static method validates input.

### 3. E-commerce Product System

**Scenario:** Managing products with business rules and calculations.

```python
class Product:
    tax_rate = 0.08
    
    @classmethod
    def bulk_import(cls, products_list):
        """Import multiple products at once"""
        return [cls(**product_data) for product_data in products_list]
    
    @classmethod
    def update_tax_rate(cls, new_rate):
        """Update tax for all products"""
        cls.tax_rate = new_rate
    
    @staticmethod
    def calculate_discount(price, percent):
        """Calculate discounted price"""
        return price * (1 - percent / 100)
    
    @staticmethod
    def format_price(amount):
        """Format as currency"""
        return f"${amount:,.2f}"
```

**Why:** Class methods handle bulk operations and configuration, static methods provide reusable calculations.

## Common Patterns

### Pattern 1: Factory Pattern with Class Methods

```python
class Report:
    @classmethod
    def from_excel(cls, filepath):
        # Parse Excel file
        return cls(data)
    
    @classmethod
    def from_database(cls, query):
        # Fetch from database
        return cls(data)
    
    @classmethod
    def from_api(cls, endpoint):
        # Fetch from API
        return cls(data)
```

### Pattern 2: Validation Layer with Static Methods

```python
class User:
    @staticmethod
    def validate_email(email):
        return '@' in email and '.' in email
    
    @staticmethod
    def validate_password(password):
        return len(password) >= 8 and any(c.isdigit() for c in password)
    
    def __init__(self, email, password):
        if not User.validate_email(email):
            raise ValueError("Invalid email")
        if not User.validate_password(password):
            raise ValueError("Weak password")
        self.email = email
        self.password = password
```

### Pattern 3: Configuration Management with Class Methods

```python
class APIClient:
    base_url = "https://api.example.com"
    timeout = 30
    
    @classmethod
    def configure(cls, base_url=None, timeout=None):
        """Configure all API clients at once"""
        if base_url:
            cls.base_url = base_url
        if timeout:
            cls.timeout = timeout
```

## Best Practices

### 1. Choose the Right Method Type

❌ **Don't use static method when you need class data:**
```python
class Product:
    tax_rate = 0.08
    
    @staticmethod
    def calculate_price_with_tax(price):
        # Can't access cls.tax_rate!
        return price * 1.08  # Hardcoded, bad!
```

✅ **Use class method instead:**
```python
class Product:
    tax_rate = 0.08
    
    @classmethod
    def calculate_price_with_tax(cls, price):
        return price * (1 + cls.tax_rate)
```

### 2. Name Alternative Constructors Clearly

✅ **Good naming convention:**
- `from_string()`, `from_dict()`, `from_csv()`
- Clear what format they expect

❌ **Poor naming:**
- `create()`, `make()`, `new()`
- Ambiguous what they do differently from `__init__`

### 3. Keep Static Methods Pure

Static methods should be self-contained and not rely on external state:

✅ **Good:**
```python
@staticmethod
def calculate_discount(price, percent):
    return price * (1 - percent / 100)
```

❌ **Bad:**
```python
@staticmethod
def calculate_discount(price):
    # Relies on global variable
    return price * discount_rate
```

### 4. Document Use Cases

Always document why you chose class/static methods:

```python
@classmethod
def from_json(cls, json_string):
    """
    Create Product from JSON string.
    
    Use case: API responses, configuration files
    Example: Product.from_json('{"name": "Widget", "price": 9.99}')
    """
    data = json.loads(json_string)
    return cls(**data)
```

### 5. Avoid Overusing Static Methods

If you have many static methods with no instance/class methods, consider if they should be module-level functions instead:

❌ **Questionable:**
```python
class StringUtils:
    @staticmethod
    def uppercase(s): ...
    
    @staticmethod
    def lowercase(s): ...
    
    @staticmethod
    def reverse(s): ...
```

✅ **Better:**
```python
# string_utils.py
def uppercase(s): ...
def lowercase(s): ...
def reverse(s): ...
```

### 6. Class Methods for Inheritance

Class methods work well with inheritance because they use `cls`:

```python
class Animal:
    @classmethod
    def create(cls, name):
        return cls(name)  # Creates instance of actual class

class Dog(Animal):
    pass

dog = Dog.create("Buddy")  # Creates Dog, not Animal!
```

## Running the Examples

To run the provided examples:

```bash
python class_static_methods.py
```

The script will demonstrate:
- Employee management with alternative constructors
- Database connection pooling
- Product inventory with calculations
- Date utilities

Each example shows practical, real-world scenarios where class methods and static methods solve actual problems you'll encounter in production code.

## Summary

- **Instance methods** are for operations on individual objects
- **Class methods** (`@classmethod`) are for operations on the class itself - alternative constructors, managing shared state, class-level configuration
- **Static methods** (`@staticmethod`) are for utility functions that logically belong to the class but don't need instance or class data

Choose based on what the method needs to access, not arbitrary preference. The right choice makes your code more maintainable, testable, and intuitive to other developers.