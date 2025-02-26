#!/bin/bash

# Template Selector Script
# This script helps select and copy templates from the awesome-cursor-rules-mdc directory

# Colors for better readability
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Base directories
TEMPLATE_DIR=".cursor/rules/awesome-cursor-rules-mdc"
TARGET_DIR=".cursor/rules"

# Check if the template directory exists
if [ ! -d "$TEMPLATE_DIR" ]; then
    echo -e "${RED}Error: Template directory not found at $TEMPLATE_DIR${NC}"
    exit 1
fi

# Function to display available categories
show_categories() {
    echo -e "${BLUE}Available Template Categories:${NC}"
    echo "1) Frontend Frameworks"
    echo "2) Backend Frameworks"
    echo "3) Full Stack Solutions"
    echo "4) Mobile Development"
    echo "5) Data Science & ML"
    echo "6) Blockchain"
    echo "7) Other"
    echo -e "${YELLOW}Enter your choice (1-7):${NC}"
}

# Function to display available templates based on category
show_templates() {
    local category=$1
    
    case $category in
        1) # Frontend Frameworks
            echo -e "${BLUE}Frontend Framework Templates:${NC}"
            echo "1) React"
            echo "2) Next.js"
            echo "3) Vue.js"
            echo "4) Svelte/SvelteKit"
            echo "5) Solid.js"
            echo "6) Qwik"
            ;;
        2) # Backend Frameworks
            echo -e "${BLUE}Backend Framework Templates:${NC}"
            echo "1) Python (FastAPI/Django)"
            echo "2) Node.js/Express"
            echo "3) NestJS"
            echo "4) Laravel/PHP"
            ;;
        3) # Full Stack Solutions
            echo -e "${BLUE}Full Stack Solution Templates:${NC}"
            echo "1) Next.js + TypeScript"
            echo "2) TypeScript + React + Supabase"
            echo "3) MERN Stack (MongoDB, Express, React, Node.js)"
            echo "4) TypeScript + shadcn/ui + Next.js"
            ;;
        4) # Mobile Development
            echo -e "${BLUE}Mobile Development Templates:${NC}"
            echo "1) React Native"
            echo "2) React Native + Expo"
            echo "3) SwiftUI"
            ;;
        5) # Data Science & ML
            echo -e "${BLUE}Data Science & ML Templates:${NC}"
            echo "1) Python LLM and ML workflow"
            echo "2) PyTorch and scikit-learn"
            echo "3) Pandas and scikit-learn"
            ;;
        6) # Blockchain
            echo -e "${BLUE}Blockchain Templates:${NC}"
            echo "1) Solidity with Hardhat"
            echo "2) Solidity with React"
            ;;
        7) # Other
            echo -e "${BLUE}Other Templates:${NC}"
            echo "1) TypeScript Configuration"
            echo "2) Tailwind CSS Setup"
            echo "3) Testing Frameworks"
            ;;
        *)
            echo -e "${RED}Invalid category${NC}"
            return 1
            ;;
    esac
    
    echo -e "${YELLOW}Enter your choice:${NC}"
}

# Function to get template directory based on selection
get_template_dir() {
    local category=$1
    local choice=$2
    
    case $category in
        1) # Frontend Frameworks
            case $choice in
                1) echo "react-typescript-nextjs-nodejs-cursorrules-prompt-file" ;;
                2) echo "nextjs-typescript-tailwind-cursorrules-prompt-file" ;;
                3) echo "vue-3-nuxt-3-typescript-cursorrules-prompt-file" ;;
                4) echo "sveltekit-typescript-guide-cursorrules-prompt-file" ;;
                5) echo "solidjs-typescript-cursorrules-prompt-file" ;;
                6) echo "qwik-tailwind-cursorrules-prompt-file" ;;
                *) return 1 ;;
            esac
            ;;
        2) # Backend Frameworks
            case $choice in
                1) echo "python-fastapi-best-practices-cursorrules-prompt-f" ;;
                2) echo "nodejs-mongodb-jwt-express-react-cursorrules-promp" ;;
                3) echo "typescript-nestjs-best-practices-cursorrules-promp" ;;
                4) echo "laravel-tall-stack-best-practices-cursorrules-prom" ;;
                *) return 1 ;;
            esac
            ;;
        3) # Full Stack Solutions
            case $choice in
                1) echo "typescript-nextjs-supabase-cursorrules-prompt-file" ;;
                2) echo "typescript-react-nextui-supabase-cursorrules-promp" ;;
                3) echo "nodejs-mongodb-jwt-express-react-cursorrules-promp" ;;
                4) echo "typescript-shadcn-ui-nextjs-cursorrules-prompt-fil" ;;
                *) return 1 ;;
            esac
            ;;
        4) # Mobile Development
            case $choice in
                1) echo "react-native-expo-cursorrules-prompt-file" ;;
                2) echo "react-native-expo-router-typescript-windows-cursorrules-prompt-file" ;;
                3) echo "swiftui-guidelines-cursorrules-prompt-file" ;;
                *) return 1 ;;
            esac
            ;;
        5) # Data Science & ML
            case $choice in
                1) echo "python-llm-ml-workflow-cursorrules-prompt-file" ;;
                2) echo "pytorch-scikit-learn-cursorrules-prompt-file" ;;
                3) echo "pandas-scikit-learn-guide-cursorrules-prompt-file" ;;
                *) return 1 ;;
            esac
            ;;
        6) # Blockchain
            case $choice in
                1) echo "solidity-hardhat-cursorrules-prompt-file" ;;
                2) echo "solidity-react-blockchain-apps-cursorrules-prompt-" ;;
                *) return 1 ;;
            esac
            ;;
        7) # Other
            case $choice in
                1) echo "typescript-code-convention-cursorrules-prompt-file" ;;
                2) echo "tailwind-css-nextjs-guide-cursorrules-prompt-file" ;;
                3) echo "typescript-expo-jest-detox-cursorrules-prompt-file" ;;
                *) return 1 ;;
            esac
            ;;
        *)
            return 1
            ;;
    esac
}

# Function to determine target directory
get_target_subdir() {
    local category=$1
    
    case $category in
        1) echo "tech/frontend" ;; # Frontend Frameworks
        2) echo "tech/backend" ;; # Backend Frameworks
        3) echo "stack" ;; # Full Stack Solutions
        4) echo "tech/mobile" ;; # Mobile Development
        5) echo "tech/data-science" ;; # Data Science & ML
        6) echo "tech/blockchain" ;; # Blockchain
        7) echo "tech/other" ;; # Other
        *) echo "tech" ;;
    esac
}

# Main script execution
echo -e "${GREEN}=== Cursor Rules Template Selector ===${NC}"
echo "This script helps you select and copy templates from the awesome-cursor-rules-mdc directory."

# Step 1: Select category
show_categories
read -r category_choice

if ! [[ "$category_choice" =~ ^[1-7]$ ]]; then
    echo -e "${RED}Invalid choice. Please enter a number between 1 and 7.${NC}"
    exit 1
fi

# Step 2: Select template
show_templates "$category_choice"
read -r template_choice

# Step 3: Get template directory
template_dir=$(get_template_dir "$category_choice" "$template_choice")

if [ -z "$template_dir" ]; then
    echo -e "${RED}Invalid template choice.${NC}"
    exit 1
fi

# Step 4: Determine target directory
target_subdir=$(get_target_subdir "$category_choice")
full_target_dir="$TARGET_DIR/$target_subdir"

# Step 5: Confirm and copy
echo -e "${BLUE}Selected template:${NC} $template_dir"
echo -e "${BLUE}Target directory:${NC} $full_target_dir"
echo -e "${YELLOW}Do you want to copy this template? (y/n)${NC}"
read -r confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo -e "${RED}Operation cancelled.${NC}"
    exit 0
fi

# Create target directory if it doesn't exist
mkdir -p "$full_target_dir"

# Copy template files
echo -e "${GREEN}Copying template files...${NC}"
cp -r "$TEMPLATE_DIR/$template_dir"/* "$full_target_dir/"

# Check if copy was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Template files copied successfully to $full_target_dir${NC}"
    echo -e "${YELLOW}Remember to update glob patterns in the template files to match your project structure.${NC}"
else
    echo -e "${RED}Failed to copy template files.${NC}"
    exit 1
fi

echo -e "${GREEN}Done!${NC}" 