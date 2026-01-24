from flask import Flask, request, send_file, jsonify
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/filter", methods=["POST"])
def filter_dat_file():
    try:
        # 1️⃣ Get files from Postman
        input_file = request.files.get("input_file")
        filter_file = request.files.get("filter_file")

        if not input_file or not filter_file:
            return jsonify({"error": "Both input_file and filter_file are required"}), 400

        # 2️⃣ Save both files
        input_path = os.path.join(UPLOAD_DIR, input_file.filename)
        filter_path = os.path.join(UPLOAD_DIR, filter_file.filename)

        input_file.save(input_path)
        filter_file.save(filter_path)

        # 3️⃣ Read files
        df_input = pd.read_csv(input_path)
        df_filter = pd.read_csv(filter_path)

        key_cols = [
            "Operating Unit ID",
            "Vendor ID",
            "Supplier Site Code"
        ]

        # 4️⃣ Filter logic
        filtered_df = df_input.merge(
            df_filter[key_cols].drop_duplicates(),
            on=key_cols,
            how="inner"
        )

        # 5️⃣ Output file in SAME FOLDER as input
        input_dir = os.path.dirname(input_path)
        output_filename = "filtered_output.dat"
        output_path = os.path.join(input_dir, output_filename)

        filtered_df.to_csv(output_path, index=False)

        # 6️⃣ Return file for download
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
