from csv import reader
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

### Set MPL plot parameters
# Selectable SVG text
plt.rcParams['svg.fonttype'] = 'none'

# Use TeX
plt.rcParams['text.usetex'] = True

# Set figsize
plt.rcParams["figure.figsize"] = (26,20)
plt.rcParams["figure.dpi"] = 300

# Set xtick size
plt.rcParams['xtick.major.size'] = 20
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['xtick.minor.size'] = 10
plt.rcParams['xtick.minor.width'] = 2

# Set ytick size
plt.rcParams['ytick.major.size'] = 20
plt.rcParams['ytick.major.width'] = 2
plt.rcParams['ytick.minor.size'] = 10
plt.rcParams['ytick.minor.width'] = 2

### Load data
# Initiate empty parameter lists
dm = []
flux = []
width = []

# Read FRBSTATS CSV catalogue
with open('catalogue.csv', 'r') as read_obj:
	csv_reader = reader(read_obj)
	header = next(csv_reader)
	# Skip header
	if header != None:
		for row in csv_reader:
			dm.append(row[9])
			flux.append(row[10])
			width.append(row[11])

### Pre-process data
# Pick out incompatible rows
idx_mask = set()
for idx, val in enumerate(dm):
        try:
                dm[idx] = float(val)
        except ValueError:
                idx_mask.add(idx)

for idx, val in enumerate(flux):
	try:
		flux[idx] = float(val)
	except ValueError:
		idx_mask.add(idx)

for idx, val in enumerate(width):
        try:
                width[idx] = float(val)
        except ValueError:
                idx_mask.add(idx)

# Dump rows with missing data
for idx in sorted(idx_mask, reverse=True):
	del dm[idx]
	del flux[idx]
	del width[idx]

### Initiate plot
# Apply grid
plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.9)

### HeRTA
# Set minimum detectable FRB fluence (boresight)
F_min_bs = 8.056312742 # Threshold: S:N > 7
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
plt.plot(x_bs, y_bs, c='#ff7f0e', lw=4, label=r'$\mathrm{Boresight \ (11.5 \ Jy \ ms)}$', alpha=0.7, zorder=20)
plt.plot(x_hpbw, y_hpbw, c='#2ca02c', lw=4, label=r'$\mathrm{FWHM \ (23 \ Jy \ ms)}$', alpha=0.7, zorder=20)
plt.fill_between(x_hpbw, y_hpbw, y2=1000, facecolor='green', alpha=0.2)
plt.fill_between(x_bs, y_bs, y2=1000, facecolor='orange', alpha=0.1)
legend = plt.legend(fontsize=37)
legend.get_frame().set_alpha(None)
legend.get_frame().set_facecolor((1, 1, 1, 0.7))

plt.annotate(r'$\mathrm{Threshold} \colon \ \mathrm{S}/\mathrm{N} \geq 7$', xy=(1005, 1045),
	     xycoords='axes points', size=40, ha='left', va='bottom', color='black')

# Scatter plot
plt.scatter(width, flux, c=dm, s=500, alpha=0.7, edgecolor='black', linewidth=2, cmap='plasma', zorder=10)

# Set colorbar
cbar = plt.colorbar()
cbar.set_label(r'$\mathrm{Dispersion \ Measure \ }\Bigg[\mathrm{pc \ cm}^{-3}\Bigg]$', fontsize=52)
cbar.ax.tick_params(labelsize=42)

# Remove alpha colorbar component
cbar.set_alpha(1)
cbar.draw_all()

# Set axis labels & figure title
plt.xlabel(r'$\mathrm{Burst \ Width \ [ms]}$', fontsize=52)
plt.ylabel(r'$\mathrm{Peak \ Flux \ Density \ [Jy]}$', fontsize=52)
plt.title(r'$\mathrm{FRB \ Fluence \ Distribution}$', fontsize=72, y=1.01)

# Set log-log scaling
plt.xscale('log')
plt.yscale('log')

# Set ylim
plt.xlim(10**-1,10**4)
plt.ylim(10**-2,10**3)

# Set tick size
plt.xticks(fontsize=42, y=-0.005)
plt.yticks(fontsize=42)

# Remove top and right border
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.gca().xaxis.set_tick_params(top='off',which='both')
plt.gca().yaxis.set_tick_params(right='off',which='both')

plt.tight_layout()

# Save data to a scalable format
plt.savefig('plot.png')#, format='svg')
