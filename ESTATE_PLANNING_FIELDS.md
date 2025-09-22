# Estate Planning CRM Fields Setup

## Manual Field Creation Required

Your API token has read/write permissions but cannot create fields. Please manually add these fields to your CRM table (ID: 698) in Baserow:

### Fields to Add

1. **meeting_stage** (Single Select)
   - Options: Closed Won (green), Closed Lost (red), No Show (gray), Follow Up (blue)

2. **marital_status** (Single Select)
   - Options: Single (blue), Married (green), Widowed (gray), Divorced (orange)

3. **children_count** (Number)
   - No negative numbers allowed

4. **estate_value** (Number)
   - 2 decimal places, no negative numbers

5. **has_real_estate** (Boolean/Checkbox)

6. **has_business** (Boolean/Checkbox)

7. **pain_points** (Long Text)

8. **objections** (Long Text)

9. **urgency_score** (Rating)
   - Max value: 10

10. **follow_up_required** (Boolean/Checkbox)

11. **transcript_file** (Text)

12. **processed_date** (Date & Time)

## How to Add Fields

1. Go to http://localhost
2. Open your CRM table
3. Click the "+" button to add new fields
4. Add each field with the specified type and options

## Configuration Generated

A `baserow_config.json` file has been created with your current setup:
- Database ID: 174
- CRM Table ID: 698
- API Token configured for read/write access

## Next Steps

After adding the fields manually:
1. The n8n workflow can use the existing configuration
2. Transcript processing will automatically populate these fields
3. Test record creation already works