import matplotlib.pyplot as plt

# Disable the interactive toolbar
plt.rcParams['toolbar'] = 'None'

# Sentiment data from sentiment_analysis.py
sentiment_data = {'positive': 3, 'negative': 2, 'neutral': 41}
total_tweets = sum(sentiment_data.values())  # Total tweets analyzed: 46

# Calculate percentages
percentages = {key: (value / total_tweets) * 100 for key, value in sentiment_data.items()}

# Set modern style with dark theme
plt.style.use('default')
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 0.6

# Create figure and axis
fig, ax = plt.subplots(figsize=(7, 5))

# Set the window title
fig.canvas.manager.set_window_title('Sentiment Analysis Chart')  # Renames "Figure 1" to custom title

# Dark modern color palette
colors = ['#A3BE8C', '#D08770', '#81A1C1']

# Create bar chart with slimmer bars
labels = list(sentiment_data.keys())
values = list(sentiment_data.values())
bars = ax.bar(labels, values, color=colors, alpha=0.9, edgecolor='white', linewidth=1, width=0.4)

# Add percentage labels on top of each bar
for bar, percentage in zip(bars, percentages.values()):
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 1.5,
        f'{percentage:.1f}%',
        ha='center', va='bottom', fontsize=10, fontweight='bold', color='#E0E0E0'
    )

# Customize the chart
ax.set_title('Sentiment Insights: #Python & #Coding Tweets', 
             fontsize=14, fontweight='bold', color='#E0E0E0', pad=15)
ax.set_xlabel('Sentiment', fontsize=11, color='#E0E0E0')
ax.set_ylabel('Number of Tweets', fontsize=11, color='#E0E0E0')
ax.set_ylim(0, max(values) + 7)

# Dark theme axes
ax.tick_params(axis='both', which='major', labelsize=10, colors='#BBBBBB')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#555555')
ax.spines['bottom'].set_color('#555555')

# Subtle gridlines (y-axis only)
ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='#555555')
ax.set_axisbelow(True)

# Dark modern background
fig.patch.set_facecolor('#1E1E1E')
ax.set_facecolor('#2D2D2D')

# Add total tweets annotation
ax.text(0.5, max(values) + 5, f'Total Tweets Analyzed: {total_tweets}', 
        ha='center', fontsize=9, color='#BBBBBB')

# Save and display the chart
plt.tight_layout()
plt.savefig(r'C:\Users\Unknown01\Desktop\Grok\sentiment_chart.png', dpi=300, bbox_inches='tight', facecolor='#1E1E1E')
plt.show()
