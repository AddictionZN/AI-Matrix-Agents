from typing import List, Dict


def compute_net_cash_flow(inflows: List[float], outflows: List[float]) -> List[float]:
    """
    Compute the net cash flow for each period by subtracting outflows from inflows.
    
    Args:
        inflows (List[float]): A list of cash inflows per period.
        outflows (List[float]): A list of cash outflows per period.
        
    Returns:
        List[float]: A list of net cash flows for each period.
    
    Raises:
        ValueError: If the lengths of the inflows and outflows lists do not match.
    """
    if len(inflows) != len(outflows):
        raise ValueError("The number of inflows must equal the number of outflows.")
    return [inflow - outflow for inflow, outflow in zip(inflows, outflows)]


def compute_cumulative_flow(net_flows: List[float]) -> List[float]:
    """
    Calculate the cumulative cash flow over the given periods.
    
    Args:
        net_flows (List[float]): A list of net cash flows for each period.
        
    Returns:
        List[float]: A cumulative cash flow list.
    """
    cumulative = []
    total = 0.0
    for flow in net_flows:
        total += flow
        cumulative.append(total)
    return cumulative


def apply_discount_rate(cash_flows: List[float], discount_rate: float, periods: List[int] = None) -> List[float]:
    """
    Apply a discount rate to each cash flow to determine its present value.
    
    Args:
        cash_flows (List[float]): A list of cash flows (e.g., net flows) for each period.
        discount_rate (float): The discount rate per period (e.g., for monthly discounting, an annual rate divided by 12).
        periods (List[int], optional): A list of period indices (starting at 1). If not provided, periods will be assumed to sequentially start at 1.
    
    Returns:
        List[float]: A list of discounted cash flows for each period.
    
    Raises:
        ValueError: If the length of periods does not match the length of cash_flows.
    """
    if periods is None:
        periods = list(range(1, len(cash_flows) + 1))
    if len(cash_flows) != len(periods):
        raise ValueError("Length of cash_flows and periods must match")
    return [cf / ((1 + discount_rate) ** period) for cf, period in zip(cash_flows, periods)]


def compute_cumulative_discounted_cash_flow(discounted_cash_flows: List[float]) -> List[float]:
    """
    Compute the cumulative sum of discounted cash flows.
    
    Args:
        discounted_cash_flows (List[float]): A list of discounted cash flows.
        
    Returns:
        List[float]: A list showing the cumulative discounted cash flow for each period.
    """
    cumulative_discounted = []
    total = 0.0
    for dc in discounted_cash_flows:
        total += dc
        cumulative_discounted.append(total)
    return cumulative_discounted


def generate_cash_flow_statement(
    inflows: List[float],
    outflows: List[float],
    discount_rate: float,
    periods: List[int] = None
) -> Dict[str, List[float]]:
    """
    Generate a comprehensive cash flow statement that includes:
      - Net cash flow per period
      - Cumulative cash flow
      - Discounted cash flow per period
      - Cumulative discounted cash flow
      
    Args:
        inflows (List[float]): Monthly cash inflows.
        outflows (List[float]): Monthly cash outflows.
        discount_rate (float): Discount rate per period.
        periods (List[int], optional): Period indices. Defaults to sequential numbering starting at 1.
        
    Returns:
        Dict[str, List[float]]: A dictionary with keys:
            - "net_cash_flow"
            - "cumulative_cash_flow"
            - "discounted_cash_flow"
            - "cumulative_discounted_cash_flow"
    """
    net_flows = compute_net_cash_flow(inflows, outflows)
    cumulative_flows = compute_cumulative_flow(net_flows)
    discounted_flows = apply_discount_rate(net_flows, discount_rate, periods)
    cumulative_discounted = compute_cumulative_discounted_cash_flow(discounted_flows)
    
    return {
        "net_cash_flow": net_flows,
        "cumulative_cash_flow": cumulative_flows,
        "discounted_cash_flow": discounted_flows,
        "cumulative_discounted_cash_flow": cumulative_discounted,
    }