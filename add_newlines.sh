#!/bin/bash
find .cursor/rules -name "*.mdc" -type f | while read file; do
  if [ "$(tail -c 1 "$file" | wc -l)" -eq 0 ]; then
    echo "Adding newline to $file"
    printf "
" >> "$file"
  fi
done
