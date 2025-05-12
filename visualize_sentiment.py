import matplotlib
matplotlib.use('Qt5Agg')  # Use Qt5Agg backend
matplotlib.rcParams['toolbar'] = 'none'
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import Counter
from PyQt5.QtGui import QIcon
import os

print("Starting visualize_sentiment.py...")

try:
    # Ensure outputs directory exists
    outputs_dir = 'outputs'
    os.makedirs(outputs_dir, exist_ok=True)
    print(f"Created/check outputs directory: {os.path.abspath(outputs_dir)}")

    # Count sentiments from your log file
    sentiment_counts = Counter()
    try:
        if not os.path.exists('sentiment_results.txt'):
            raise FileNotFoundError("sentiment_results.txt does not exist.")
        with open('sentiment_results.txt', 'r', encoding='utf-8') as f:
            print("Opened sentiment_results.txt.")
            for line in f:
                if line.startswith("Sentiment:"):
                    sentiment = line.split(':')[1].split('(')[0].strip().capitalize()
                    sentiment_counts[sentiment] += 1
                    print(f"Found sentiment: {sentiment}")
    except FileNotFoundError as e:
        print(f"Error: {e}. Run sentiment_analysis.py first.")
        exit(1)
    except IOError as e:
        print(f"Error reading sentiment_results.txt: {e}")
        exit(1)

    # If no sentiments found, print error and stop
    if not sentiment_counts:
        print("Error: No sentiment data found in sentiment_results.txt.")
        exit(1)
    print(f"Sentiment counts: {sentiment_counts}")

    # Prepare data for plotting
    labels = list(sentiment_counts.keys())
    values = list(sentiment_counts.values())
    total = sum(values)
    if total == 0:
        print("Error: Total sentiment count is zero, cannot compute percentages.")
        exit(1)
    percentages = [(v / total * 100) for v in values]
    print(f"Labels: {labels}, Percentages: {percentages}")

    # Set up the figure and axes (1280x720 pixels at 100 DPI)
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=100)
    fig.canvas.manager.toolbar_visible = False
    fig.canvas.manager.set_window_title('Sentiment Analysis Chart')
    # Remove window icon
    try:
        fig.canvas.manager.window.setWindowIcon(QIcon())  # Set empty icon
        print("Removed window icon.")
    except Exception as e:
        print(f"Warning: Could not remove window icon: {e}")
    ax.set_title("Sentiment Insights: #Python & #Coding Tweets", color='white', pad=20)
    fig.patch.set_facecolor('#2e2e2e')
    ax.set_facecolor('#2e2e2e')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    print("Figure and axes set up.")

    # Define bar colors for known sentiments
    color_map = {
        'Positive': '#4CAF50',
        'Negative': '#F44336',
        'Neutral': '#2196F3'
    }

    # Assign colors based on sentiment labels (fallback to gray)
    bar_colors = [color_map.get(label, '#9E9E9E') for label in labels]
    print(f"Bar colors assigned: {bar_colors}")

    # Initialize bars and labels
    bars = ax.bar(labels, [0] * len(labels), color=bar_colors, width=0.5)
    ax.set_ylim(0, 100)
    ax.set_ylabel('Percentage (%)', color='white')
    print("Bars initialized.")

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
    print("Animation created.")

    # Save animation as GIF in outputs/
    try:
        gif_path = os.path.join(outputs_dir, 'animated_sentiment_chart.gif')
        if os.path.exists(gif_path):
            os.remove(gif_path)
        ani.save(gif_path, writer='pillow', fps=20)
        print(f"Saved animated_sentiment_chart.gif to {os.path.abspath(gif_path)}")
    except Exception as e:
        print(f"Error saving animated_sentiment_chart.gif: {e}")
        exit(1)

    # Save static chart after animation
    for i, bar in enumerate(bars):
        bar.set_height(percentages[i])
        texts[i].set_y(percentages[i] + 1)
        texts[i].set_text(f'{percentages[i]:.1f}%')
    try:
        png_path = os.path.join(outputs_dir, 'sentiment_chart.png')
        if os.path.exists(png_path):
            os.remove(png_path)
        plt.savefig(png_path, bbox_inches='tight', facecolor=fig.get_facecolor())
        print(f"Saved sentiment_chart.png to {os.path.abspath(png_path)}")
    except Exception as e:
        print(f"Error saving sentiment_chart.png: {e}")
        exit(1)

    # Show the chart
    print("Displaying chart...")
    plt.show()

except Exception as e:
    print(f"Unexpected error in visualize_sentiment.py: {e}")
    exit(1)