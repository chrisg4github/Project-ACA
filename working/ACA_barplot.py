import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Load data
path = '/../'

with open('%sCovGains.csv' % path) as f:
    df = pd.read_csv(f)

states = pd.read_csv('https://query.data.world/s/bkbonapg553rwy1riqjqqdm9f')


# add state abbreviations
states.drop([47, 48, 49, 50, 51, 52], axis=0, inplace=True)
states = states.sort_values(by='STATE_NAME')
states=states.reset_index(drop=True)

df['StateAbb'] = states.STUSAB
df = df[:51]


# plot

sns.set_style('ticks')

f, ax = plt.subplots(figsize=(10, 18))

df = df.sort_values(by='UninsuredRate2015', ascending=False)

sns.set_color_codes("pastel")
sns.barplot(x='UninsuredRate2010', y='StateAbb', data=df, label='2010', color='b')

sns.set_color_codes("muted")
sns.barplot(x='UninsuredRate2015', y='StateAbb', data=df, label='2015', color='b')

ax.legend(ncol=2, loc="lower right", frameon=True, fontsize=14)

plt.grid(alpha=0.5, linestyle='dashed')
ax.set_ylabel('')
ax.set_xlabel('Percent Uninsured', fontsize=18)
plt.yticks(fontsize=15)
locs, labels = plt.xticks()
plt.xticks(locs[1:], ['5%', '10%', '15%', '20%', '25%'], fontsize=15)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.set_title('Uninsured Rates (healthcare) by State\n2010 vs 2015', fontsize=22)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.show()
