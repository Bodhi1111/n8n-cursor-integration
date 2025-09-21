# Estate Planning n8n + Baserow + GPT-OSS:20B Setup Guide

## ✅ Current Status
- GPT-OSS:20B model: ✅ Installed and tested
- Workflow JSON: ✅ Fixed and ready to import
- Sample test: ✅ Successfully extracted data from transcript

## 🚀 Next Steps

### 1. Get Your Baserow Configuration

First, get your table IDs and create the required fields:

```bash
# Replace with your actual Baserow token
export BASEROW_TOKEN="your_token_here"

# Get your database tables
curl -H "Authorization: Token $BASEROW_TOKEN" \
  http://localhost/api/database/tables/database/1/ | python3 -m json.tool

# Get field IDs for your main table (replace TABLE_ID)
curl -H "Authorization: Token $BASEROW_TOKEN" \
  http://localhost/api/database/fields/table/TABLE_ID/ | python3 -m json.tool
```

### 2. Required Baserow Fields

**Main Estate Planning Table:**
1. Client Name (Text)
2. Meeting Date (Date)
3. State (Text)
4. Marital Status (Single select: Single|Married|Divorced|Widowed)
5. Age (Number)
6. Spouse Name (Text)
7. Estate Value (Text)
8. Number of Beneficiaries (Number)
9. Primary Beneficiaries (Long text)
10. Real Estate Count (Number)
11. Real Estate Locations (Long text)
12. LLC Interest (Single select: Yes|No|Maybe)
13. Entity Type (Single select: LLC|S-Corp|C-Corp|Partnership|Trust|Multiple|None)
14. Meeting Stage (Single select: Closed Won|Closed Lost|No Show|Follow Up)
15. Urgency Score (Number 1-5)
16. Next Steps (Long text)
17. Key Pain Points (Long text)
18. Decision Factors (Long text)
19. Objections Raised (Long text)
20. Follow Up Timeline (Text)
21. Has Minor Children (Checkbox)
22. Business Owner (Checkbox)
23. Meeting Quality (Single select: Excellent|Good|Fair|Poor)
24. Advisor Notes (Long text)
25. File Path (Text) - for tracking source file
26. Processing Status (Single select: Processed|Error)

**Follow-Up Email Table:**
1. Client Name (Text)
2. Email Subject (Text)
3. Email Body (Long text)
4. Status (Single select: Draft|Sent|Scheduled)
5. Created Date (Date)
6. Meeting Stage (Text)
7. Original Record ID (Text)

### 3. Import and Configure Workflow

1. **Import the workflow:**
   - Open n8n
   - Go to Workflows → Import from File
   - Select `estate-planning-workflow-fixed.json`

2. **Update the Settings node:**
   ```json
   {
     "tableId": "YOUR_MAIN_TABLE_ID",
     "emailTableId": "YOUR_EMAIL_TABLE_ID",
     "baserowToken": "YOUR_BASEROW_API_TOKEN"
   }
   ```

3. **Update field mappings:**
   Replace `field_1`, `field_2`, etc. with your actual Baserow field IDs (e.g., `field_12345`, `field_12346`)

### 4. Test with Single File

Before processing all 352 transcripts:

```bash
# Create test directory
mkdir -p ~/test-transcripts

# Copy one transcript file
cp "/Users/joshuavaughan/Documents/McAdams Transcripts/sample.txt" ~/test-transcripts/

# Update workflow path temporarily to ~/test-transcripts
```

### 5. Run Production Processing

After successful test:
1. Update path back to `/Users/joshuavaughan/Documents/McAdams Transcripts`
2. Run the workflow
3. Monitor progress in n8n execution logs
4. Check Baserow tables for populated data

## 🔧 Troubleshooting

### Common Issues:

**JSON Parsing Errors:**
- The regex in parse-json node handles multi-line JSON
- If issues persist, check GPT-OSS:20B response format

**Baserow Authentication:**
- Ensure token has proper permissions
- Verify table IDs are correct
- Check field IDs match exactly

**File Reading Issues:**
- Verify transcript directory path
- Ensure files are readable .txt format
- Check file permissions

### Performance Optimization:

**For 352 files:**
- Processing time: ~30-45 seconds per transcript
- Total time: ~4-5 hours
- Monitor system resources during processing
- Consider splitting into smaller batches if needed

## 📊 Expected Results

After processing, you'll have:
- ✅ Complete client database in Baserow
- ✅ Automatic follow-up email generation for prospects
- ✅ Sales pipeline tracking and analytics
- ✅ Structured data for reporting and analysis

The GPT-OSS:20B model will provide superior classification accuracy for nuanced estate planning scenarios compared to smaller models.