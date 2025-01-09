import csv

def txt_to_csv(input_txt, output_csv):
    with open(input_txt, 'r', encoding='utf-8') as f_in, \
         open(output_csv, 'w', encoding='utf-8', newline='') as f_out:
        
        writer = csv.writer(f_out)
        writer.writerow(["Description", "Amount (TL)"]) 
        lines = f_in.read().splitlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.lower().startswith("description"):
                continue

            parts = line.rsplit(None, 1) 
            if len(parts) == 2:
                description, amount_str = parts
                writer.writerow([description, amount_str])
            else:
               
                print(f"Skipping line (cannot split into exactly 2 parts): {line}")


txt_to_csv(r"C:\Users\Emir Avcı\OneDrive\Desktop\DönemDönem Sabancı\Ne 2 Ne 3\Dsa210\Proj\dataSet\October.txt",
           r"C:\Users\Emir Avcı\OneDrive\Desktop\DönemDönem Sabancı\Ne 2 Ne 3\Dsa210\Proj\dataSet\October.csv")


txt_to_csv(r"C:\Users\Emir Avcı\OneDrive\Desktop\DönemDönem Sabancı\Ne 2 Ne 3\Dsa210\Proj\dataSet\November.txt",
           r"C:\Users\Emir Avcı\OneDrive\Desktop\DönemDönem Sabancı\Ne 2 Ne 3\Dsa210\Proj\dataSet\November.csv")

txt_to_csv(r"C:\Users\Emir Avcı\OneDrive\Desktop\DönemDönem Sabancı\Ne 2 Ne 3\Dsa210\Proj\dataSet\September.txt",
           r"C:\Users\Emir Avcı\OneDrive\Desktop\DönemDönem Sabancı\Ne 2 Ne 3\Dsa210\Proj\dataSet\September.csv")


print("Finished converting to CSV")
