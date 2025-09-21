# Quick Baserow Setup for Estate Planning CRM

## 🚀 Quick Start

1. **Run the setup script:**
   ```bash
   python3 simple_baserow_setup.py
   ```

2. **Follow the prompts:**
   - Open http://localhost in browser
   - Login/create Baserow account
   - Go to Settings → API Tokens
   - Create token named "Estate Planning"
   - Paste token into script

3. **Script will create:**
   - **Pipeline table** with all estate planning fields
   - **Follow-ups table** for email management
   - Test record to verify setup

4. **Generated files:**
   - `baserow_config.json` - Complete configuration
   - `n8n_settings.json` - Copy values to n8n Settings node
   - `pipeline_field_mapping.json` - Field mappings for workflow

## 📋 Tables Created

### Pipeline Table Fields:
- client_name, meeting_date, meeting_stage
- state, marital_status, age, estate_value
- num_beneficiaries, real_estate_count
- llc_interest, urgency_score
- next_steps, key_pain_points
- has_minor_children, business_owner

### Follow-ups Table Fields:
- client_name, email_subject, email_body
- status, created_date

## 🔧 Using with n8n

1. **Update Settings node** with values from `n8n_settings.json`
2. **Update Create Record nodes** with field mappings from `pipeline_field_mapping.json`
3. **Test with one transcript** before processing all 352 files

## ⚡ That's It!

Simple, practical setup for your local estate planning CRM.