import json
import pandas as pd
import os


class Exporter:

    def export(self,
               components,
               output_dir="output"):

        os.makedirs(output_dir, exist_ok=True)

        # JSON
        json_path = os.path.join(
            output_dir,
            "bom.json"
        )

        with open(json_path,
                  'w',
                  encoding='utf-8') as f:

            json.dump(
                components,
                f,
                ensure_ascii=False,
                indent=2
            )

        # DataFrame
        df = pd.DataFrame(components)

        csv_path = os.path.join(
            output_dir,
            "bom.csv"
        )

        xlsx_path = os.path.join(
            output_dir,
            "bom.xlsx"
        )

        df.to_csv(
            csv_path,
            index=False,
            encoding='utf-8-sig'
        )

        df.to_excel(
            xlsx_path,
            index=False
        )

        print(f"JSON输出: {json_path}")
        print(f"CSV输出: {csv_path}")
        print(f"Excel输出: {xlsx_path}")