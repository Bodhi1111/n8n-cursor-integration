#!/usr/bin/env node
/**
 * BMAD Document Validator Agent
 * Quality assurance and data validation for estate planning extractions
 */

const fs = require('fs');
const path = require('path');

class DocumentValidator {
  constructor(config = {}) {
    this.qualityThresholds = {
      minimum: config.minimumScore || 60,
      auto_approve: config.autoApproveScore || 85,
      high_confidence: config.highConfidenceScore || 95
    };

    this.validationRules = this.initializeValidationRules();

    console.log(`🛡️ Document Validator Agent initialized`);
    console.log(`📊 Quality Thresholds: Min=${this.qualityThresholds.minimum}% Auto=${this.qualityThresholds.auto_approve}%`);
  }

  initializeValidationRules() {
    return {
      required_fields: {
        critical: ['client_name', 'meeting_stage'],
        important: ['estate_value', 'marital_status', 'state'],
        optional: ['urgency_score', 'next_steps', 'objections_raised']
      },

      format_validation: {
        email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        phone: /^\+?[\d\s\-\(\)\.]{10,}$/,
        date: /^\d{4}-\d{2}-\d{2}$/,
        state_code: /^[A-Z]{2}$/,
        currency: /^\$?[\d,]+(\.\d{2})?[KMB]?$/i
      },

      range_validation: {
        age: { min: 18, max: 120 },
        urgency_score: { min: 1, max: 10 },
        estate_value_numeric: { min: 0, max: 1000000000 },
        children_count: { min: 0, max: 20 }
      },

      enum_validation: {
        meeting_stage: ['Closed Won', 'Closed Lost', 'No Show', 'Follow Up'],
        marital_status: ['Single', 'Married', 'Divorced', 'Widowed'],
        entity_type: ['LLC', 'S-Corp', 'C-Corp', 'Partnership', 'Trust', 'Multiple', 'None']
      },

      logical_consistency: [
        {
          name: 'spouse_alignment',
          rule: 'if marital_status is Married, spouse_name should be present',
          validator: (data) => {
            if (data.marital_status === 'Married') {
              return data.spouse_name && data.spouse_name.trim().length > 0;
            }
            return true;
          }
        },
        {
          name: 'business_entity_alignment',
          rule: 'if business_owner is true, entity_type should not be None',
          validator: (data) => {
            if (data.business_owner === true || data.business_owner === 'true') {
              return data.entity_type && data.entity_type !== 'None';
            }
            return true;
          }
        },
        {
          name: 'children_beneficiary_alignment',
          rule: 'if has_minor_children is true, num_beneficiaries should be > 0',
          validator: (data) => {
            if (data.has_minor_children === true || data.has_minor_children === 'true') {
              const numBeneficiaries = parseInt(data.num_beneficiaries) || 0;
              return numBeneficiaries > 0;
            }
            return true;
          }
        },
        {
          name: 'estate_value_consistency',
          rule: 'estate_value should be consistent with tax_planning_priority',
          validator: (data) => {
            const estateValue = this.parseEstateValue(data.estate_value);
            const priority = data.tax_planning_priority;

            if (estateValue > 10000000 && priority !== 'critical') return false;
            if (estateValue < 1000000 && priority === 'critical') return false;
            return true;
          }
        }
      ]
    };
  }

  // Main validation method
  async validateDocument(extractedData, originalTranscript = null) {
    console.log(`🔍 Validating extracted data...`);

    const validation = {
      timestamp: new Date().toISOString(),
      overall_score: 0,
      quality_level: 'unknown',
      recommendation: 'unknown',
      field_validation: {},
      logical_validation: {},
      completeness_analysis: {},
      error_summary: [],
      warnings: [],
      auto_corrections: {}
    };

    try {
      // 1. Field-level validation
      validation.field_validation = this.validateFields(extractedData);

      // 2. Logical consistency validation
      validation.logical_validation = this.validateLogicalConsistency(extractedData);

      // 3. Completeness analysis
      validation.completeness_analysis = this.analyzeCompleteness(extractedData);

      // 4. Data quality scoring
      validation.overall_score = this.calculateQualityScore(
        validation.field_validation,
        validation.logical_validation,
        validation.completeness_analysis
      );

      // 5. Generate recommendations
      validation.quality_level = this.determineQualityLevel(validation.overall_score);
      validation.recommendation = this.generateRecommendation(validation);

      // 6. Auto-corrections where possible
      validation.auto_corrections = this.attemptAutoCorrections(extractedData);

      console.log(`✅ Validation complete - Score: ${validation.overall_score}% (${validation.quality_level})`);

      return validation;

    } catch (error) {
      console.error('❌ Validation failed:', error.message);
      validation.error_summary.push(`Validation process error: ${error.message}`);
      validation.overall_score = 0;
      validation.quality_level = 'failed';
      validation.recommendation = 'manual_review';
      return validation;
    }
  }

  validateFields(data) {
    const fieldValidation = {
      passed: 0,
      failed: 0,
      errors: {},
      warnings: {}
    };

    // Check required fields
    [...this.validationRules.required_fields.critical, ...this.validationRules.required_fields.important].forEach(field => {
      if (!data[field] || (typeof data[field] === 'string' && data[field].trim() === '')) {
        fieldValidation.errors[field] = 'Missing required field';
        fieldValidation.failed++;
      } else {
        fieldValidation.passed++;
      }
    });

    // Format validation
    Object.entries(this.validationRules.format_validation).forEach(([fieldType, pattern]) => {
      const relevantFields = Object.keys(data).filter(key =>
        key.includes(fieldType) || (fieldType === 'currency' && key.includes('value'))
      );

      relevantFields.forEach(field => {
        if (data[field] && !pattern.test(data[field])) {
          fieldValidation.errors[field] = `Invalid ${fieldType} format`;
          fieldValidation.failed++;
        }
      });
    });

    // Range validation
    Object.entries(this.validationRules.range_validation).forEach(([field, range]) => {
      if (data[field] !== undefined) {
        const value = parseFloat(data[field]);
        if (isNaN(value) || value < range.min || value > range.max) {
          fieldValidation.errors[field] = `Value out of range (${range.min}-${range.max})`;
          fieldValidation.failed++;
        }
      }
    });

    // Enum validation
    Object.entries(this.validationRules.enum_validation).forEach(([field, validValues]) => {
      if (data[field] && !validValues.includes(data[field])) {
        fieldValidation.errors[field] = `Invalid value. Expected: ${validValues.join(', ')}`;
        fieldValidation.failed++;
      }
    });

    return fieldValidation;
  }

  validateLogicalConsistency(data) {
    const logicalValidation = {
      passed: 0,
      failed: 0,
      inconsistencies: {}
    };

    this.validationRules.logical_consistency.forEach(rule => {
      const isValid = rule.validator(data);
      if (isValid) {
        logicalValidation.passed++;
      } else {
        logicalValidation.failed++;
        logicalValidation.inconsistencies[rule.name] = rule.rule;
      }
    });

    return logicalValidation;
  }

  analyzeCompleteness(data) {
    const completeness = {
      critical_fields: { completed: 0, total: this.validationRules.required_fields.critical.length },
      important_fields: { completed: 0, total: this.validationRules.required_fields.important.length },
      optional_fields: { completed: 0, total: this.validationRules.required_fields.optional.length },
      overall_percentage: 0
    };

    // Count completed fields
    this.validationRules.required_fields.critical.forEach(field => {
      if (data[field] && data[field].toString().trim() !== '') {
        completeness.critical_fields.completed++;
      }
    });

    this.validationRules.required_fields.important.forEach(field => {
      if (data[field] && data[field].toString().trim() !== '') {
        completeness.important_fields.completed++;
      }
    });

    this.validationRules.required_fields.optional.forEach(field => {
      if (data[field] && data[field].toString().trim() !== '') {
        completeness.optional_fields.completed++;
      }
    });

    // Calculate overall percentage
    const totalCompleted = completeness.critical_fields.completed +
                          completeness.important_fields.completed +
                          completeness.optional_fields.completed;

    const totalFields = completeness.critical_fields.total +
                       completeness.important_fields.total +
                       completeness.optional_fields.total;

    completeness.overall_percentage = Math.round((totalCompleted / totalFields) * 100);

    return completeness;
  }

  calculateQualityScore(fieldValidation, logicalValidation, completeness) {
    // Weighted scoring algorithm
    const weights = {
      field_accuracy: 0.4,      // 40% - Field format and presence
      logical_consistency: 0.3,  // 30% - Data makes sense together
      completeness: 0.3         // 30% - How much data we extracted
    };

    // Field accuracy score
    const totalFieldChecks = fieldValidation.passed + fieldValidation.failed;
    const fieldAccuracy = totalFieldChecks > 0 ? (fieldValidation.passed / totalFieldChecks) * 100 : 0;

    // Logical consistency score
    const totalLogicalChecks = logicalValidation.passed + logicalValidation.failed;
    const logicalConsistency = totalLogicalChecks > 0 ? (logicalValidation.passed / totalLogicalChecks) * 100 : 100;

    // Critical field bonus/penalty
    const criticalFieldScore = (completeness.critical_fields.completed / completeness.critical_fields.total) * 100;

    // Calculate weighted score
    let score = (fieldAccuracy * weights.field_accuracy) +
               (logicalConsistency * weights.logical_consistency) +
               (completeness.overall_percentage * weights.completeness);

    // Apply critical field penalty if any critical fields are missing
    if (criticalFieldScore < 100) {
      score *= (criticalFieldScore / 100);
    }

    return Math.round(Math.max(0, Math.min(100, score)));
  }

  determineQualityLevel(score) {
    if (score >= this.qualityThresholds.high_confidence) return 'excellent';
    if (score >= this.qualityThresholds.auto_approve) return 'good';
    if (score >= this.qualityThresholds.minimum) return 'acceptable';
    return 'poor';
  }

  generateRecommendation(validation) {
    const score = validation.overall_score;

    if (score >= this.qualityThresholds.auto_approve) {
      return 'auto_approve';
    } else if (score >= this.qualityThresholds.minimum) {
      if (validation.field_validation.failed > 0 || validation.logical_validation.failed > 0) {
        return 'review_and_correct';
      } else {
        return 'manual_review';
      }
    } else {
      return 'reject_and_reprocess';
    }
  }

  attemptAutoCorrections(data) {
    const corrections = {};

    // Auto-correct common format issues
    Object.keys(data).forEach(key => {
      const value = data[key];
      if (typeof value === 'string') {
        // Clean up name fields
        if (key.includes('name') && value) {
          const cleaned = value.replace(/[^\w\s\-\.]/g, '').trim();
          if (cleaned !== value) {
            corrections[key] = { original: value, corrected: cleaned, reason: 'Removed invalid characters' };
          }
        }

        // Standardize state codes
        if (key === 'state' && value.length > 2) {
          const stateMap = {
            'california': 'CA', 'texas': 'TX', 'florida': 'FL', 'new york': 'NY',
            'illinois': 'IL', 'pennsylvania': 'PA', 'ohio': 'OH', 'georgia': 'GA'
          };
          const standardized = stateMap[value.toLowerCase()];
          if (standardized) {
            corrections[key] = { original: value, corrected: standardized, reason: 'Standardized state code' };
          }
        }

        // Clean currency values
        if (key.includes('value') || key.includes('estate')) {
          const cleaned = value.replace(/[^\d\.,KMB]/gi, '');
          if (cleaned !== value && cleaned) {
            corrections[key] = { original: value, corrected: cleaned, reason: 'Cleaned currency format' };
          }
        }
      }
    });

    return corrections;
  }

  parseEstateValue(estateValue) {
    if (!estateValue) return 0;

    let numericValue = 0;
    const valueStr = estateValue.toString();

    const valueMatch = valueStr.match(/[\d,]+/);
    if (valueMatch) {
      numericValue = parseInt(valueMatch[0].replace(/,/g, ''));

      if (/million|M/i.test(valueStr)) {
        numericValue *= 1000000;
      } else if (/thousand|K/i.test(valueStr)) {
        numericValue *= 1000;
      } else if (/billion|B/i.test(valueStr)) {
        numericValue *= 1000000000;
      }
    }

    return numericValue;
  }

  // Generate validation report
  generateReport(validation, originalData) {
    const report = {
      summary: {
        overall_score: validation.overall_score,
        quality_level: validation.quality_level,
        recommendation: validation.recommendation,
        timestamp: validation.timestamp
      },
      details: {
        field_errors: Object.keys(validation.field_validation.errors).length,
        logical_inconsistencies: Object.keys(validation.logical_validation.inconsistencies).length,
        completeness_percentage: validation.completeness_analysis.overall_percentage,
        auto_corrections_applied: Object.keys(validation.auto_corrections).length
      },
      actions_required: this.generateActionItems(validation),
      corrected_data: this.applyCorrections(originalData, validation.auto_corrections)
    };

    return report;
  }

  generateActionItems(validation) {
    const actions = [];

    if (validation.field_validation.failed > 0) {
      actions.push(`Fix ${validation.field_validation.failed} field validation errors`);
    }

    if (validation.logical_validation.failed > 0) {
      actions.push(`Resolve ${validation.logical_validation.failed} logical inconsistencies`);
    }

    if (validation.completeness_analysis.critical_fields.completed < validation.completeness_analysis.critical_fields.total) {
      actions.push(`Complete missing critical fields`);
    }

    if (validation.overall_score < this.qualityThresholds.minimum) {
      actions.push(`Improve overall data quality (currently ${validation.overall_score}%)`);
    }

    return actions;
  }

  applyCorrections(originalData, corrections) {
    const correctedData = { ...originalData };

    Object.entries(corrections).forEach(([field, correction]) => {
      correctedData[field] = correction.corrected;
    });

    return correctedData;
  }

  // CLI interface
  async processFile(dataPath) {
    try {
      const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
      const validation = await this.validateDocument(data);
      const report = this.generateReport(validation, data);

      console.log(JSON.stringify(report, null, 2));
      return report;
    } catch (error) {
      console.error('❌ Processing failed:', error.message);
      return { error: error.message };
    }
  }
}

// CLI execution
if (require.main === module) {
  const dataPath = process.argv[2];

  if (!dataPath) {
    console.log('Usage: node document-validator.js <extracted-data.json>');
    console.log('Example: node document-validator.js /path/to/extracted-data.json');
    process.exit(1);
  }

  const validator = new DocumentValidator();
  validator.processFile(dataPath).catch(console.error);
}

module.exports = DocumentValidator;