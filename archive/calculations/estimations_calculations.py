from typing import List, Dict, Any


def calculate_line_item(quantity: float, unit_price: float) -> float:
    """
    Calculate the line subtotal for a single cost item.
    
    Args:
        quantity (float): The quantity of the cost item.
        unit_price (float): The price per unit.
        
    Returns:
        float: The computed line subtotal.
    """
    return quantity * unit_price


def calculate_subtotal(line_totals: List[float]) -> float:
    """
    Calculate the subtotal by summing up all line item totals.
    
    Args:
        line_totals (List[float]): A list of line item totals.
        
    Returns:
        float: The subtotal amount.
    """
    return sum(line_totals)


def calculate_tax(subtotal: float, tax_rate: float) -> float:
    """
    Calculate the tax amount based on the subtotal and a tax rate.
    
    Args:
        subtotal (float): The subtotal amount.
        tax_rate (float): The tax rate (e.g., 0.07 for 7%).
        
    Returns:
        float: The tax amount.
    """
    return subtotal * tax_rate


def calculate_grand_total(subtotal: float, tax: float) -> float:
    """
    Calculate the grand total by adding the subtotal and tax.
    
    Args:
        subtotal (float): The subtotal amount.
        tax (float): The tax amount.
        
    Returns:
        float: The grand total.
    """
    return subtotal + tax


def generate_estimation_summary(
    line_items: List[Dict[str, Any]],
    tax_rate: float = 0.0
) -> Dict[str, Any]:
    """
    Generate a comprehensive estimation summary from a list of cost items.
    
    Each cost item in `line_items` should be a dictionary with at least the following keys:
      - 'description': A description of the cost item.
      - 'quantity': The quantity for the cost item.
      - 'unit_price': The unit price for the cost item.
    
    The function calculates:
      - A computed line subtotal for each item (quantity * unit_price)
      - An overall subtotal as the sum of all line subtotals
      - The tax amount (based on the provided tax_rate)
      - The grand total (subtotal + tax)
    
    Args:
        line_items (List[Dict[str, Any]]): A list of cost item dictionaries.
        tax_rate (float): Tax rate to apply (default is 0.0 if no tax).
        
    Returns:
        Dict[str, Any]: A dictionary summarizing:
                        - "line_items": List of cost items with computed "line_subtotal"
                        - "subtotal": Total of all line item subtotals
                        - "tax": Computed tax based on subtotal and tax rate
                        - "grand_total": Subtotal plus tax
    """
    computed_items = []
    line_totals = []

    for item in line_items:
        # Ensure proper conversion of quantity and unit_price to float values.
        qty = float(item.get("quantity", 0))
        up = float(item.get("unit_price", 0))
        line_total = calculate_line_item(qty, up)
        
        computed_items.append({
            "description": item.get("description", ""),
            "quantity": qty,
            "unit_price": up,
            "line_subtotal": line_total
        })
        line_totals.append(line_total)
    
    subtotal = calculate_subtotal(line_totals)
    tax = calculate_tax(subtotal, tax_rate)
    grand_total = calculate_grand_total(subtotal, tax)
    
    return {
        "line_items": computed_items,
        "subtotal": subtotal,
        "tax": tax,
        "grand_total": grand_total
    }