import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def process_payments(file_path):
    """
    Process payment data from a CSV file and generate a pie chart visualization.
    
    Args:
        file_path (str): Path to the CSV file containing payment data
    """
    # Validate file existence
    if not Path(file_path).exists():
        raise FileNotFoundError(f"The file {file_path} was not found.")
    
    try:
        # Read the CSV file and handle potential encoding issues
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        
        # Clean column names: strip whitespace and convert to title case
        df.columns = df.columns.str.strip().str.title()
        
        # Check if columns exist with various possible names
        amount_cols = ['Amount', 'amount']
        desc_cols = ['Description', 'description']
        
        amount_col = next((col for col in amount_cols if col in df.columns), None)
        desc_col = next((col for col in desc_cols if col in df.columns), None)
        
        if not amount_col or not desc_col:
            raise ValueError(f"CSV must contain columns for amount and description. Found columns: {list(df.columns)}")
        
        # Standardize column names
        df = df.rename(columns={
            amount_col: 'Amount',
            desc_col: 'Description'
        })
        
        # Convert Amount to numeric, removing any currency symbols and handling commas
        df['Amount'] = pd.to_numeric(df['Amount'].astype(str).str.replace(',', '').str.replace('$', ''), errors='coerce')
        
        # Group payments by description
        grouped = df.groupby('Description')['Amount'].sum().reset_index()
        
        # Calculate total amount and threshold for "Others" category
        total_amount = grouped['Amount'].sum()
        threshold = total_amount * 0.005  # 1% threshold
        
        # Split into significant and small payments
        significant = grouped[grouped['Amount'] >= threshold]
        small = grouped[grouped['Amount'] < threshold]
        
        # Create "Others" category if there are small payments
        if not small.empty:
            others = pd.DataFrame({
                'Description': ['Others'],
                'Amount': [small['Amount'].sum()]
            })
            final_data = pd.concat([significant, others], ignore_index=True)
        else:
            final_data = significant
            
        # Sort by amount in descending order
        final_data = final_data.sort_values('Amount', ascending=False)
        
        # Create pie chart with modified layout
        plt.figure(figsize=(12, 8))
        
        # Create the pie chart without labels on the pie itself
        patches, _ = plt.pie(
            final_data['Amount'],
            labels=None,  # Remove labels from pie
            startangle=90
        )
        
        # Calculate percentages for legend labels
        percentages = (final_data['Amount'] / total_amount * 100).round(1)
        legend_labels = [f'{desc} ({pct}%)' for desc, pct in zip(final_data['Description'], percentages)]
        
        # Add legend to bottom right
        plt.legend(
            patches,
            legend_labels,
            title="Categories",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )
        
        plt.title('Payment Distribution by Category of December')
        plt.axis('equal')  # Equal aspect ratio ensures circular plot
        
        # Show summary statistics
        print("\nPayment Summary:")
        print(f"Total Amount: ${total_amount:,.2f}")
        print(f"Number of Categories: {len(final_data)}")
        if not small.empty:
            print(f"Small Categories Combined: {len(small)}")
        
        # Display the processed data
        print("\nCategory Breakdown:")
        for _, row in final_data.iterrows():
            print(f"{row['Description']}: ${row['Amount']:,.2f}")
        
        # Adjust layout to prevent legend cutoff
        plt.tight_layout()
        
        # Show the plot
        plt.show()
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")

def main():
    """Main function to get user input and process the CSV file."""
    while True:
        file_path = input("\nEnter the path to your CSV file (or 'q' to quit): ")
        if file_path.lower() == 'q':
            break
        
        try:
            process_payments(file_path)
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()