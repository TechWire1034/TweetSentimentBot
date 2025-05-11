import matplotlib
matplotlib.use('QtAgg')  # Switch to Qt backend
matplotlib.rcParams['toolbar'] = 'none'
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import Counter
from PyQt5.QtGui import QIcon

# Count sentiments from your log file
sentiment_counts = Counter()

with open('sentiment_results.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith("Sentiment:"):
            sentiment = line.split(':')[1].split('(')[0].strip().capitalize()
            sentiment_counts[sentiment] += 1

# If no sentiments found, print error and stop
if not sentiment_counts:
    print("No sentiment data found in file.")
    exit()

# Prepare data for plotting
labels = list(sentiment_counts.keys())
values = list(sentiment_counts.values())
total = sum(values)
percentages = [(v / total * 100) for v in values]

# Set up the figure and axes (1280x720 pixels at 100 DPI)
fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=100)
fig.canvas.manager.toolbar_visible = False  # Disable the toolbar
fig.canvas.manager.set_window_title('Sentiment Analysis Chart')  # Set window title
fig.canvas.manager.window.setWindowIcon(QIcon('sentiment_icon.ico'))
ax.set_title("Sentiment Insights: #Python & #Coding Tweets", color='white', pad=20)
fig.patch.set_facecolor('#2e2e2e')
ax.set_facecolor('#2e2e2e')
ax.tick_params(colors='white')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Define bar colors for known sentiments
color_map = {
    'Positive': '#4CAF50',
    'Negative': '#F44336',
    'Neutral':  '#2196F3'
}

# Assign colors based on sentiment labels (fallback to gray)
bar_colors = [color_map.get(label, '#9E9E9E') for label in labels]

# Initialize bars and labels
bars = ax.bar(labels, [0] * len(labels), color=bar_colors, width=0.5)
ax.set_ylim(0, 100)
ax.set_ylabel('Percentage (%)', color='white')

# Add text labels above each bar
texts = [ax.text(bar.get_x() + bar.get_width() / 2, 0, '0.0%', ha='center', va='bottom', color='white') for bar in bars]

# Animation function
def animate(frame):
    progress_ratio = (frame + 1) / 50
    for i, bar in enumerate(bars):
        target_height = percentages[i] * progress_ratio
        bar.set_height(target_height)
        texts[i].set_y(target_height + 1)
        texts[i].set_text(f'{target_height:.1f}%')
    return list(bars) + texts

# Create animation
ani = animation.FuncAnimation(fig, animate, frames=50, interval=50, blit=True, repeat=False)

# Save animation as GIF
ani.save('animated_sentiment_chart.gif', writer='pillow', fps=20)

# Show the chart
plt.show()