#!/bin/bash

# Script to generate PDF resume from cv.yml
# Usage: ./make_resume.sh [basic|enhanced|both]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📄 Wei Fu Resume Generator${NC}"
echo -e "${BLUE}=========================${NC}"

# Check if cv.yml exists
if [ ! -f "_data/cv.yml" ]; then
    echo -e "${RED}❌ Error: _data/cv.yml not found!${NC}"
    exit 1
fi

# Check if Python packages are installed
echo -e "${YELLOW}🔍 Checking dependencies...${NC}"
python3 -c "import reportlab, yaml" 2>/dev/null || {
    echo -e "${YELLOW}📦 Installing required packages...${NC}"
    pip install reportlab PyYAML
}

# Determine which version to generate
VERSION="${1:-both}"

case $VERSION in
    "basic")
        echo -e "${YELLOW}📝 Generating basic resume...${NC}"
        python3 generate_resume.py
        echo -e "${GREEN}✅ Basic resume generated: Wei_Fu_Resume.pdf${NC}"
        ;;
    "enhanced")
        echo -e "${YELLOW}📝 Generating enhanced resume...${NC}"
        python3 generate_resume_enhanced.py
        echo -e "${GREEN}✅ Enhanced resume generated: Wei_Fu_Resume_Enhanced.pdf${NC}"
        ;;
    "both"|*)
        echo -e "${YELLOW}📝 Generating both resume versions...${NC}"
        python3 generate_resume_enhanced.py
        echo -e "${GREEN}✅ Both resume versions generated!${NC}"
        ;;
esac

# Show file information
echo
echo -e "${BLUE}📊 Generated Files:${NC}"
for file in Wei_Fu_Resume*.pdf; do
    if [ -f "$file" ]; then
        size=$(ls -lh "$file" | awk '{print $5}')
        echo -e "  📄 $file (${size})"
    fi
done

echo
echo -e "${GREEN}🎉 Resume generation complete!${NC}"
echo -e "${BLUE}Tip: Use './make_resume.sh basic' for basic version only${NC}"
echo -e "${BLUE}     Use './make_resume.sh enhanced' for enhanced version only${NC}"
