import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import base64
from io import BytesIO
from matplotlib.colors import LinearSegmentedColormap

def generate_confidence_heatmap(results):
    """
    Generate an enhanced heatmap visualization of extraction confidence scores.
    
    Args:
        results (dict): Dictionary containing extraction results with confidence scores
        
    Returns:
        str: Base64 encoded PNG image of the heatmap with data URI prefix
    """
    # Extract field names and confidence scores
    
    fields = list(results.keys())
    confidence_scores = [results[field]['confidence'] for field in fields]
    answers = [results[field]['answer'] for field in fields]
    
    # Create a matrix for the heatmap (1 row, multiple columns)
    
    matrix = np.array(confidence_scores).reshape(1, -1)
    
    # Set up the matplotlib figure with more height for labels
    
    plt.figure(figsize=(14, 4))
    
    # Custom colormap 
    
    colors = ['#ff0000', '#ffa700', '#fff400', '#a3ff00', '#2cba00']
    custom_cmap = LinearSegmentedColormap.from_list("custom", colors, N=100)
    
    try:
        # Create heatmap using seaborn
        
        ax = sns.heatmap(
            matrix,
            annot=True,  
            fmt='.1f',   
            cmap=custom_cmap,
            vmin=0,      
            vmax=100,    
            cbar_kws={
                'label': 'Confidence %',
                'ticks': [0, 25, 50, 75, 100],
                'orientation': 'horizontal'
            },
            yticklabels=['Extracted\nValues'],
            xticklabels=fields
        )
        
        
        ax2 = ax.twinx()
        ax2.set_ylim(ax.get_ylim())
        
        
        formatted_answers = []
        for ans in answers:
            if not isinstance(ans, str):
                ans = str(ans)
            if len(ans) > 30:
                ans = ans[:27] + "..."
            formatted_answers.append(ans)
        
        ax2.set_yticks([0.5])
        ax2.set_yticklabels([''])
        
        
        for idx, (conf, ans) in enumerate(zip(confidence_scores, formatted_answers)):
            color = 'black' if conf > 50 else 'white'
            ax.text(idx + 0.5, 0.5, ans,
                    ha='center', va='center',
                    color=color, fontsize=8,
                    rotation=0)
        
        # Rotate x-axis labels for better readability
        
        plt.xticks(rotation=30, ha='right')
        plt.title('Invoice Field Extraction Results with Confidence Scores', pad=20)
        
        # Adjust layout to prevent label cutoff
        
        plt.tight_layout()
        
        # Convert plot to base64 encoded PNG with high DPI for clarity
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close()
        
        # Encode to base64
        
        graphic = "data:image/png;base64," + base64.b64encode(image_png).decode('utf-8')
        
        return graphic
        
    except Exception as e:
        print(f"Error generating heatmap: {str(e)}")
        plt.close()  
        return None