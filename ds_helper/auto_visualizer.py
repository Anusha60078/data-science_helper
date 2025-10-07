# auto_visualizer.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

def visualize(df):
    """
    Automatically generate plots based on column types:
    - Numerical → histogram, boxplot, scatter
    - Categorical → bar chart, count plot
    - Text (high-cardinality categorical) → top value frequency bar chart
    """
    # Detect column types
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Classify categorical vs text based on unique values
    text_cols = []
    categorical_final = []
    for col in categorical_cols:
        if df[col].nunique() > 20:
            text_cols.append(col)
        else:
            categorical_final.append(col)

    print("Detected Columns:")
    print({
        'numerical': numerical_cols,
        'categorical': categorical_final,
        'text': text_cols
    })

    # Plotting
    for col in numerical_cols:
        _plot_numerical(df, col)
    for col in categorical_final:
        _plot_categorical(df, col)
    for col in text_cols:
        _plot_text_frequency(df, col)

    plt.show()


# --------------------- Helper functions ---------------------

def _plot_numerical(df, col):
    fig, axes = plt.subplots(1, 3, figsize=(18, 4))
    sns.histplot(df[col], kde=True, ax=axes[0], color='skyblue')
    axes[0].set_title(f'Histogram of {col}')
    sns.boxplot(x=df[col], ax=axes[1], color='lightgreen')
    axes[1].set_title(f'Boxplot of {col}')
    axes[2].scatter(df.index, df[col], color='salmon', alpha=0.7)
    axes[2].set_title(f'Scatter plot of {col} vs index')
    axes[2].set_xlabel('Index')
    axes[2].set_ylabel(col)
    plt.tight_layout()


def _plot_categorical(df, col):
    fig, axes = plt.subplots(1, 2, figsize=(14, 4))
    sns.countplot(x=col, data=df, ax=axes[0], palette='Set2')
    axes[0].set_title(f'Count plot of {col}')
    axes[0].tick_params(axis='x', rotation=45)
    freq = df[col].value_counts()
    freq.plot(kind='bar', ax=axes[1], color='lightcoral')
    axes[1].set_title(f'Bar chart of {col}')
    plt.tight_layout()


def _plot_text_frequency(df, col):
    """Plot frequency of top 20 values for high-cardinality text columns"""
    freq = df[col].value_counts().head(20)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=freq.values, y=freq.index, palette='viridis')
    plt.title(f'Top 20 value frequency in {col}')
    plt.xlabel("Count")
    plt.ylabel(col)
    plt.tight_layout()


# --------------------- Test block ---------------------
if __name__ == "__main__":
    # Example DataFrame
    df = pd.DataFrame({
        'Age': [23, 25, 30, 22, 35],
        'Gender': ['M', 'F', 'F', 'M', 'F'],
        'ZIP': ['56001', '56002', '56003', '56001', '56002'],
        'Feedback': ['good', 'excellent', 'good', 'average', 'excellent']
    })

    visualize(df)
