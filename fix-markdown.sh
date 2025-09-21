#!/bin/bash

# Fix markdown formatting issues

echo "Fixing markdown formatting issues..."

# Fix README.md
sed -i '' '
# Add blank lines before headings that need them
s/^## 🛠 Available Scripts$/## 🛠 Available Scripts\n/g
s/^## 🔗 HTTP Request Templates$/## 🔗 HTTP Request Templates\n/g
s/^## 🐳 Docker Commands$/## 🐳 Docker Commands\n/g
s/^## 🧪 Local Testing$/## 🧪 Local Testing\n/g
s/^## 📝 Best Practices$/## 📝 Best Practices\n/g
s/^## 🔒 Security Notes$/## 🔒 Security Notes\n/g
s/^## 🚀 Advanced Features$/## 🚀 Advanced Features\n/g
s/^## 📚 Resources$/## 📚 Resources\n/g
s/^## 🤝 Contributing$/## 🤝 Contributing\n/g
s/^## 📄 License$/## 📄 License\n/g

# Add blank lines before lists
s/^### 1\. Script Development in Cursor IDE$/### 1. Script Development in Cursor IDE\n/g
s/^### 2\. n8n Workflow Development$/### 2. n8n Workflow Development\n/g
s/^### 3\. Integration Examples$/### 3. Integration Examples\n/g
s/^### 1\. Script Development$/### 1. Script Development\n/g
s/^### 2\. Workflow Design$/### 2. Workflow Design\n/g
s/^### 3\. Error Handling$/### 3. Error Handling\n/g

# Fix code blocks
s/^```$/```bash\n/g
' README.md

# Fix scripts/README.md
sed -i '' '
# Remove multiple blank lines
/^$/N;/^\n$/d

# Add blank lines before headings
s/^## 📋 Available Scripts$/## 📋 Available Scripts\n/g
s/^## 🧪 Testing Scripts$/## 🧪 Testing Scripts\n/g
s/^## 📝 Writing Custom Scripts$/## 📝 Writing Custom Scripts\n/g
s/^## 🔄 Integration with Cursor IDE$/## 🔄 Integration with Cursor IDE\n/g
s/^## 📚 n8n Function Node Tips$/## 📚 n8n Function Node Tips\n/g
s/^## 🚀 Advanced Patterns$/## 🚀 Advanced Patterns\n/g

# Add blank lines before lists
s/^### data-processor\.js$/### data-processor.js\n/g
s/^### api-payload-builder\.js$/### api-payload-builder.js\n/g
s/^### conditional-router\.js$/### conditional-router.js\n/g
s/^### file-processor\.js$/### file-processor.js\n/g

# Fix code blocks
s/^```$/```javascript\n/g
' scripts/README.md

echo "Markdown formatting fixes completed!"
