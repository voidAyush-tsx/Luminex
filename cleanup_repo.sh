#!/bin/bash
# Repository Cleanup Script for Futurix AI
# This script removes unnecessary files and prepares the repo for clean commits

echo "=== Futurix AI Repository Cleanup ==="
echo ""

# Create backup timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/tmp/repo_cleanup_backup_${TIMESTAMP}"

echo "Creating backup directory: ${BACKUP_DIR}"
mkdir -p "${BACKUP_DIR}"

# List of files to potentially clean up
FILES_TO_REVIEW=(
    "debug_client.py"
    "fix_openai_client.sh"
    "FIX_README.md"
    "setup_shivaay_integration.sh"
    "SHIVAAY_INTEGRATION_SUMMARY.md"
    "test_openai_client.py"
    "test_shivaay_integration.py"
    "run.py"  # May be redundant with backend/app/main.py
)

# Directories to review
DIRS_TO_REVIEW=(
    "src"  # Old structure, now we have backend/
    "examples"  # May contain demo files that should be in docs or removed
)

echo ""
echo "=== Files Flagged for Review ==="
for file in "${FILES_TO_REVIEW[@]}"; do
    if [ -f "$file" ]; then
        echo "  - $file (potential cleanup candidate)"
        # Backup before deletion
        cp "$file" "${BACKUP_DIR}/" 2>/dev/null || true
    fi
done

echo ""
echo "=== Directories Flagged for Review ==="
for dir in "${DIRS_TO_REVIEW[@]}"; do
    if [ -d "$dir" ]; then
        echo "  - $dir/ (potential cleanup candidate)"
        # Backup before deletion
        tar -czf "${BACKUP_DIR}/${dir}.tar.gz" "$dir" 2>/dev/null || true
    fi
done

echo ""
echo "=== Cleanup Actions ==="
echo ""
echo "The following actions are SAFE and will be performed:"
echo ""

# Remove Python cache files
echo "1. Removing Python cache files (__pycache__, *.pyc)..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

# Remove .DS_Store files (macOS)
echo "2. Removing .DS_Store files..."
find . -type f -name ".DS_Store" -delete 2>/dev/null || true

# Remove temporary files
echo "3. Removing temporary files (*.tmp, *.bak)..."
find . -type f -name "*.tmp" -delete 2>/dev/null || true
find . -type f -name "*.bak" -delete 2>/dev/null || true

# Remove log files (but keep logs/ directory structure)
echo "4. Removing standalone log files (keep logs/ directory)..."
find . -maxdepth 1 -type f -name "*.log" -delete 2>/dev/null || true

echo ""
echo "=== Cleanup Summary ==="
echo "Backup created at: ${BACKUP_DIR}"
echo ""
echo "Files backed up:"
ls -lh "${BACKUP_DIR}/" 2>/dev/null || echo "  (backup directory empty or inaccessible)"

echo ""
echo "=== Recommendations ==="
echo ""
echo "MANUAL REVIEW REQUIRED for:"
echo "  - Root-level files that may be duplicates (requirements.txt, Dockerfile, docker-compose.yml)"
echo "  - Old src/ directory (if backend/ replaces it)"
echo "  - Test/demo files in root (test_*.py, examples/)"
echo ""
echo "ACTION ITEMS:"
echo "  1. Review and decide on src/ vs backend/ structure"
echo "  2. Consolidate duplicate config files (Dockerfile, docker-compose.yml)"
echo "  3. Move or remove example/demo files"
echo "  4. Update .gitignore to prevent re-adding cleaned files"
echo ""

# Create manifest
MANIFEST="${BACKUP_DIR}/cleanup_manifest.txt"
echo "Cleanup Manifest - ${TIMESTAMP}" > "${MANIFEST}"
echo "================================" >> "${MANIFEST}"
echo "" >> "${MANIFEST}"
echo "Backed up files:" >> "${MANIFEST}"
ls -1 "${BACKUP_DIR}/" >> "${MANIFEST}" 2>/dev/null || true

echo "Manifest created: ${MANIFEST}"
echo ""
echo "=== Cleanup Complete ==="
echo "Review the recommendations above and manually delete files as needed."
echo "Backup is available at: ${BACKUP_DIR}"

