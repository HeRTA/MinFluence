import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Set MPL plot parameters
plt.rcParams["figure.figsize"] = (25,20)
plt.rcParams.update({'font.size': 24})

# Define headers and null
headers = ['rmp_dm', 'rmp_width', 'rmp_flux', 'null']

dm = []
width = []
flux = []

# Load FRBCAT database
with open('frbcat.csv') as frb_db:
    for line in frb_db:
        # Strip headers and nulls
        if not any(headers in line for headers in headers):
            # Strip quotes
            line = line.replace('"', '')

            # Store FRB parameters
            dm.append(line.split(',')[0].partition('&')[0])
            width.append(line.split(',')[1].partition('&')[0])
            flux.append(line.split(',')[2].partition('&')[0])

# Convert to floats
dm = [float(i) for i in dm]
width = [float(i) for i in width]
flux = [float(i) for i in flux]

# Scatter Plot
fig, ax = plt.subplots()

# Set minimum detectable FRB fluence (boresight)
F_min_bs = 11.5090182
point1_bs = [F_min_bs*1e10, 1*1e-10]
point2_bs = [1*1e-10, F_min_bs*1e10]

# Set minimum detectable FRB fluence (beam FWHM)
F_min_hpbw = 2*F_min_bs
point1_hpbw = [F_min_hpbw*1e10, 1*1e-10]
point2_hpbw = [1*1e-10, F_min_hpbw*1e10]

# Define line from points (boresight)
x_bs = [point1_bs[0], point2_bs[0]]
y_bs = [point1_bs[1], point2_bs[1]]

# Define line from points (beam FWHM)
x_hpbw = [point1_hpbw[0], point2_hpbw[0]]
y_hpbw = [point1_hpbw[1], point2_hpbw[1]]

# Plot fluence detection limits
ax.plot(x_bs, y_bs, c='#ff7f0e', lw=4, label='Boresight (11.5 Jy ms)')
ax.plot(x_hpbw, y_hpbw, c='#2ca02c', lw=4, label='FWHM (23 Jy ms)')

ax.fill_between(x_hpbw, y_hpbw, y2=1000, facecolor='green', alpha=0.2)
ax.fill_between(x_bs, y_bs, y2=1000, facecolor='orange', alpha=0.1)

# Plot previous FRB events
ax.scatter(width, flux, alpha=0.70, label = 'Previous FRB events', s=200)

# Enable legend
ax.legend()

# Enable grid
ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.7)

# Add title
ax.set_title('HeRTA | Minimum detectable FRB fluence', fontsize=44, y=1.01)

# Set axis limits
ax.set_xlim(10**-1,10**4)
ax.set_ylim(10**-2,10**3)
ax.set_xscale('log')
ax.set_yscale('log')

# Set axis labels
ax.set_xlabel('Pulse Width (ms)', fontsize=32)
ax.set_ylabel('Peak Flux Density (Jy)', fontsize=32)

# Remove top and right border
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Save plot to file
plt.savefig('plot.png', bbox_inches='tight')