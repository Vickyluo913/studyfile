def sort_performance(components, isRainbow, rainbowCheapestDelivery):
    if isRainbow:
        if rainbowCheapestDelivery:
            # Sort by forward adjustment first if cheapest delivery is required
            components.sort(key=lambda x: x.fwdAdj)
        
        # Then sort by performance in descending order
        components.sort(key=lambda x: x.perf, reverse=True)

        # Handle cases with the same performance
        i = 0
        while i < len(components) - 1:
            if components[i].perf == components[i + 1].perf:
                start = i
                while i < len(components) - 1 and components[i].perf == components[i + 1].perf:
                    i += 1
                # Sort by assetIdx within the same performance block to resolve ties
                components[start:i+1] = sorted(components[start:i+1], key=lambda x: x.assetIdx)
            i += 1
    else:
        # If not a rainbow option, just sort by assetIdx
        components.sort(key=lambda x: x.assetIdx)


def calculate_values(components, aggregation_mode, in_the_money_cond):
    total_value = 0
    for component in components:
        dist = basket_distance(component, aggregation_mode)
        component.isITM = is_in_the_money(dist, in_the_money_cond)
        
        if component.isITM:
            physical_value = component.perf * component.physicalRatio + component.fwdAdj
            cash_value = component.perf * (1 - component.physicalRatio)
            value = component.participation * (physical_value + cash_value - component.strike)
            total_value += component.weight * value

    return total_value


def simulate():
    components = [
        ComponentPerfAdj(1, 100, 10, 90, 0.5, 0.8, 0.2),
        ComponentPerfAdj(2, 100, 20, 85, 0.4, 0.7, 0.3),
        ComponentPerfAdj(3, 95, 15, 88, 0.6, 0.9, 0.1),
        ComponentPerfAdj(4, 105, 25, 80, 0.7, 0.6, 0.4)
    ]
    isRainbow = True
    rainbowCheapestDelivery = True  # Controls the fwdAdj sorting
    is_doing_past = False
    legal_weights = [0.1, 0.2, 0.1, 0.2]
    risk_weights = [0.15, 0.25, 0.1, 0.3]

    current_weights = weights(is_doing_past, legal_weights, risk_weights)
    for idx, comp in enumerate(components):
        comp.weight = current_weights[idx]

    sort_performance(components, isRainbow, rainbowCheapestDelivery)

    aggregation_mode = "OPTION_ON_BASKET"
    in_the_money_cond = "HIGHER"
    total_value = calculate_values(components, aggregation_mode, in_the_money_cond)
    print("Total Value Computed:", total_value)

simulate()