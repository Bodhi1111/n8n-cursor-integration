# New Notion Database Columns to Add

## Add These Columns to Your SALES REPORT DASHBOARD

### Client Information Columns
| Column Name | Type | Options/Notes |
|-------------|------|---------------|
| **State** | Text | State of residence (2-letter code) |
| **Marital Status** | Select | Single, Married, Divorced, Widowed |
| **Age** | Text | Client's age |
| **Spouse Name** | Text | If married |

### Beneficiary Columns
| Column Name | Type | Notes |
|-------------|------|-------|
| **Beneficiaries Count** | Number | Total number of beneficiaries |
| **Primary Beneficiaries** | Text | Names and relationships |
| **Contingent Beneficiaries** | Text | Backup beneficiaries |

### Estate Information Columns
| Column Name | Type | Notes |
|-------------|------|-------|
| **Estate Value** | Text | Total estate value |
| **Estate Complexity** | Select | Simple, Moderate, Complex |

### Real Estate Columns
| Column Name | Type | Notes |
|-------------|------|-------|
| **Real Estate** | Checkbox | Has real estate? |
| **Properties Count** | Number | Number of properties |
| **Property Locations** | Text | States/locations of properties |

### Entity Formation Columns
| Column Name | Type | Notes |
|-------------|------|-------|
| **LLC Interest** | Checkbox | Interested in LLC formation? |
| **Entity Type** | Select | LLC, Corporation, Partnership, None |

### Planning Documents Columns
| Column Name | Type | Options |
|-------------|------|---------|
| **Needs Will** | Select | Yes, No, Already Has |
| **Needs Trust** | Select | Yes, No, Already Has |
| **Trust Type** | Text | Living, Revocable, Irrevocable, etc |
| **Needs POA** | Select | Yes, No, Already Has |
| **Healthcare Directive** | Select | Yes, No, Already Has |

### Family Information Columns
| Column Name | Type | Notes |
|-------------|------|-------|
| **Children Count** | Number | Number of children |
| **Minor Children** | Checkbox | Has minor children? |

### Financial Assets Columns
| Column Name | Type | Notes |
|-------------|------|-------|
| **Retirement Accounts** | Text | 401k, IRA, etc |
| **Life Insurance** | Text | Coverage amount |
| **Business Ownership** | Text | Business details |

### Timeline Columns
| Column Name | Type | Options |
|-------------|------|---------|
| **Urgency** | Select | High, Medium, Low |
| **Timeline Driver** | Text | Why urgent? |
| **Desired Completion** | Text | When they want it done |

### Processing Metadata
| Column Name | Type | Notes |
|-------------|------|-------|
| **Source File** | Text | Original transcript filename |
| **Batch Processed** | Checkbox | Processed via batch? |
| **Processed Date** | Date | When processed |

## How to Add These Columns

1. **Open your Notion database**
2. **Click the "+" button** at the end of your column headers
3. **Add each column** with the specified type
4. **For Select columns**, add the options listed
5. **Save your database**

## The Enhanced Notes Field

The **Notes** column will now contain a comprehensive structured analysis including:

- **Client Information Summary**
- **Estate Overview**
- **Complete Beneficiary Details**
- **Real Estate Holdings**
- **Financial Assets Breakdown**
- **Planning Needs Assessment**
- **Family Dynamics**
- **Key Concerns and Action Items**
- **Notable Quotes from Meeting**

This gives you both:
1. **Quick reference data** in individual columns
2. **Complete detailed analysis** in the Notes field

## After Adding Columns

1. Import the new workflow: `estate-planning-processor-enhanced.json`
2. Update the Notion Database ID in the workflow
3. Test with one transcript first
4. Run batch processing on all 352 files