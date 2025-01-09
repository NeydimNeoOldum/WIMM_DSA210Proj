import csv

def txt_to_csv(input_txt, output_csv):
    with open(input_txt, 'r', encoding='utf-8') as f_in, \
         open(output_csv, 'w', encoding='utf-8', newline='') as f_out:
        
        writer = csv.writer(f_out)
        writer.writerow(["Description", "Amount (TL)"])  # CSV header in output

        lines = f_in.read().splitlines()

        for line in lines:
            # Strip whitespace to check if it's empty
            line = line.strip()
            if not line:
                # Skip completely blank lines
                continue

            # If the line starts with "Description", skip it (it's likely a header)
            if line.lower().startswith("description"):
                continue

            # Split from the right so the last part is the amount
            parts = line.rsplit(None, 1)  # rsplit on whitespace, once
            if len(parts) == 2:
                description, amount_str = parts
                writer.writerow([description, amount_str])
            else:
                # Not 2 parts? Let’s see what the line looks like.
                print(f"Skipping line (cannot split into exactly 2 parts): {line}")



# Example usage:
txt_to_csv(r"C:\Users\Emir Avcı\OneDrive\Desktop\DönemDönem Sabancı\Ne 2 Ne 3\Dsa210\Proj\dataSet\October.txt",
           r"C:\Users\Emir Avcı\OneDrive\Desktop\DönemDönem Sabancı\Ne 2 Ne 3\Dsa210\Proj\dataSet\October.csv")


txt_to_csv(r"C:\Users\Emir Avcı\OneDrive\Desktop\DönemDönem Sabancı\Ne 2 Ne 3\Dsa210\Proj\dataSet\November.txt",
           r"C:\Users\Emir Avcı\OneDrive\Desktop\DönemDönem Sabancı\Ne 2 Ne 3\Dsa210\Proj\dataSet\November.csv")

txt_to_csv(r"C:\Users\Emir Avcı\OneDrive\Desktop\DönemDönem Sabancı\Ne 2 Ne 3\Dsa210\Proj\dataSet\September.txt",
           r"C:\Users\Emir Avcı\OneDrive\Desktop\DönemDönem Sabancı\Ne 2 Ne 3\Dsa210\Proj\dataSet\September.csv")


print("Finished converting to CSV")
