import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def process_payments(file_path):
    """
    Process payment data from a CSV file and generate a pie chart visualization.

    """

    if not Path(file_path).exists():
        raise FileNotFoundError(f"The file {file_path} was not found.")
    
    try:
      
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        df.columns = df.columns.str.strip().str.title()
        
        amount_cols = ['Amount', 'amount']
        desc_cols = ['Description', 'description']
        
        amount_col = next((col for col in amount_cols if col in df.columns), None)
        desc_col = next((col for col in desc_cols if col in df.columns), None)
        
        if not amount_col or not desc_col:
            raise ValueError(f"CSV must contain columns for amount and description. Found columns: {list(df.columns)}")
        
       
        df = df.rename(columns={
            amount_col: 'Amount',
            desc_col: 'Description'
        })
        
        df['Amount'] = pd.to_numeric(df['Amount'].astype(str).str.replace(',', '').str.replace('$', ''), errors='coerce')
        
        grouped = df.groupby('Description')['Amount'].sum().reset_index()
        
    
        total_amount = grouped['Amount'].sum()
        threshold = total_amount * 0.005 
        
       
        significant = grouped[grouped['Amount'] >= threshold]
        small = grouped[grouped['Amount'] < threshold]
        
       
        if not small.empty:
            others = pd.DataFrame({
                'Description': ['Others'],
                'Amount': [small['Amount'].sum()]
            })
            final_data = pd.concat([significant, others], ignore_index=True)
        else:
            final_data = significant

        
        final_data = final_data.sort_values('Amount', ascending=False)
        
    
        plt.figure(figsize=(12, 8))
        
       
        patches, _ = plt.pie(
            final_data['Amount'],
            labels=None,  
            startangle=90
        )
        
     
        percentages = (final_data['Amount'] / total_amount * 100).round(1)
        legend_labels = [f'{desc} ({pct}%)' for desc, pct in zip(final_data['Description'], percentages)]
        
     
        plt.legend(
            patches,
            legend_labels,
            title="Categories",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )
        
        plt.title('Payment Distribution by Category of December')
        plt.axis('equal')  
        
        
        print("\nPayment Summary:")
        print(f"Total Amount: ${total_amount:,.2f}")
        print(f"Number of Categories: {len(final_data)}")
        if not small.empty:
            print(f"Small Categories Combined: {len(small)}")
        
      
        print("\nCategory Breakdown:")
        for _, row in final_data.iterrows():
            print(f"{row['Description']}: ${row['Amount']:,.2f}")
        
       
        plt.tight_layout()
        
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
