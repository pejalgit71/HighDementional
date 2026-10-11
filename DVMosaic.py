import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.graphics.mosaicplot import mosaic
import matplotlib.pyplot as plt
from itertools import product
from collections import Counter
import statsmodels.formula.api as smf

# Streamlit title
st.title("Simulated Detergent Preference Study (Cox & Snell, 1991)")

# Define categorical levels
water_softness_levels = ['soft', 'medium', 'hard']
temperature_levels = ['low', 'high']
m_user_levels = ['yes', 'no']

# Simulate dataset with interaction effects
np.random.seed(42)
data = []

for w in water_softness_levels:
    for t in temperature_levels:
        for mu in m_user_levels:
            # Base probability
            if mu == 'yes':
                p_M = 0.7
            else:
                p_M = 0.4

            # Add interaction effects
            if w == 'hard' and t == 'low':
                p_M += 0.15
            elif w == 'soft' and t == 'high':
                p_M -= 0.1

            p_M = np.clip(p_M, 0, 1)

            # Simulate 40 samples per combination
            n = 40
            preferences = np.random.choice(['M', 'X'], size=n, p=[p_M, 1 - p_M])
            for pref in preferences:
                data.append([w, t, mu, pref])

# Create DataFrame
df = pd.DataFrame(data, columns=['Water Softness', 'Temperature', 'M-user', 'Preference'])
df.rename(columns={'Water Softness': 'Water_Softness', 'M-user': 'M_user'}, inplace=True)

# Prepare data for mosaic plot
def mosaic_data(df):
    grouped = Counter([tuple(row) for row in df[['Water_Softness', 'Temperature', 'M_user', 'Preference']].values])
    return grouped

# Define highlight colors for binary factor
def highlight_properties(key):
    # Last variable is Preference (binary: M or X)
    if key[-1] == 'M':
        color = '#4c72b0'  # blue for M
    else:
        color = '#dd8452'  # orange for X
    return {'color': color, 'edgecolor': 'white', 'alpha': 0.85}

# Plot mosaic with highlighting for last variable
def plot_mosaic(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    mosaic(
        data,
        ax=ax,
        labelizer=lambda k: "",  # suppress small labels inside cells
        properties=highlight_properties,
        title="Mosaic Plot — Highlighted Binary Factor (Preference)",
    )

    # Add legend manually for clarity
    handles = [
        plt.Rectangle((0, 0), 1, 1, color='#4c72b0', alpha=0.85, label='Preference = M'),
        plt.Rectangle((0, 0), 1, 1, color='#dd8452', alpha=0.85, label='Preference = X'),
    ]
    ax.legend(handles=handles, loc='upper right', frameon=False)

    plt.xlabel("Conditioning: Water Softness × Temperature × M_user")
    plt.ylabel("Preference (Binary Factor Highlighted)")
    plt.tight_layout()
    return fig

# Generate and display mosaic plot
mosaic_data_dict = mosaic_data(df)
mosaic_fig = plot_mosaic(mosaic_data_dict)
st.pyplot(mosaic_fig)

# Show sample data
st.subheader("Sample of Simulated Data")
st.dataframe(df.head(10))

# Logistic regression analysis
st.subheader("Logistic Regression Analysis")

df['Preference_M'] = (df['Preference'] == 'M').astype(int)
model = smf.logit("Preference_M ~ C(Water_Softness) * C(Temperature) + C(M_user)", data=df).fit(disp=False)

st.text(model.summary())

st.markdown("""
### Interpretation
- **Water_Softness × Temperature:** Interaction terms show if detergent preference depends on water hardness and temperature jointly.
- **M_user:** Previous brand usage effect.
- The **highlighted binary mosaic** visually links Preference (M or X) across all conditioning combinations.
""")

with st.expander("Explanation of Simulation"):
    st.markdown("""
    - The **first variables (Water Softness, Temperature)** condition the visualization — they are plotted first.
    - The **interaction of M_user × Preference** forms the last two axes.
    - The **last variable Preference** is binary, so it’s visually *linked* using color shading (like in R’s `vcd` mosaic).
    - This structure helps interpret interactions efficiently without clutter.
    """)

st.title("Car MPG vs Weight by Drivetrain Type")

# Simulated data
np.random.seed(42)
n = 90
weights = np.random.uniform(2000, 5000, n)
drivetrain = np.random.choice(['FWD', 'RWD', 'AWD'], size=n, p=[0.4, 0.4, 0.2])

# Base MPG decreases with weight
mpg = 55 - 0.007 * weights

# Adjust MPG by drivetrain
mpg_adjustment = {'FWD': 3, 'RWD': 0, 'AWD': -3}
mpg = [m + mpg_adjustment[d] + np.random.normal(0, 2) for m, d in zip(mpg, drivetrain)]

df = pd.DataFrame({'Weight (lbs)': weights, 'MPG': mpg, 'Drivetrain': drivetrain})

# Plot
fig, ax = plt.subplots()
for d in ['FWD', 'RWD', 'AWD']:
    subset = df[df['Drivetrain'] == d]
    ax.scatter(subset['Weight (lbs)'], subset['MPG'], label=d, alpha=0.7)

ax.set_xlabel("Weight (pounds)")
ax.set_ylabel("Miles per Gallon (MPG)")
ax.set_title("MPG vs Car Weight by Drivetrain Type")
ax.legend()
st.pyplot(fig)

st.markdown("""
### Observations:
- **FWD (Front-Wheel Drive)**: Lightest and most fuel-efficient.
- **RWD (Rear-Wheel Drive)**: Slightly lower MPG, common in sports cars.
- **AWD (All-Wheel Drive)**: Heaviest and least efficient, but provides better traction.
""")


st.title("🚗 Car Fuel Efficiency Simulation: MPG vs Weight, Engine, Horsepower, and Drivetrain")

# --- Simulate data ---
np.random.seed(42)
n = 120

# Generate variables
weights = np.random.uniform(2000, 5000, n)       # in pounds
engine_size = np.random.uniform(1.2, 5.0, n)     # in liters
horsepower = engine_size * np.random.uniform(60, 90, n)  # roughly scaled
drivetrain = np.random.choice(['FWD', 'RWD', 'AWD'], size=n, p=[0.4, 0.4, 0.2])

# --- MPG model ---
# Base MPG decreases with weight, engine size, and horsepower
mpg = 60 - 0.006 * weights - 1.8 * engine_size - 0.015 * horsepower

# Adjust for drivetrain effects
mpg_adjustment = {'FWD': +3, 'RWD': 0, 'AWD': -4}
mpg = [m + mpg_adjustment[d] + np.random.normal(0, 2) for m, d in zip(mpg, drivetrain)]

# Clip to realistic values
mpg = np.clip(mpg, 10, 60)

# --- Create DataFrame ---
df = pd.DataFrame({
    'Weight (lbs)': weights,
    'Engine Size (L)': engine_size,
    'Horsepower': horsepower,
    'Drivetrain': drivetrain,
    'MPG': mpg
})

# --- Show sample data ---
st.subheader("Sample of Simulated Data")
st.dataframe(df.head(10))

# --- Interactive Visualization ---
st.subheader("📊 MPG vs Weight (Colored by Drivetrain)")

fig, ax = plt.subplots()
for d in ['FWD', 'RWD', 'AWD']:
    subset = df[df['Drivetrain'] == d]
    ax.scatter(subset['Weight (lbs)'], subset['MPG'], label=d, alpha=0.7)

ax.set_xlabel("Weight (pounds)")
ax.set_ylabel("Miles per Gallon (MPG)")
ax.set_title("MPG vs Weight by Drivetrain Type")
ax.legend()
st.pyplot(fig)

# --- Optional: user filter ---
st.subheader("🔍 Explore Relationships")

x_var = st.selectbox("Select X-axis variable", ['Weight (lbs)', 'Engine Size (L)', 'Horsepower'])
y_var = st.selectbox("Select Y-axis variable", ['MPG'])
fig2, ax2 = plt.subplots()

for d in ['FWD', 'RWD', 'AWD']:
    subset = df[df['Drivetrain'] == d]
    ax2.scatter(subset[x_var], subset[y_var], label=d, alpha=0.7)

ax2.set_xlabel(x_var)
ax2.set_ylabel(y_var)
ax2.set_title(f"{y_var} vs {x_var} by Drivetrain Type")
ax2.legend()
st.pyplot(fig2)

# --- Summary ---
st.markdown("""
### 🧠 Interpretation:
- **Weight & Engine Size:** Heavier and larger engines → lower MPG.
- **Horsepower:** Higher horsepower also reduces fuel efficiency.
- **Drivetrain:**
  - 🟢 **FWD (Front-Wheel Drive):** Best MPG (light and efficient)
  - ⚙️ **RWD (Rear-Wheel Drive):** Moderate efficiency
  - 🔵 **AWD (All-Wheel Drive):** Lowest MPG (heavier, more friction)
""")

with st.expander("📘 Technical Notes"):
    st.markdown("""
    - This dataset is **simulated**, but modeled on real-world EPA fuel economy relationships.
    - The MPG model used:
      \n**MPG = 60 - 0.006×Weight - 1.8×EngineSize - 0.015×Horsepower + DrivetrainAdjustment + noise**
    - You can extend it further to include:
      - **Transmission type (auto/manual)**
      - **Fuel type (petrol/diesel/hybrid)**
      - **Aerodynamic drag or tire resistance**
    """)
