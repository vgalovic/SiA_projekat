import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# System parameters
V = 4.5
J = 0.000000807
b = 0.000000414
K = 0.0059
R = 1.72
L = 0.000106

# Transfer function numerator and denominator coefficients
numerator = [V * K]
denominator = [J * L, (J * R + b * L), (b * R + K**2)]

# Create the transfer function
P_motor = signal.TransferFunction(numerator, denominator)

# Time vector for simulation
total_time = 0.25  # Total simulation time in seconds
num_points = 10000  # Number of points for simulation

# Compute the step response
time = np.linspace(0, total_time, num_points)
time, response = signal.step(P_motor, T=time)

# Calculate settling time to 2% tolerance
final_value = response[-1]  # Final value of the step response
tolerance = 0.02 * final_value  # 2% of the final value
settling_time = None

# Find the index where the response is within the tolerance
for idx, y in enumerate(response):
    if abs(y - final_value) < tolerance:
        settling_time = time[idx]
        break

# Find the coordinates around settling time
settling_idx = np.abs(time - settling_time).argmin()
settling_time_coord = time[settling_idx]
settling_response_coord = response[settling_idx]

# Plotting the step response
plt.figure(figsize=(8, 6))
plt.plot(time, response, linewidth=2, label='Step Response')
plt.axvline(x=settling_time, color='r', linestyle='--', label=f'Settling Time: {settling_time:.4f} sec')
plt.plot(settling_time_coord, settling_response_coord, 'ro', label='Settling Time Coordinate')
plt.grid(True)
plt.title('Step Response of $P_{\mathrm{motor}}$')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.legend()
plt.tight_layout()
plt.show()

