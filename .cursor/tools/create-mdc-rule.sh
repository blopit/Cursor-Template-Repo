#!/bin/bash

# create-mdc-rule.sh
# Script to create a new .mdc rule file based on the template

# Default values
TEMPLATE_PATH=".cursor/templates/rule-template.mdc"
OUTPUT_DIR=".cursor/rules"
CURRENT_DATE=$(date +%Y-%m-%d)

# Display help message
show_help() {
  echo "Usage: $0 [options] <rule-name>"
  echo
  echo "Creates a new .mdc rule file based on the template."
  echo
  echo "Options:"
  echo "  -h, --help                 Show this help message"
  echo "  -d, --directory <dir>      Specify output directory (default: $OUTPUT_DIR)"
  echo "  -t, --template <template>  Specify template file (default: $TEMPLATE_PATH)"
  echo "  -g, --globs <pattern>      Specify glob pattern"
  echo "  -c, --category <category>  Specify rule category (creates subdirectory)"
  echo
  echo "Example:"
  echo "  $0 -c workflows -g \"**/*.js,**/*.ts\" my-workflow-rule"
  echo
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      show_help
      exit 0
      ;;
    -d|--directory)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    -t|--template)
      TEMPLATE_PATH="$2"
      shift 2
      ;;
    -g|--globs)
      GLOB_PATTERN="$2"
      shift 2
      ;;
    -c|--category)
      CATEGORY="$2"
      shift 2
      ;;
    -*)
      echo "Unknown option: $1"
      show_help
      exit 1
      ;;
    *)
      RULE_NAME="$1"
      shift
      ;;
  esac
done

# Check if rule name is provided
if [ -z "$RULE_NAME" ]; then
  echo "Error: Rule name is required."
  show_help
  exit 1
fi

# Check if template file exists
if [ ! -f "$TEMPLATE_PATH" ]; then
  echo "Error: Template file not found: $TEMPLATE_PATH"
  exit 1
fi

# Determine output path
if [ -n "$CATEGORY" ]; then
  OUTPUT_DIR="$OUTPUT_DIR/$CATEGORY"
  # Create category directory if it doesn't exist
  mkdir -p "$OUTPUT_DIR"
fi

# Ensure rule name has .mdc extension
if [[ "$RULE_NAME" != *.mdc ]]; then
  RULE_NAME="${RULE_NAME}.mdc"
fi

OUTPUT_PATH="$OUTPUT_DIR/$RULE_NAME"

# Check if output file already exists
if [ -f "$OUTPUT_PATH" ]; then
  read -p "File already exists: $OUTPUT_PATH. Overwrite? (y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Operation cancelled."
    exit 0
  fi
fi

# Copy template to output path
cp "$TEMPLATE_PATH" "$OUTPUT_PATH"

# Prompt for rule description
read -p "Enter rule description: " DESCRIPTION

# Update metadata in the new file
if [ -n "$DESCRIPTION" ]; then
  sed -i '' "s/description: Brief description of this rule's purpose/description: $DESCRIPTION/" "$OUTPUT_PATH"
fi

if [ -n "$GLOB_PATTERN" ]; then
  sed -i '' "s/globs: \*\*\/\*\.\{ext1,ext2\}/globs: $GLOB_PATTERN/" "$OUTPUT_PATH"
fi

# Update author and date
USER_NAME=$(git config user.name 2>/dev/null || echo "Your Name")
sed -i '' "s/author: Your Name/author: $USER_NAME/" "$OUTPUT_PATH"
sed -i '' "s/YYYY-MM-DD/$CURRENT_DATE/g" "$OUTPUT_PATH"

# Update rule title
TITLE=$(echo "$RULE_NAME" | sed 's/\.mdc$//' | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1')
sed -i '' "s/# Rule Title/# $TITLE/" "$OUTPUT_PATH"

echo "Created new rule file: $OUTPUT_PATH"
echo "Remember to add this rule to your .cursorrules file in the <available_instructions> section."

# Suggest command to add to .cursorrules
RULE_ID=$(echo "$RULE_NAME" | sed 's/\.mdc$//')
echo
echo "Suggested entry for .cursorrules:"
echo "$RULE_ID: $DESCRIPTION" 