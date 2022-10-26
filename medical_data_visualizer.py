import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['overweight'] = df.overweight = df['weight'] / ((df['height'] * 0.01) ** 2)
df.loc[df.overweight <= 25, 'overweight'] = 0
df.loc[df.overweight > 25, 'overweight'] = 1
df = df.astype({'overweight': 'int'})

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df.loc[df.cholesterol == 1, 'cholesterol'] = 0
df.loc[df.cholesterol > 1, 'cholesterol'] = 1
df.loc[df.gluc == 1, 'gluc'] = 0
df.loc[df.gluc > 1, 'gluc'] = 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars='cardio', value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])
    

    # Draw the catplot with 'sns.catplot()'
    sns.catplot(data=df_cat, x='variable', col='cardio', hue='value', kind='count')


    # Get the figure for the output
    fig = sns.catplot(data=df_cat, x='variable', col='cardio', hue='value', kind='count')


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    index_heat = df[(df['ap_lo'] > df['ap_hi']) | (df['height'] < df['height'].quantile(0.025)) | (df['height'] > df['height'].quantile(0.975)) | (df['weight'] < df['weight'].quantile(0.025)) | (df['weight'] > df['weight'].quantile(0.975))].index
    df_heat = df.drop(index_heat)

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(corr)

    # Set up the matplotlib figure
    fig, ax = plt.subplots()

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask=mask, annot=True, fmt=".1f", linewidth=.5, vmin=-.1, vmax=.3)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
