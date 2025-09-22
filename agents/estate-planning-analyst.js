#!/usr/bin/env node
/**
 * BMAD Estate Planning Analyst Agent
 * Specialized transcript analysis for estate planning scenarios
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');

class EstatePlanningAnalyst {
  constructor(config = {}) {
    this.ollamaUrl = config.ollamaUrl || 'http://localhost:11434';
    this.model = config.model || 'gpt-oss:20b';
    this.temperature = config.temperature || 0.1;
    this.baserowConfig = this.loadBaserowConfig();

    // Agent persona and expertise
    this.persona = {
      name: "Estate Planning Analyst",
      expertise: "20+ years estate planning, family law, business succession",
      specialization: ["family_structure", "asset_classification", "risk_assessment"],
      tone: "analytical, thorough, detail-oriented"
    };

    console.log(`🎯 Estate Planning Analyst Agent initialized`);
    console.log(`📊 Model: ${this.model} | Expertise: ${this.persona.specialization.join(', ')}`);
  }

  loadBaserowConfig() {
    try {
      const configPath = path.join(__dirname, '../baserow_config.json');
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      return config.baserow;
    } catch (error) {
      console.warn('⚠️ Baserow config not found, using defaults');
      return {
        base_url: 'http://localhost',
        database_id: '174',
        tables: { CRM: { id: '698' } }
      };
    }
  }

  // Advanced family structure analysis
  analyzeFamilyStructure(transcript) {
    const familyPatterns = {
      blended_family: [
        /step[\-\s]?children?/gi,
        /previous marriage/gi,
        /ex[\-\s]?(wife|husband|spouse)/gi,
        /half[\-\s]?(brother|sister|sibling)/gi,
        /from (my|his|her) first marriage/gi
      ],
      special_needs: [
        /special needs/gi,
        /disabled (child|beneficiary)/gi,
        /special trust/gi,
        /supplemental needs trust/gi,
        /ABLE account/gi
      ],
      minor_children: [
        /(\d+)[\-\s]?year[\-\s]?old/gi,
        /minor children?/gi,
        /under 18/gi,
        /guardianship/gi,
        /education fund/gi
      ],
      family_conflict: [
        /estranged/gi,
        /don't speak to/gi,
        /family drama/gi,
        /contentious/gi,
        /lawsuit/gi
      ]
    };

    const analysis = {
      complexity_score: 0,
      risk_factors: [],
      special_considerations: []
    };

    Object.entries(familyPatterns).forEach(([category, patterns]) => {
      const matches = patterns.some(pattern => pattern.test(transcript));
      if (matches) {
        analysis.complexity_score += 1;
        analysis.risk_factors.push(category);

        switch(category) {
          case 'blended_family':
            analysis.special_considerations.push('Requires careful beneficiary designation and potential trust structures');
            break;
          case 'special_needs':
            analysis.special_considerations.push('Must preserve government benefits eligibility');
            break;
          case 'minor_children':
            analysis.special_considerations.push('Guardianship provisions and age-based distributions needed');
            break;
          case 'family_conflict':
            analysis.special_considerations.push('Consider dispute resolution mechanisms and clear documentation');
            break;
        }
      }
    });

    return analysis;
  }

  // Business entity classification with precision
  classifyBusinessEntities(transcript) {
    const entityPatterns = {
      LLC: [
        /\bLLC\b/gi,
        /Limited Liability Company/gi,
        /operating agreement/gi
      ],
      'S-Corp': [
        /S[\-\s]?Corp/gi,
        /S[\-\s]?Corporation/gi,
        /pass[\-\s]?through tax/gi
      ],
      'C-Corp': [
        /C[\-\s]?Corp/gi,
        /C[\-\s]?Corporation/gi,
        /double tax/gi,
        /corporate tax/gi
      ],
      Partnership: [
        /partnership/gi,
        /general partner/gi,
        /limited partner/gi,
        /partnership agreement/gi
      ],
      'Sole Proprietorship': [
        /sole proprietor/gi,
        /Schedule C/gi,
        /self[\-\s]?employed/gi
      ],
      Trust: [
        /family trust/gi,
        /revocable trust/gi,
        /irrevocable trust/gi,
        /trustee/gi
      ]
    };

    const entities = [];
    const businessComplexity = {
      entity_count: 0,
      succession_planning_needed: false,
      valuation_required: false
    };

    Object.entries(entityPatterns).forEach(([entityType, patterns]) => {
      patterns.forEach(pattern => {
        const matches = transcript.match(pattern);
        if (matches) {
          entities.push({
            type: entityType,
            mentions: matches.length,
            confidence: this.calculateEntityConfidence(transcript, pattern)
          });
          businessComplexity.entity_count++;
        }
      });
    });

    // Determine succession planning needs
    const successionKeywords = /succession|buy[\-\s]?sell|continuity|key person/gi;
    businessComplexity.succession_planning_needed = successionKeywords.test(transcript);

    // Check if valuation is needed
    const valuationKeywords = /appraisal|valuation|fair market value|business worth/gi;
    businessComplexity.valuation_required = valuationKeywords.test(transcript);

    return { entities, complexity: businessComplexity };
  }

  calculateEntityConfidence(transcript, pattern) {
    const contextWindow = 50; // words around the match
    const matches = [...transcript.matchAll(new RegExp(pattern.source, 'gi'))];

    let totalConfidence = 0;
    matches.forEach(match => {
      const start = Math.max(0, match.index - contextWindow);
      const end = Math.min(transcript.length, match.index + match[0].length + contextWindow);
      const context = transcript.slice(start, end);

      // Higher confidence if mentioned with ownership, management terms
      const contextBoosts = [
        /own/gi, /manage/gi, /partner/gi, /member/gi, /shareholder/gi
      ];

      let confidence = 0.6; // base confidence
      contextBoosts.forEach(boost => {
        if (boost.test(context)) confidence += 0.1;
      });

      totalConfidence += Math.min(confidence, 1.0);
    });

    return totalConfidence / matches.length || 0;
  }

  // Estate tax exposure assessment
  assessEstateExposure(estateValue, year = 2024) {
    const exemptionAmount = 13610000; // 2024 federal exemption
    const taxRate = 0.40; // 40% tax rate above exemption

    let numericValue = 0;

    // Parse estate value from various formats
    if (typeof estateValue === 'string') {
      const valueMatch = estateValue.match(/[\d,]+/);
      if (valueMatch) {
        numericValue = parseInt(valueMatch[0].replace(/,/g, ''));

        // Check for millions notation
        if (/million/i.test(estateValue)) {
          numericValue *= 1000000;
        } else if (/thousand/i.test(estateValue)) {
          numericValue *= 1000;
        }
      }
    } else {
      numericValue = estateValue;
    }

    const exposure = {
      estate_value: numericValue,
      exemption_amount: exemptionAmount,
      taxable_amount: Math.max(0, numericValue - exemptionAmount),
      estimated_tax: Math.max(0, (numericValue - exemptionAmount) * taxRate),
      tax_planning_priority: 'low'
    };

    if (exposure.taxable_amount > 0) {
      exposure.tax_planning_priority = 'critical';
    } else if (numericValue > exemptionAmount * 0.8) {
      exposure.tax_planning_priority = 'high';
    } else if (numericValue > exemptionAmount * 0.5) {
      exposure.tax_planning_priority = 'medium';
    }

    return exposure;
  }

  // Generate enhanced analysis prompt
  generateAnalysisPrompt(transcript) {
    return `You are a Senior Estate Planning Attorney with 20+ years of experience. Analyze this client transcript with the precision of a legal expert.

FAMILY STRUCTURE ANALYSIS (Critical for estate planning):
- Identify ALL family members mentioned (spouse, children, parents, siblings)
- Note ages, relationships, and any special circumstances
- Flag blended family situations, special needs beneficiaries
- Assess potential family conflicts or complications

ASSET CATEGORIZATION (Precise classification needed):
- Real Estate: Primary residence vs investment properties
- Business Interests: LLC, S-Corp, C-Corp, Partnership ownership percentages
- Retirement Accounts: 401k, IRA, pension plans
- Personal Property: Valuable items, collectibles, vehicles
- Financial Accounts: Bank accounts, investments, insurance

ESTATE PLANNING GAPS (Risk assessment):
- Current planning status (existing wills, trusts, powers of attorney)
- Liquidity concerns for estate settlement
- Business succession planning needs
- Tax optimization opportunities
- Guardianship provisions for minor children

MEETING OUTCOME CLASSIFICATION (Be precise):
- CLOSED WON: Explicit commitment, signed agreement, payment made
- FOLLOW UP: Interested but needs time, additional info, or spouse discussion
- CLOSED LOST: Explicit decline, chose competitor, cannot afford
- NO SHOW: Meeting didn't occur

URGENCY FACTORS (Scale 1-10):
- Health concerns mentioned
- Tax deadline pressures
- Business sale/transition timing
- Family situations requiring immediate attention
- Existing plan inadequacy

TRANSCRIPT TO ANALYZE:
${transcript}

Return comprehensive JSON analysis focusing on estate planning implications and next steps.`;
  }

  // Main analysis method
  async analyzeTranscript(transcriptPath) {
    try {
      console.log(`🔍 Analyzing transcript: ${path.basename(transcriptPath)}`);

      const transcript = fs.readFileSync(transcriptPath, 'utf8');
      const startTime = Date.now();

      // Run parallel analysis
      const [familyAnalysis, businessAnalysis] = await Promise.all([
        this.analyzeFamilyStructure(transcript),
        this.classifyBusinessEntities(transcript)
      ]);

      // Generate enhanced prompt
      const enhancedPrompt = this.generateAnalysisPrompt(transcript);

      // Call Ollama for main analysis
      const ollamaResponse = await axios.post(`${this.ollamaUrl}/api/generate`, {
        model: this.model,
        prompt: enhancedPrompt,
        stream: false,
        temperature: this.temperature,
        options: {
          num_predict: 2000,
          top_k: 10,
          top_p: 0.9
        }
      });

      let extractedData;
      try {
        // Clean and parse JSON response with improved extraction
        const responseText = ollamaResponse.data.response.trim();

        // Try multiple JSON extraction strategies
        let jsonText = null;

        // Strategy 1: Look for JSON block between ```json and ```
        const jsonBlockMatch = responseText.match(/```json\s*([\s\S]*?)\s*```/);
        if (jsonBlockMatch) {
          jsonText = jsonBlockMatch[1].trim();
        } else {
          // Strategy 2: Look for complete JSON object
          const jsonMatch = responseText.match(/\{[\s\S]*\}/);
          if (jsonMatch) {
            jsonText = jsonMatch[0];
          } else {
            // Strategy 3: Extract first complete JSON-like structure
            const lines = responseText.split('\n');
            let inJson = false;
            let braceCount = 0;
            let jsonLines = [];

            for (const line of lines) {
              if (line.trim().startsWith('{')) {
                inJson = true;
                braceCount = 0;
              }

              if (inJson) {
                jsonLines.push(line);
                braceCount += (line.match(/\{/g) || []).length;
                braceCount -= (line.match(/\}/g) || []).length;

                if (braceCount === 0 && line.includes('}')) {
                  jsonText = jsonLines.join('\n');
                  break;
                }
              }
            }
          }
        }

        if (jsonText) {
          // Clean up common JSON issues
          jsonText = jsonText
            .replace(/,\s*}/g, '}')  // Remove trailing commas
            .replace(/,\s*]/g, ']')  // Remove trailing commas in arrays
            .replace(/\\n/g, '\\\\n') // Escape newlines properly
            .replace(/‑/g, '-')      // Replace em dash with regular dash
            .replace(/'/g, "'")      // Replace smart quotes
            .replace(/"/g, '"')      // Replace smart quotes
            .replace(/"/g, '"')      // Replace smart quotes
            .replace(/\u00A0/g, ' ') // Replace non-breaking spaces
            .replace(/\u2013/g, '-') // Replace en dash
            .replace(/\u2014/g, '-') // Replace em dash
            .replace(/\u2019/g, "'") // Replace right single quotation mark
            .replace(/\u201C/g, '"') // Replace left double quotation mark
            .replace(/\u201D/g, '"'); // Replace right double quotation mark

          extractedData = JSON.parse(jsonText);
        } else {
          throw new Error('No JSON structure found in response');
        }
      } catch (parseError) {
        console.error('❌ JSON parsing failed:', parseError.message);
        console.error('📄 Raw response (first 500 chars):', ollamaResponse.data.response.substring(0, 500));
        extractedData = {
          error: 'Failed to parse LLM response',
          parse_error: parseError.message,
          raw_response_preview: ollamaResponse.data.response.substring(0, 200)
        };
      }

      // Enhance with agent analysis
      const enhancedData = {
        ...extractedData,
        agent_analysis: {
          family_structure: familyAnalysis,
          business_entities: businessAnalysis,
          estate_tax_exposure: this.assessEstateExposure(extractedData.estate_value),
          processing_metadata: {
            agent: this.persona.name,
            processing_time_ms: Date.now() - startTime,
            confidence_score: this.calculateOverallConfidence(extractedData, familyAnalysis, businessAnalysis),
            transcript_file: path.basename(transcriptPath)
          }
        }
      };

      console.log(`✅ Analysis complete in ${Date.now() - startTime}ms`);
      console.log(`📊 Confidence: ${enhancedData.agent_analysis.processing_metadata.confidence_score}%`);

      return enhancedData;

    } catch (error) {
      console.error('❌ Analysis failed:', error.message);
      return {
        error: error.message,
        transcript_file: path.basename(transcriptPath),
        agent: this.persona.name
      };
    }
  }

  calculateOverallConfidence(basicData, familyAnalysis, businessAnalysis) {
    let confidence = 50; // base confidence

    // Boost confidence based on data completeness
    const criticalFields = ['client_name', 'meeting_stage', 'estate_value'];
    const completedCritical = criticalFields.filter(field => basicData[field]).length;
    confidence += (completedCritical / criticalFields.length) * 30;

    // Boost for detected complexity (shows thorough analysis)
    if (familyAnalysis.complexity_score > 0) confidence += 10;
    if (businessAnalysis.entities.length > 0) confidence += 10;

    return Math.min(Math.round(confidence), 100);
  }

  // CLI interface
  async processFile(filePath) {
    const result = await this.analyzeTranscript(filePath);
    console.log(JSON.stringify(result, null, 2));
    return result;
  }
}

// CLI execution
if (require.main === module) {
  const filePath = process.argv[2];

  if (!filePath) {
    console.log('Usage: node estate-planning-analyst.js <transcript-file>');
    console.log('Example: node estate-planning-analyst.js /path/to/transcript.txt');
    process.exit(1);
  }

  const analyst = new EstatePlanningAnalyst();
  analyst.processFile(filePath).catch(console.error);
}

module.exports = EstatePlanningAnalyst;