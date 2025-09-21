# n8n Function Node Scripts

This directory contains reusable JavaScript functions for n8n Function nodes. Each script is designed to be copied and pasted directly into n8n Function nodes.

## 📋 Available Scripts
### `data-processor.js`
**Purpose:** Transforms and validates incoming data
- Adds timestamps and computed fields
- Validates data quality
- Generates hashes for deduplication

**Usage:** Copy to a Function node after receiving data from webhooks or APIs

### `api-payload-builder.js`
**Purpose:** Builds structured API payloads
- Creates different payload types based on data
- Handles user, product, and generic data types
- Adds metadata and timestamps

**Usage:** Use before HTTP Request nodes to format data

### `conditional-router.js`
**Purpose:** Routes items to different outputs based on conditions
- Routes by priority, type, status
- Supports multiple output connections
- Adds routing metadata

**Usage:** Connect multiple outputs to create branching workflows

### `file-processor.js`
**Purpose:** Processes file metadata and information
- Extracts file properties
- Categorizes files by type
- Determines binary vs text files

**Usage:** Use after file upload triggers or file system operations

## 🧪 Testing Scripts
Test scripts locally before using in n8n:

```bash

# Test all scripts
npm run test

# Test specific script
node scripts/test-runner.js
```bash
## 📝 Writing Custom Scripts

When creating new scripts:

1. **Follow the n8n pattern:**
   ```javascript
   return items.map(item => {
     const data = item.json;
     // Your processing logic here
     return {
       json: processedData
     };
   });
   ```

2. **Handle edge cases:**
   ```javascript
   // Always validate input
   if (!data.message) {
     return { json: { error: 'Missing message field' } };
   }
   ```

3. **Add metadata:**
   ```javascript
   return {
     json: {
       ...data,
       processed_at: new Date().toISOString(),
       script_version: '1.0'
     }
   };
   ```

4. **Test with mock data:**
   ```javascript
   // Use the mockContext from test-runner.js
   const result = yourScript(mockContext.items, mockContext);
   ```

## 🔄 Integration with Cursor IDE
1. **Develop in Cursor:** Write and test scripts with full IDE features
2. **Local testing:** Use `npm run test` to validate logic
3. **Copy to n8n:** Paste working scripts into Function nodes
4. **Iterate:** Make changes in Cursor, test, then update n8n

## 📚 n8n Function Node Tips
- **Return format:** Always return an array of objects with `json` property
- **Item processing:** Use `items.map()` to process each item
- **Error handling:** Use try-catch blocks for robust error handling
- **Performance:** Keep functions lightweight for better performance
- **Debugging:** Use `console.log()` for debugging (visible in n8n logs)

## 🚀 Advanced Patterns
### Multiple Outputs
```javascript
// Return arrays for multiple outputs
return [
  highPriorityItems,  // Output 0
  normalItems,        // Output 1
  errorItems          // Output 2
];
```bash
### Binary Data Handling
```javascript
// Access binary data
const binaryData = item.binary?.data;
if (binaryData) {
  // Process binary data
}
```bash
### Dynamic Routing
```javascript
// Route based on data content
const outputIndex = data.priority === 'high' ? 0 : 1;
return [outputIndex === 0 ? [item] : [], outputIndex === 1 ? [item] : []];
```bash
