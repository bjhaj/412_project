import math

# Dictionary to store coefficients based on sex and competition type
coefficients = {
    'men': {
        'equipped_powerlifting': (1236.25115, 1449.21864, 0.01644),
        'classic_powerlifting': (1199.72839, 1025.18162, 0.00921),
        'equipped_bench_press': (381.22073, 733.79378, 0.02398),
        'classic_bench_press': (320.98041, 281.40258, 0.01008),
    },
    'women': {
        'equipped_powerlifting': (758.63878, 949.31382, 0.02435),
        'classic_powerlifting': (610.32796, 1045.59282, 0.03048),
        'equipped_bench_press': (221.82209, 357.00377, 0.02937),
        'classic_bench_press': (142.40398, 442.52671, 0.04724),
    }
}

def calculate_glp(sex, competition_type, body_weight, result):
    # Fetch A, B, C based on input sex and competition type
    A, B, C = coefficients[sex][competition_type]
    
    # Calculate the exponent part of the formula
    exponent = 100 / (A - (B * math.exp(C * -1 * body_weight)))
    
    # Calculate GLP
    return round(result * exponent, 6)

# Example usage:
sex = 'women'  # 'men' or 'women'
competition_type = 'classic_powerlifting'  # competition type
body_weight = 68.9  # Athlete's body weight in kg
result = 600.0  # Total weight lifted in kg

glp = calculate_glp(sex, competition_type, body_weight, result)
print(f"The GLP is: {glp}")
