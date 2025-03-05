#!/bin/bash

# Helper functions for git operations using hidden temporary files

# Constants
COMMIT_MSG_FILE=".commit_msg"
PR_BODY_FILE=".pr_body"

# Function to create a commit with a multi-line message
# Usage: create_commit "Title" "Body" [files...]
create_commit() {
    local title="$1"
    local body="$2"
    shift 2
    local files=("$@")
    
    # Create the commit message with Cursor prefix
    echo "[Cursor] $title" > "$COMMIT_MSG_FILE"
    echo "" >> "$COMMIT_MSG_FILE"
    echo "$body" >> "$COMMIT_MSG_FILE"
    
    # Add files if specified, otherwise add all changes
    if [ ${#files[@]} -gt 0 ]; then
        git add "${files[@]}"
    else
        git add .
    fi
    
    # Create the commit
    git commit -F "$COMMIT_MSG_FILE"
    
    # Clean up
    rm -f "$COMMIT_MSG_FILE"
}

# Function to create a PR with a multi-line description
# Usage: create_pr "Title" "Body" [base_branch]
create_pr() {
    local title="$1"
    local body="$2"
    local base_branch="${3:-main}"
    
    # Create the PR body file with Cursor prefix
    echo "[Cursor] $title" > "$PR_BODY_FILE"
    echo "" >> "$PR_BODY_FILE"
    echo "$body" >> "$PR_BODY_FILE"
    
    # Create the PR
    gh pr create --title "[Cursor] $title" --body-file "$PR_BODY_FILE" --base "$base_branch"
    
    # Clean up
    rm -f "$PR_BODY_FILE"
}

# Function to create a feature branch
# Usage: create_feature_branch "feature-name"
create_feature_branch() {
    local branch_name="$1"
    
    # Ensure branch name is valid
    branch_name=$(echo "$branch_name" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
    
    # Create and checkout the branch
    git checkout -b "$branch_name"
    echo "Created and switched to branch: $branch_name"
}

# Function to push a branch and set upstream
# Usage: push_branch [branch_name]
push_branch() {
    local branch_name="${1:-$(git branch --show-current)}"
    
    git push -u origin "$branch_name"
}

# Display help if no arguments provided
if [ $# -eq 0 ]; then
    echo "Git Helper Functions"
    echo "-------------------"
    echo "Usage:"
    echo "  source tools/git_helpers.sh"
    echo ""
    echo "Available functions:"
    echo "  create_commit \"Title\" \"Body\" [files...]"
    echo "  create_pr \"Title\" \"Body\" [base_branch]"
    echo "  create_feature_branch \"feature-name\""
    echo "  push_branch [branch_name]"
fi 