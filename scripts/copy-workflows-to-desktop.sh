#!/bin/bash

# Copy workflows to Desktop for easy import
echo "📁 Copying workflow files to Desktop..."

cp /Users/joshuavaughan/n8n-cursor-integration/workflows/sales-transcript-processor.json ~/Desktop/
cp /Users/joshuavaughan/n8n-cursor-integration/workflows/batch-transcript-processor.json ~/Desktop/

echo "✅ Workflow files copied to Desktop:"
echo "   - sales-transcript-processor.json"
echo "   - batch-transcript-processor.json"
echo ""
echo "🚀 Next steps:"
echo "1. Go to your n8n: http://localhost:5678"
echo "2. Import both workflow files from your Desktop"
echo "3. Configure API credentials (OpenAI + Notion)"
echo "4. Test with a sample transcript"