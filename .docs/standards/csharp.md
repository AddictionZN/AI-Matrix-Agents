# C# Coding Standards

This document outlines our C# coding standards and best practices. Following these guidelines ensures consistency, readability, and maintainability across all C# codebases in the project.

## Table of Contents

1. [Microsoft Coding Conventions](#1-microsoft-coding-conventions)
2. [Naming Conventions](#2-naming-conventions)
3. [Layout and Formatting](#3-layout-and-formatting)
4. [Documentation](#4-documentation)
5. [Code Organization](#5-code-organization)
6. [SOLID Principles](#6-solid-principles)
7. [Exception Handling](#7-exception-handling)
8. [Null Handling](#8-null-handling)
9. [Modern C# Features](#9-modern-c-features)
10. [Testing Strategy](#10-testing-strategy)
11. [Code Quality Tools](#11-code-quality-tools)

## 1. Microsoft Coding Conventions

All C# code must follow [Microsoft's C# Coding Conventions](https://docs.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions) for consistent formatting and style.

## 2. Naming Conventions

### 2.1 Casing Standards
- `PascalCase` for namespaces, classes, methods, properties, public fields, constants, enums
- `camelCase` for local variables, parameters, private fields
- Prefix interfaces with "I" (e.g., `IDisposable`)
- Prefix private fields with underscore (e.g., `_privateField`)

### 2.2 Descriptive Naming
- Use clear, meaningful names that explain purpose
- Avoid abbreviations unless widely understood
- Method names should indicate actions (e.g., `CalculateTotal`, `GetUserData`)
- Boolean properties/variables should read as conditions (e.g., `IsValid`, `HasPermission`)

```csharp
// Correct
public class CustomerRepository
{
    private readonly DbContext _context;
    
    public CustomerRepository(DbContext context)
    {
        _context = context;
    }
    
    public async Task<Customer> GetCustomerByIdAsync(int customerId)
    {
        return await _context.Customers.FindAsync(customerId);
    }
}

// Incorrect
public class CustRepo
{
    private readonly DbContext context;
    
    public CustRepo(DbContext db)
    {
        context = db;
    }
    
    public async Task<Customer> Fetch(int id)
    {
        return await context.Customers.FindAsync(id);
    }
}
```

## 3. Layout and Formatting

- Use 4 spaces for indentation (not tabs)
- One statement per line
- One declaration per line
- Use braces for all control structures (even one-liners)
- Place braces on new lines
- Limit lines to a reasonable length (120 characters recommended)

```csharp
// Correct
if (condition)
{
    DoSomething();
}
else
{
    DoSomethingElse();
}

// Incorrect
if (condition) DoSomething();
else DoSomethingElse();
```

## 4. Documentation

- Use XML documentation comments for all public members
- Include `<summary>`, `<param>`, `<returns>`, `<exception>` tags as appropriate
- Write documentation that explains WHY, not just WHAT

```csharp
/// <summary>
/// Calculates the total price including tax.
/// </summary>
/// <param name="price">The base price without tax.</param>
/// <param name="taxRate">The tax rate as a decimal value (e.g., 0.07 for 7%).</param>
/// <returns>The total price including tax.</returns>
/// <exception cref="ArgumentException">Thrown when tax rate is negative.</exception>
public decimal CalculateTotalPrice(decimal price, decimal taxRate)
{
    if (taxRate < 0)
    {
        throw new ArgumentException("Tax rate cannot be negative.", nameof(taxRate));
    }
    
    return price * (1 + taxRate);
}
```

## 5. Code Organization

### 5.1 File Organization
- One primary class per file (with rare exceptions for tightly related small classes)
- Filename should match the primary class name

### 5.2 Class Member Organization
Organize class members in the following order:
1. Constants
2. Fields
3. Constructors
4. Properties
5. Methods
6. Nested types

Within each group, order by:
1. Public
2. Internal
3. Protected
4. Private

```csharp
public class User
{
    // Constants
    public const int MaxNameLength = 50;
    
    // Fields
    private readonly IUserRepository _userRepository;
    private string _cachedFullName;
    
    // Constructors
    public User(IUserRepository userRepository)
    {
        _userRepository = userRepository;
    }
    
    // Properties
    public int Id { get; set; }
    public string FirstName { get; set; }
    public string LastName { get; set; }
    
    // Methods
    public string GetFullName()
    {
        if (_cachedFullName == null)
        {
            _cachedFullName = $"{FirstName} {LastName}";
        }
        
        return _cachedFullName;
    }
    
    // Nested types
    public enum UserStatus
    {
        Active,
        Inactive,
        Suspended
    }
}
```

### 5.3 Using Directives
- Organize using directives alphabetically
- Place using directives at the top of file, outside of namespace
- Group System namespaces first, then others

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;

using MyCompany.Project.Models;
```

## 6. SOLID Principles

### 6.1 Single Responsibility Principle
- Each class should have one and only one reason to change
- Keep classes focused on a single responsibility

```csharp
// Correct: Separate responsibilities
public class OrderValidator
{
    public bool ValidateOrder(Order order) { /* ... */ }
}

public class OrderProcessor
{
    private readonly OrderValidator _validator;
    
    public OrderProcessor(OrderValidator validator)
    {
        _validator = validator;
    }
    
    public void Process(Order order)
    {
        if (_validator.ValidateOrder(order))
        {
            // Process the order
        }
    }
}

// Incorrect: Mixed responsibilities
public class OrderService
{
    public bool ValidateOrder(Order order) { /* ... */ }
    public void ProcessOrder(Order order) { /* ... */ }
    public void SaveOrder(Order order) { /* ... */ }
    public void EmailConfirmation(Order order) { /* ... */ }
}
```

### 6.2 Open/Closed Principle
- Classes should be open for extension but closed for modification
- Use interfaces and abstract classes to allow for extensibility

### 6.3 Liskov Substitution Principle
- Derived classes should be substitutable for their base classes
- Override methods should not alter the base behavior unexpectedly

### 6.4 Interface Segregation Principle
- Many specific interfaces are better than one general interface
- Clients should not be forced to depend on methods they do not use

```csharp
// Correct: Segregated interfaces
public interface IOrderReader
{
    Order GetById(int id);
    IEnumerable<Order> GetAll();
}

public interface IOrderWriter
{
    void Create(Order order);
    void Update(Order order);
    void Delete(int id);
}

// Incorrect: Fat interface
public interface IOrderRepository
{
    Order GetById(int id);
    IEnumerable<Order> GetAll();
    void Create(Order order);
    void Update(Order order);
    void Delete(int id);
    IEnumerable<Order> GetByCustomerId(int customerId);
    IEnumerable<Order> GetByDateRange(DateTime start, DateTime end);
    void ProcessPayment(int orderId, Payment payment);
    void GenerateInvoice(int orderId);
}
```

### 6.5 Dependency Inversion Principle
- Depend on abstractions, not concretions
- High-level modules should not depend on low-level modules

```csharp
// Correct: Depending on abstraction
public class NotificationService
{
    private readonly IMessageSender _messageSender;
    
    public NotificationService(IMessageSender messageSender)
    {
        _messageSender = messageSender;
    }
    
    public void NotifyUser(User user, string message)
    {
        _messageSender.SendMessage(user.Email, message);
    }
}

// Incorrect: Depending on concrete implementation
public class NotificationService
{
    public void NotifyUser(User user, string message)
    {
        var emailSender = new EmailSender();
        emailSender.SendEmail(user.Email, message);
    }
}
```

## 7. Exception Handling

- Use specific exception types rather than broad exceptions
- Include relevant information in exception messages
- Catch exceptions at the appropriate level of abstraction
- Use exception filters where appropriate
- Avoid swallowing exceptions without logging

```csharp
// Correct
public Customer GetCustomer(int id)
{
    try
    {
        return _repository.GetCustomerById(id);
    }
    catch (DatabaseConnectionException ex)
    {
        _logger.LogError(ex, "Database connection failed while retrieving customer {CustomerId}", id);
        throw new ServiceUnavailableException("Unable to connect to customer database", ex);
    }
    catch (EntityNotFoundException)
    {
        _logger.LogInformation("Customer {CustomerId} not found", id);
        return null;
    }
}

// Incorrect
public Customer GetCustomer(int id)
{
    try
    {
        return _repository.GetCustomerById(id);
    }
    catch (Exception)
    {
        return null;  // Swallowing exception without logging
    }
}
```

## 8. Null Handling

### 8.1 Nullable Reference Types
- Enable nullable reference types in projects (.NET 6+)
- Use `?` suffix for nullable reference types

```csharp
// In .csproj or at file level: #nullable enable
public class User
{
    public string Name { get; set; } = ""; // Non-nullable, must be initialized
    public string? MiddleName { get; set; } // Explicitly nullable
}
```

### 8.2 Null Checking
- Use null-conditional operator (`?.`) for safe member access
- Use null-coalescing operator (`??`) to provide defaults
- Use `ArgumentNullException.ThrowIfNull()` (.NET 6+) for parameter validation

```csharp
// Correct
public string GetFullName(User? user)
{
    ArgumentNullException.ThrowIfNull(user);
    
    return $"{user.FirstName} {user.LastName}";
}

public string GetDisplayName(User? user)
{
    return user?.DisplayName ?? "Guest";
}

// Incorrect
public string GetFullName(User user)
{
    if (user == null)
    {
        throw new ArgumentNullException(nameof(user));
    }
    
    if (user.FirstName == null)
    {
        return user.LastName;
    }
    else if (user.LastName == null)
    {
        return user.FirstName;
    }
    else
    {
        return user.FirstName + " " + user.LastName;
    }
}
```

## 9. Modern C# Features

Utilize modern C# features to write more concise, readable code:

### 9.1 Expression-Bodied Members
```csharp
// Shorter syntax for simple methods
public decimal CalculateTotal(decimal price, decimal tax) => price * (1 + tax);

// Properties
public string FullName => $"{FirstName} {LastName}";
```

### 9.2 Pattern Matching
```csharp
// Type patterns
public string GetDescription(object item) => item switch
{
    Person p => $"Person: {p.Name}, {p.Age} years old",
    Order o => $"Order: {o.OrderNumber}, ${o.Total}",
    null => "null",
    _ => item.ToString() ?? string.Empty
};

// Property patterns
public string GetDeliveryTime(Order order) => order.Status switch
{
    OrderStatus.Pending => "Processing order",
    OrderStatus.Shipped { ExpressDelivery: true } => "1-2 days",
    OrderStatus.Shipped => "3-5 days",
    OrderStatus.Delivered => "Already delivered",
    _ => "Unknown"
};
```

### 9.3 Target-Typed New Expressions
```csharp
// Concise object creation
CustomerRepository repository = new();
```

### 9.4 Records for Immutable Data
```csharp
// Immutable data class with value-based equality
public record OrderSummary(int Id, string CustomerName, decimal Total);
```

## 10. Testing Strategy

### 10.1 Unit Testing Guidelines
- Use a consistent testing framework (xUnit, NUnit, or MSTest)
- Follow the Arrange-Act-Assert pattern
- Test one thing per test method
- Use descriptive test method names (e.g., `Should_ReturnNull_When_IdIsZero`)

```csharp
// Using xUnit
public class CustomerServiceTests
{
    [Fact]
    public void GetCustomerById_ExistingCustomer_ReturnsCustomer()
    {
        // Arrange
        var repository = new Mock<ICustomerRepository>();
        var customer = new Customer { Id = 1, Name = "John Doe" };
        repository.Setup(r => r.GetById(1)).Returns(customer);
        
        var service = new CustomerService(repository.Object);
        
        // Act
        var result = service.GetCustomerById(1);
        
        // Assert
        Assert.NotNull(result);
        Assert.Equal("John Doe", result.Name);
    }
    
    [Fact]
    public void GetCustomerById_NonExistingCustomer_ReturnsNull()
    {
        // Arrange
        var repository = new Mock<ICustomerRepository>();
        repository.Setup(r => r.GetById(It.IsAny<int>())).Returns((Customer)null);
        
        var service = new CustomerService(repository.Object);
        
        // Act
        var result = service.GetCustomerById(999);
        
        // Assert
        Assert.Null(result);
    }
}
```

### 10.2 Mock Frameworks
- Use a mock framework (e.g., Moq, NSubstitute) for creating test doubles
- Mock only what's necessary for the test

### 10.3 Test Data
- Use factory methods or the builder pattern for creating test data
- Avoid sharing mutable test data between tests

## 11. Code Quality Tools

Enforce these standards using the following tools:

| Tool | Purpose | Configuration |
|------|---------|--------------|
| StyleCop | Code style enforcement | `stylecop.json` in project root |
| .editorconfig | Editor formatting rules | `.editorconfig` in solution root |
| SonarQube/SonarLint | Static code analysis | Rules configuration in CI pipeline |
| ReSharper/Rider | Code inspections | Team-shared settings |
| .NET Analyzers | Built-in code analysis | Enable in project file |

Run these tools as part of your development workflow and CI/CD pipeline.