#!/bin/bash

categories=("MJU20" "MJU18" "MJU16" "M15" "M14" "MJU14" "M13" "M12" "WJU20" "WJU18" "WJU16" "W15" "W14" "WJU14" "W13" "W12")
additional_urls=("https://bestenliste.slb-saarland.com/aktive/M" "https://bestenliste.slb-saarland.com/aktive/W")
base_url="https://bestenliste.slb-saarland.com/jugend/"

output_dir="raw/2023"

mkdir -p "$output_dir"

for category in "${categories[@]}"; do
  url="${base_url}${category}/"
  output_file="${output_dir}/${category}.html"
  
  echo "Downloading $url to $output_file"
  curl -o "$output_file" "$url" 
done

for url in "${additional_urls[@]}"; do
  category_name="$(basename "$url")"
  output_file="${output_dir}/${category_name}.html"
  
  echo "Downloading $url to $output_file"
  curl -o "$output_file" "$url"
done

echo "Download completed."
