def calculate_simple_interest(principal, rate, time):
    """
    Function to calculate simple interest.
    
    Args:
    principal (float): The principal amount.
    rate (float): The rate of interest (in percentage).
    time (float): The time period (in years).
    
    Returns:
    float: The simple interest.
    """
    interest = (principal * rate * time) / 100
    return interest

def calculate_total_amount(principal, interest):
    """
    Function to calculate total amount.
    
    Args:
    principal (float): The principal amount.
    interest (float): The simple interest.
    
    Returns:
    float: The total amount.
    """
    total_amount = principal + interest
    return total_amount

if __name__ == "__main__":
    # Taking user input for principal amount, rate of interest, and time period
    principal_amount = float(input("Enter the principal amount: "))
    rate_of_interest = float(input("Enter the rate of interest (in percentage): "))
    time_period = float(input("Enter the time period (in years): "))
    
    # Calculating simple interest
    simple_interest = calculate_simple_interest(principal_amount, rate_of_interest, time_period)
    
    # Calculating total amount
    total_amount = calculate_total_amount(principal_amount, simple_interest)
    
    # Displaying the results
    print(f"Simple Interest: {simple_interest}")
    print(f"Total Amount: {total_amount}")
