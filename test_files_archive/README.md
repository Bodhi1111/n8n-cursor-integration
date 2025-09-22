# Test Files Archive

This directory contains test files that were created during development and testing phases. These files have been moved here to prevent project bloat while preserving them for reference.

## 📁 Contents

### Individual Client Test Files
- `test_abbot_ware_*.py` - Abbot Ware transcript testing
- `test_adele_nicols.py` - Adele Nicols transcript testing  
- `test_amanda_jennings.py` - Amanda Jennings transcript testing
- `test_georgia_garrison.py` - Georgia Garrison transcript testing
- `test_minimal_georgia.py` - Minimal Georgia testing
- `test_son_dinh.py` - Son Dinh transcript testing

### Core Test Files (Kept Active)
- `test_connections.py` - Connection testing (kept active)
- `test_full_pipeline.py` - Full pipeline testing (kept active)
- `test_gpt_oss.py` - GPT OSS testing (kept active)
- `test_minimal_baserow.py` - Minimal Baserow testing (kept active)
- `test_single_transcript_complete.py` - Complete transcript testing (kept active)

### Specialized Test Files
- `test_deal_detection.py` - Deal detection testing
- `test_estate_value_constraint.py` - Estate value constraint testing
- `test_field_by_field.py` - Field-by-field testing

## 🎯 Purpose

These files were moved here to:
1. **Prevent Project Bloat** - Avoid cluttering the main project directory
2. **Preserve History** - Keep test files for reference and debugging
3. **Maintain Clean Structure** - Keep only essential files in the main directory
4. **Enable Future Reference** - Allow access to specific client test cases when needed

## 🚀 Current Testing Approach

Going forward, use the centralized testing approach:

```bash
# Use the centralized test runner instead of creating new files
python transcript_test_runner.py --transcript <file> --client <name>

# For existing core tests, use the active test files
python test_single_transcript_complete.py
python test_full_pipeline.py
python test_connections.py
```

## 📋 Notes

- **Total Files Archived**: 16 test files
- **Active Test Files**: 5 core test files remain in main directory
- **Archived Date**: September 2024
- **Reason**: Prevent Claude Code from creating test file bloat

## 🔄 Restoration

If you need to restore any specific test file:
```bash
cp test_files_archive/test_specific_client.py ./
```

But consider using the centralized approach first:
```bash
python transcript_test_runner.py --transcript <file> --client <name>
```
