#%%
'''
This BarrierOption class calculates the price of barrier options with knock-in or knock-out features. Here's an explanation of the key parts:

__init__: Initializes the option parameters including the current stock price (S), strike price (K), risk-free rate (r), time to maturity (T), volatility (sigma), barrier level (barrier), option type (option_type), and barrier type (barrier_type).

d1 and d2: Calculate the components of the Black-Scholes formula.

vanilla_option_price: Calculates the price of a vanilla European option using the Black-Scholes formula.

barrier_option_price: Calculates the price of a barrier option. For a knock-in barrier option, adjusts the vanilla option price based on whether the barrier has been hit. For a knock-out barrier option, adjusts the vanilla option price based on whether the barrier has not been hit.

Example usage: Creates an instance of the BarrierOption class with given parameters and prints the option price.

This class demonstrates a more advanced use case of defining a class in Python, implementing complex financial calculations for barrier options with different barrier types.
'''
import numpy as np
from scipy.stats import norm

class BarrierOption:
    def __init__(self, S, K, r, T, sigma, barrier, option_type, barrier_type):
        self.S = S  # Current stock price
        self.K = K  # Strike price
        self.r = r  # Risk-free rate
        self.T = T  # Time to maturity
        self.sigma = sigma  # Volatility
        self.barrier = barrier  # Barrier level
        self.option_type = option_type  # Option type (call or put)
        self.barrier_type = barrier_type  # Barrier type (knock-in or knock-out)

    def d1(self):
        return (np.log(self.S / self.K) + (self.r + (self.sigma ** 2) / 2) * self.T) / (self.sigma * np.sqrt(self.T))

    def d2(self):
        return self.d1() - self.sigma * np.sqrt(self.T)

    def vanilla_option_price(self):
        if self.option_type == "call":
            return self.S * norm.cdf(self.d1()) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2())
        elif self.option_type == "put":
            return self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2()) - self.S * norm.cdf(-self.d1())

    def barrier_option_price(self):
        if self.barrier_type == "knock-in":
            if self.option_type == "call":
                return self.vanilla_option_price() * (norm.cdf(self.d2()) - norm.cdf((self.d1() - 2 * np.log(self.barrier / self.S) / (self.sigma * np.sqrt(self.T)))))
            elif self.option_type == "put":
                return self.vanilla_option_price() * (norm.cdf(-self.d2()) - norm.cdf((-self.d1() - 2 * np.log(self.barrier / self.S) / (self.sigma * np.sqrt(self.T)))))
        elif self.barrier_type == "knock-out":
            if self.option_type == "call":
                return self.vanilla_option_price() - (self.barrier / self.S) ** ((2 * self.r) / (self.sigma ** 2)) * self.vanilla_option_price() * norm.cdf(self.d2() - self.sigma * np.sqrt(self.T))
            elif self.option_type == "put":
                return self.vanilla_option_price() + (self.barrier / self.S) ** ((2 * self.r) / (self.sigma ** 2)) * self.vanilla_option_price() * norm.cdf(-self.d2() + self.sigma * np.sqrt(self.T))

#%%
# Example usage:
S = 100  # Current stock price
K = 100  # Strike price
r = 0.05  # Risk-free rate
T = 1  # Time to maturity
sigma = 0.2  # Volatility
barrier = 110  # Barrier level
option_type = "call"  # Option type (call or put)
barrier_type = "knock-in"  # Barrier type (knock-in or knock-out)

option = BarrierOption(S, K, r, T, sigma, barrier, option_type, barrier_type)
print("Option price:", option.barrier_option_price())

# %%
