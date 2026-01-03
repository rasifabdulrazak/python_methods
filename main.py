"""
Real-world examples demonstrating class methods and static methods in Python.
Each example represents practical use cases you'd encounter in production code.
"""

from datetime import datetime, timedelta
from typing import List, Optional
import re


# Example 1: Employee Management System
class Employee:
    """Demonstrates class methods for alternative constructors and class-level operations."""
    
    company_name = "PyRasif"
    employee_count = 0
    min_salary = 30000
    
    def __init__(self, name: str, salary: float, hire_date: datetime):
        self.name = name
        self.salary = salary
        self.hire_date = hire_date
        Employee.employee_count += 1
    
    @classmethod
    def from_string(cls, emp_string: str):
        """Alternative constructor: Create employee from formatted string.
        Use case: Parsing employee data from CSV or text files."""
        name, salary, date_str = emp_string.split('-',maxsplit=2)
        hire_date = datetime.strptime(date_str, '%Y-%m-%d')
        return cls(name, float(salary), hire_date)
    
    @classmethod
    def from_dict(cls, emp_dict: dict):
        """Alternative constructor: Create employee from dictionary.
        Use case: Creating objects from JSON API responses."""
        return cls(
            emp_dict['name'],
            emp_dict['salary'],
            datetime.fromisoformat(emp_dict['hire_date'])
        )
    
    @classmethod
    def set_company_name(cls, new_name: str):
        """Modify class variable affecting all instances.
        Use case: Company rebranding or configuration changes."""
        cls.company_name = new_name
    
    @classmethod
    def get_employee_count(cls) -> int:
        """Access class-level data.
        Use case: Dashboard statistics, reporting."""
        return cls.employee_count
    
    @staticmethod
    def is_valid_salary(salary: float) -> bool:
        """Utility function related to Employee but doesn't need instance/class data.
        Use case: Input validation before object creation."""
        return salary >= Employee.min_salary and salary <= 1000000
    
    @staticmethod
    def calculate_annual_bonus(salary: float, performance_rating: float) -> float:
        """Utility calculation related to employees.
        Use case: Standalone calculation that logically belongs to Employee class."""
        bonus_percentage = {
            5.0: 0.20,  # Outstanding
            4.0: 0.15,  # Exceeds expectations
            3.0: 0.10,  # Meets expectations
            2.0: 0.05,  # Needs improvement
            1.0: 0.00   # Unsatisfactory
        }
        return salary * bonus_percentage.get(performance_rating, 0.10)
    
    def __repr__(self):
        return f"Employee('{self.name}', ${self.salary:,.2f}, {self.company_name})"


# Example 2: Database Connection Pool
class DatabaseConnection:
    """Demonstrates class methods for managing shared resources (Singleton-like pattern)."""
    
    _instance = None
    _connection_pool = []
    max_connections = 5
    
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connected = False
    
    @classmethod
    def get_connection(cls, host: str = "localhost", port: int = 5432):
        """Factory method returning a shared connection.
        Use case: Connection pooling, resource management."""
        if len(cls._connection_pool) < cls.max_connections:
            conn = cls(host, port)
            conn.connected = True
            cls._connection_pool.append(conn)
            return conn
        else:
            # Return existing connection (simplified pooling)
            return cls._connection_pool[0]
    
    @classmethod
    def close_all_connections(cls):
        """Class-level cleanup operation.
        Use case: Application shutdown, resource cleanup."""
        for conn in cls._connection_pool:
            conn.connected = False
        cls._connection_pool.clear()
        print(f"Closed all {len(cls._connection_pool)} database connections")
    
    @classmethod
    def get_active_connections(cls) -> int:
        """Monitor class-level state.
        Use case: Health checks, monitoring dashboards."""
        return len([c for c in cls._connection_pool if c.connected])
    
    @staticmethod
    def validate_host(host: str) -> bool:
        """Validate input without needing instance/class context.
        Use case: Input validation, security checks."""
        # Simple validation: no special characters except dots and hyphens
        return bool(re.match(r'^[a-zA-Z0-9.-]+$', host))
    
    @staticmethod
    def parse_connection_string(conn_string: str) -> dict:
        """Parse connection string into components.
        Use case: Configuration parsing, string utilities."""
        # Format: "host:port/database"
        pattern = r'([^:]+):(\d+)/(.+)'
        match = re.match(pattern, conn_string)
        if match:
            return {
                'host': match.group(1),
                'port': int(match.group(2)),
                'database': match.group(3)
            }
        return {}
    
    def __repr__(self):
        status = "connected" if self.connected else "disconnected"
        return f"DatabaseConnection({self.host}:{self.port}, {status})"


# Example 3: Product Inventory System
class Product:
    """Demonstrates class methods for business logic and static methods for utilities."""
    
    tax_rate = 0.08  # 8% tax
    all_products = []
    
    def __init__(self, name: str, price: float, quantity: int, category: str):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category
        Product.all_products.append(self)
    
    @classmethod
    def from_barcode(cls, barcode: str):
        """Create product by looking up barcode.
        Use case: POS systems, inventory scanning."""
        # Simulated barcode lookup
        barcode_db = {
            "12345": ("Laptop", 999.99, 10, "Electronics"),
            "67890": ("Coffee Mug", 12.99, 100, "Kitchen"),
        }
        if barcode in barcode_db:
            return cls(*barcode_db[barcode])
        return None
    
    @classmethod
    def bulk_import(cls, products_data: List[dict]):
        """Create multiple products at once.
        Use case: Bulk imports, data migration."""
        imported = []
        for data in products_data:
            product = cls(**data)
            imported.append(product)
        return imported
    
    @classmethod
    def get_total_inventory_value(cls) -> float:
        """Calculate total value across all products.
        Use case: Financial reporting, analytics."""
        return sum(p.price * p.quantity for p in cls.all_products)
    
    @classmethod
    def find_by_category(cls, category: str) -> List['Product']:
        """Query class-level collection.
        Use case: Filtering, search functionality."""
        return [p for p in cls.all_products if p.category == category]
    
    @classmethod
    def update_tax_rate(cls, new_rate: float):
        """Update class-level configuration.
        Use case: Business rule changes, seasonal adjustments."""
        cls.tax_rate = new_rate
    
    @staticmethod
    def calculate_discount(price: float, discount_percent: float) -> float:
        """Calculate discounted price.
        Use case: Pricing calculations, promotions."""
        return price * (1 - discount_percent / 100)
    
    @staticmethod
    def format_currency(amount: float) -> str:
        """Format number as currency.
        Use case: Display formatting, report generation."""
        return f"${amount:,.2f}"
    
    @staticmethod
    def is_valid_sku(sku: str) -> bool:
        """Validate SKU format.
        Use case: Data validation, quality checks."""
        # SKU format: 3 letters + 5 digits
        return bool(re.match(r'^[A-Z]{3}\d{5}$', sku))
    
    def price_with_tax(self) -> float:
        """Instance method using class variable."""
        return self.price * (1 + Product.tax_rate)
    
    def __repr__(self):
        return f"Product('{self.name}', {Product.format_currency(self.price)}, qty: {self.quantity})"


# Example 4: Date and Time Utilities
class DateUtils:
    """Pure utility class - only static methods.
    Use case: Helper functions that don't need state."""
    
    @staticmethod
    def is_business_day(date: datetime) -> bool:
        """Check if date is a weekday.
        Use case: Business logic, scheduling systems."""
        return date.weekday() < 5  # Monday = 0, Friday = 4
    
    @staticmethod
    def get_business_days_between(start: datetime, end: datetime) -> int:
        """Count business days in date range.
        Use case: Project management, time tracking."""
        days = 0
        current = start
        while current <= end:
            if DateUtils.is_business_day(current):
                days += 1
            current += timedelta(days=1)
        return days
    
    @staticmethod
    def format_relative_time(date: datetime) -> str:
        """Get human-readable relative time.
        Use case: Social media, notifications."""
        now = datetime.now()
        diff = now - date
        
        if diff.days > 365:
            return f"{diff.days // 365} years ago"
        elif diff.days > 30:
            return f"{diff.days // 30} months ago"
        elif diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} hours ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} minutes ago"
        else:
            return "just now"
    
    @staticmethod
    def parse_flexible_date(date_string: str) -> Optional[datetime]:
        """Parse dates in multiple formats.
        Use case: User input handling, data import."""
        formats = [
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d-%m-%Y',
            '%Y/%m/%d',
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue
        return None


# Demo usage
if __name__ == "__main__":
    print("=" * 70)
    print("EXAMPLE 1: EMPLOYEE MANAGEMENT")
    print("=" * 70)
    
    # Regular constructor
    emp1 = Employee("Alice Smith", 75000, datetime(2020, 1, 15))
    print(f"Created: {emp1}")
    
    # Class method as alternative constructor
    emp2 = Employee.from_string("Bob Johnson-65000-2021-06-01")
    print(f"From string: {emp2}")
    
    # Class method from dictionary (like JSON API response)
    emp3 = Employee.from_dict({
        'name': 'Carol White',
        'salary': 85000,
        'hire_date': '2019-03-20'
    })
    print(f"From dict: {emp3}")
    
    # Static method for validation
    print(f"\nIs $50,000 valid salary? {Employee.is_valid_salary(50000)}")
    print(f"Is $25,000 valid salary? {Employee.is_valid_salary(25000)}")
    
    # Static method for calculations
    bonus = Employee.calculate_annual_bonus(75000, 4.0)
    print(f"Annual bonus for rating 4.0: ${bonus:,.2f}")
    
    # Class method accessing class data
    print(f"\nTotal employees: {Employee.get_employee_count()}")
    
    print("\n" + "=" * 70)
    print("EXAMPLE 2: DATABASE CONNECTION POOL")
    print("=" * 70)
    
    # Class method for resource management
    conn1 = DatabaseConnection.get_connection("db.example.com", 5432)
    conn2 = DatabaseConnection.get_connection("db.example.com", 5432)
    print(f"Connection 1: {conn1}")
    print(f"Connection 2: {conn2}")
    print(f"Active connections: {DatabaseConnection.get_active_connections()}")
    
    # Static method for validation
    print(f"\nIs 'db.example.com' valid host? {DatabaseConnection.validate_host('db.example.com')}")
    print(f"Is 'db@hack.com' valid host? {DatabaseConnection.validate_host('db@hack.com')}")
    
    # Static method for parsing
    parsed = DatabaseConnection.parse_connection_string("localhost:5432/mydb")
    print(f"Parsed connection string: {parsed}")
    
    print("\n" + "=" * 70)
    print("EXAMPLE 3: PRODUCT INVENTORY")
    print("=" * 70)
    
    # Regular constructor
    p1 = Product("Wireless Mouse", 29.99, 50, "Electronics")
    print(f"Created: {p1}")
    
    # Class method alternative constructor
    p2 = Product.from_barcode("12345")
    print(f"From barcode: {p2}")
    
    # Class method for bulk operations
    bulk_data = [
        {"name": "Notebook", "price": 5.99, "quantity": 200, "category": "Office"},
        {"name": "Pen Set", "price": 12.99, "quantity": 150, "category": "Office"},
    ]
    Product.bulk_import(bulk_data)
    
    # Class method for aggregation
    total_value = Product.get_total_inventory_value()
    print(f"\nTotal inventory value: {Product.format_currency(total_value)}")
    
    # Class method for querying
    electronics = Product.find_by_category("Electronics")
    print(f"Electronics products: {len(electronics)}")
    
    # Static methods for utilities
    discounted = Product.calculate_discount(29.99, 20)
    print(f"20% off $29.99: {Product.format_currency(discounted)}")
    print(f"Is 'ABC12345' valid SKU? {Product.is_valid_sku('ABC12345')}")
    
    print("\n" + "=" * 70)
    print("EXAMPLE 4: DATE UTILITIES")
    print("=" * 70)
    
    # Static utility methods
    today = datetime.now()
    print(f"Is today a business day? {DateUtils.is_business_day(today)}")
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 31)
    biz_days = DateUtils.get_business_days_between(start_date, end_date)
    print(f"Business days in January 2024: {biz_days}")
    
    past_date = datetime.now() - timedelta(days=45)
    print(f"45 days ago was: {DateUtils.format_relative_time(past_date)}")
    
    parsed_date = DateUtils.parse_flexible_date("2024/12/25")
    print(f"Parsed '2024/12/25': {parsed_date}")