#!/bin/bash

# Usage:
# ./run_mineru.sh <input_dir> <output_dir>

INPUT_DIR=$1
OUTPUT_DIR=$2

# Validate input
if [ -z "$INPUT_DIR" ] || [ -z "$OUTPUT_DIR" ]; then
  echo " Usage: ./run_mineru.sh <input_dir> <output_dir>"
  exit 1
fi

# Create output directory if not exists
mkdir -p "$OUTPUT_DIR"

echo "📂 Input: $INPUT_DIR"
echo "📂 Output: $OUTPUT_DIR"

# Loop through all PDFs
for pdf in "$INPUT_DIR"/*.pdf; do
  # Handle case where no PDFs exist
  [ -e "$pdf" ] || { echo "⚠️ No PDF files found in $INPUT_DIR"; break; }

  filename=$(basename "$pdf" .pdf)
  out_dir="$OUTPUT_DIR/$filename"

  mkdir -p "$out_dir"

  echo "🚀 Processing: $pdf"

  mineru -p "$pdf" -o "$out_dir" -m auto -l en

  echo "✅ Done: $filename"
done

echo "🎉 All files processed."