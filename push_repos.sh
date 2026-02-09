#!/bin/bash
set -e



# Function to push a single lab
push_lab() {
    local lab=$1
    echo "--------------------------------------------------"
    echo "Processing $lab..."
    
    if [ ! -d "$lab" ]; then
        echo "Error: Directory $lab not found!"
        return
    fi
    
    # Run in a subshell to avoid directory navigation issues
    (
        cd "$lab"
        
        # Check if remote 'origin' already exists locally
        if git remote | grep -q "^origin$"; then
            echo "Remote 'origin' already exists locally."
        else
            echo "Adding remote 'origin'..."
            # Extract just the lab name from the path (e.g., module-1/lab-name -> lab-name)
            lab_name=$(basename "$lab")
            git remote add origin "git@github.com:franakol/$lab_name.git"
        fi
    
        # Push to main
        echo "Pushing to remote..."
        git push -u origin main || {
            echo "Push failed. You might need to force push if history diverged."
            echo "Try running: cd $lab && git push -f origin main"
        }
    )
    echo "Done with $lab"
}

# Find all git repositories (directories containing .git)
# Exclude the root directory itself and hidden directories like .git.monorepo.bak
find . -maxdepth 3 -type d -name ".git" | while read gitdir; do
    # Get the parent directory of .git, which is the lab root
    lab_dir=$(dirname "$gitdir")
    
    # Skip the root repo itself (./.git)
    if [ "$lab_dir" == "." ]; then
        continue
    fi

    # Strip leading ./ for cleaner output
    lab_clean=${lab_dir#./}
    
    push_lab "$lab_clean"
done
echo "--------------------------------------------------"
echo "All repositories processed!"
