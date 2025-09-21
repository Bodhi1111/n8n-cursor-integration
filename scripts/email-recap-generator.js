/**
 * Email Recap Generator
 * Generates professional follow-up emails from sales meeting data
 */

class EmailRecapGenerator {
  constructor() {
    this.templates = {
      followUp: this.createFollowUpTemplate(),
      proposal: this.createProposalTemplate(),
      demo: this.createDemoTemplate(),
      closing: this.createClosingTemplate()
    };
  }

  /**
   * Generate email recap based on sales data
   * @param {Object} salesData - Extracted sales data
   * @returns {Object} Email content and metadata
   */
  generateRecap(salesData) {
    try {
      const meetingType = this.determineMeetingType(salesData);
      const template = this.selectTemplate(meetingType, salesData.salesStage);

      const emailContent = this.populateTemplate(template, salesData);

      return {
        ...salesData,
        emailRecap: emailContent.body,
        emailSubject: emailContent.subject,
        emailType: meetingType,
        recipientEmail: this.extractPrimaryEmail(salesData.contactInfo),
        ccEmails: this.extractCCEmails(salesData.contactInfo),
        priority: this.determinePriority(salesData),
        sendTimestamp: this.calculateOptimalSendTime(),
        followUpDate: this.calculateFollowUpDate(salesData.nextSteps),
        generatedAt: new Date().toISOString()
      };
    } catch (error) {
      console.error('Error generating email recap:', error);
      return {
        ...salesData,
        emailGenerationError: error.message,
        emailStatus: 'failed'
      };
    }
  }

  /**
   * Determine the type of meeting from sales data
   */
  determineMeetingType(salesData) {
    const stage = salesData.salesStage?.toLowerCase();
    const nextSteps = salesData.nextSteps || [];

    if (stage === 'proposal' || nextSteps.some(step => step.action?.includes('proposal'))) {
      return 'proposal';
    }
    if (stage === 'solution_presentation' || nextSteps.some(step => step.action?.includes('demo'))) {
      return 'demo';
    }
    if (stage === 'closing' || stage === 'negotiation') {
      return 'closing';
    }
    return 'followUp';
  }

  /**
   * Select appropriate template
   */
  selectTemplate(meetingType, salesStage) {
    return this.templates[meetingType] || this.templates.followUp;
  }

  /**
   * Create follow-up email template
   */
  createFollowUpTemplate() {
    return {
      subject: "Follow-up from our {{meetingType}} meeting - {{companyName}}",
      body: `Hi {{primaryContactName}},

Thank you for taking the time to speak with us {{meetingDate}}. I really enjoyed our conversation about {{topPainPoint}} and how it's impacting {{companyName}}.

## Key Discussion Points:
{{#each painPoints}}
• {{this.description}}{{#if this.impact}} - {{this.impact}}{{/if}}
{{/each}}

## Your Requirements:
{{#each requirements}}
• {{this.requirement}}{{#if this.priority}} ({{this.priority}}){{/if}}
{{/each}}

## Next Steps:
{{#each nextSteps}}
{{@index}}. {{this.action}}{{#if this.timeline}} - {{this.timeline}}{{/if}}
{{/each}}

Based on our discussion, I understand you're looking to {{primaryRequirement}} and that {{urgencyIndicator}}.

{{#if budgetIndicators.range}}
Budget Range Discussed: {{budgetIndicators.range}}
{{/if}}

{{#if competitors}}
## Competitive Considerations:
We discussed how our solution differs from {{competitors}}, particularly in {{differentiationKey}}.
{{/if}}

I'll follow up {{followUpTimeline}} with {{nextDeliverable}}.

Best regards,
{{senderName}}

P.S. {{personalNote}}`
    };
  }

  /**
   * Create proposal follow-up template
   */
  createProposalTemplate() {
    return {
      subject: "Proposal and next steps - {{companyName}}",
      body: `Hi {{primaryContactName}},

Thank you for the productive proposal discussion today. I'm excited about the opportunity to help {{companyName}} {{primaryObjective}}.

## Proposal Overview:
• Solution: {{proposedSolution}}
• Investment: {{budgetRange}}
• Timeline: {{implementationTimeline}}
• ROI: {{expectedROI}}

## Key Benefits for {{companyName}}:
{{#each painPoints}}
• Addresses {{this.description}}: {{this.proposedSolution}}
{{/each}}

## Next Steps:
{{#each nextSteps}}
{{@index}}. {{this.action}} - {{this.owner}} by {{this.timeline}}
{{/each}}

## Decision Timeline:
{{decisionTimeline}}

{{#if stakeholders}}
I understand {{stakeholders}} will be involved in the decision process. Please let me know if you'd like me to prepare any additional materials for them.
{{/if}}

Looking forward to moving forward together!

Best regards,
{{senderName}}`
    };
  }

  /**
   * Create demo follow-up template
   */
  createDemoTemplate() {
    return {
      subject: "Demo recap and resources - {{companyName}}",
      body: `Hi {{primaryContactName}},

I hope you found today's demo valuable! It was great to show you how our solution can specifically address {{topPainPoint}} for {{companyName}}.

## Demo Highlights:
{{#each demoHighlights}}
• {{this}}
{{/each}}

## Features that resonated:
{{#each resonatedFeatures}}
• {{this.feature}}: {{this.benefit}}
{{/each}}

## Resources:
{{#each resources}}
• {{this.title}}: {{this.url}}
{{/each}}

## Questions from the demo:
{{#each demoQuestions}}
• Q: {{this.question}}
• A: {{this.answer}}
{{/each}}

## Next Steps:
{{#each nextSteps}}
{{@index}}. {{this.action}} {{#if this.owner}}({{this.owner}}){{/if}} - {{this.timeline}}
{{/each}}

{{#if trialOffered}}
I've set up your trial environment as discussed. You'll receive login credentials within 24 hours.
{{/if}}

Feel free to reach out with any questions!

Best regards,
{{senderName}}`
    };
  }

  /**
   * Create closing email template
   */
  createClosingTemplate() {
    return {
      subject: "Ready to move forward - {{companyName}}",
      body: `Hi {{primaryContactName}},

Great discussion today about finalizing our partnership. I'm excited about {{companyName}}'s decision to move forward with our solution.

## Final Details:
• Start Date: {{startDate}}
• Contract Term: {{contractTerm}}
• Investment: {{finalInvestment}}
• Implementation Lead: {{implementationLead}}

## Immediate Next Steps:
{{#each nextSteps}}
{{@index}}. {{this.action}} - {{this.owner}} by {{this.timeline}}
{{/each}}

## Implementation Timeline:
{{implementationTimeline}}

{{#if contractReview}}
I understand the contract is currently under review with {{contractReviewer}}. Please let me know if any questions arise during the review process.
{{/if}}

Welcome to the {{companyName}} family! I look forward to a successful partnership.

Best regards,
{{senderName}}`
    };
  }

  /**
   * Populate template with sales data
   */
  populateTemplate(template, salesData) {
    let subject = template.subject;
    let body = template.body;

    // Replace placeholders with actual data
    const replacements = {
      meetingType: salesData.meetingType || 'meeting',
      companyName: salesData.companyName || 'your company',
      primaryContactName: this.getPrimaryContactName(salesData.contactInfo),
      meetingDate: this.formatMeetingDate(salesData.meetingDate),
      topPainPoint: this.getTopPainPoint(salesData.painPoints),
      primaryRequirement: this.getPrimaryRequirement(salesData.requirements),
      urgencyIndicator: this.getUrgencyIndicator(salesData.sentiment?.urgency, salesData.nextSteps),
      followUpTimeline: this.getFollowUpTimeline(salesData.nextSteps),
      nextDeliverable: this.getNextDeliverable(salesData.nextSteps),
      senderName: '{{SENDER_NAME}}', // To be replaced by environment variable
      personalNote: this.generatePersonalNote(salesData.keyQuotes)
    };

    // Simple template replacement (in production, use a proper template engine)
    for (const [key, value] of Object.entries(replacements)) {
      const regex = new RegExp(`{{${key}}}`, 'g');
      subject = subject.replace(regex, value);
      body = body.replace(regex, value);
    }

    // Handle arrays and complex objects
    body = this.replaceArrayPlaceholders(body, salesData);

    return { subject, body };
  }

  /**
   * Replace array placeholders in template
   */
  replaceArrayPlaceholders(body, salesData) {
    // Replace pain points
    if (body.includes('{{#each painPoints}}')) {
      const painPointsSection = salesData.painPoints?.map(pp =>
        `• ${pp.description || pp}${pp.impact ? ' - ' + pp.impact : ''}`
      ).join('\n') || '• No specific pain points identified';

      body = body.replace(/{{#each painPoints}}[\s\S]*?{{\/each}}/g, painPointsSection);
    }

    // Replace next steps
    if (body.includes('{{#each nextSteps}}')) {
      const nextStepsSection = salesData.nextSteps?.map((step, index) =>
        `${index + 1}. ${step.action || step}${step.timeline ? ' - ' + step.timeline : ''}`
      ).join('\n') || '1. Follow up as discussed';

      body = body.replace(/{{#each nextSteps}}[\s\S]*?{{\/each}}/g, nextStepsSection);
    }

    // Replace requirements
    if (body.includes('{{#each requirements}}')) {
      const requirementsSection = salesData.requirements?.map(req =>
        `• ${req.requirement || req}${req.priority ? ' (' + req.priority + ')' : ''}`
      ).join('\n') || '• No specific requirements discussed';

      body = body.replace(/{{#each requirements}}[\s\S]*?{{\/each}}/g, requirementsSection);
    }

    return body;
  }

  /**
   * Extract primary contact name
   */
  getPrimaryContactName(contactInfo) {
    if (!contactInfo || !Array.isArray(contactInfo) || contactInfo.length === 0) {
      return 'there';
    }

    // Look for decision maker first, then any contact
    const decisionMaker = contactInfo.find(c => c.role === 'decision_maker');
    return decisionMaker?.name || contactInfo[0]?.name || 'there';
  }

  /**
   * Extract primary email
   */
  extractPrimaryEmail(contactInfo) {
    if (!contactInfo || !Array.isArray(contactInfo)) return null;

    const decisionMaker = contactInfo.find(c => c.role === 'decision_maker' && c.email);
    return decisionMaker?.email || contactInfo.find(c => c.email)?.email || null;
  }

  /**
   * Extract CC emails
   */
  extractCCEmails(contactInfo) {
    if (!contactInfo || !Array.isArray(contactInfo)) return [];

    return contactInfo
      .filter(c => c.email && c.role !== 'decision_maker')
      .map(c => c.email);
  }

  /**
   * Format meeting date
   */
  formatMeetingDate(meetingDate) {
    if (!meetingDate) return 'recently';

    try {
      const date = new Date(meetingDate);
      const today = new Date();
      const diffTime = Math.abs(today - date);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

      if (diffDays === 0) return 'today';
      if (diffDays === 1) return 'yesterday';
      if (diffDays <= 7) return `${diffDays} days ago`;

      return date.toLocaleDateString();
    } catch (error) {
      return 'recently';
    }
  }

  /**
   * Get top pain point
   */
  getTopPainPoint(painPoints) {
    if (!painPoints || !Array.isArray(painPoints) || painPoints.length === 0) {
      return 'your business challenges';
    }

    // Look for high urgency pain points first
    const urgentPain = painPoints.find(p => p.urgency === 'high');
    return urgentPain?.description || painPoints[0]?.description || painPoints[0] || 'your business challenges';
  }

  /**
   * Get primary requirement
   */
  getPrimaryRequirement(requirements) {
    if (!requirements || !Array.isArray(requirements) || requirements.length === 0) {
      return 'address your business needs';
    }

    const mustHave = requirements.find(r => r.priority === 'must_have');
    return mustHave?.requirement || requirements[0]?.requirement || requirements[0] || 'address your business needs';
  }

  /**
   * Get urgency indicator
   */
  getUrgencyIndicator(urgency, nextSteps) {
    if (urgency === 'high') return 'this is a high priority initiative';
    if (urgency === 'low') return 'you\'re taking a measured approach';

    // Infer urgency from next steps timeline
    const hasUrgentSteps = nextSteps?.some(step =>
      step.timeline?.includes('week') || step.timeline?.includes('ASAP')
    );

    return hasUrgentSteps ? 'timing is important' : 'you\'re planning strategically';
  }

  /**
   * Get follow-up timeline
   */
  getFollowUpTimeline(nextSteps) {
    if (!nextSteps || !Array.isArray(nextSteps) || nextSteps.length === 0) {
      return 'early next week';
    }

    const firstStep = nextSteps[0];
    if (firstStep.timeline?.includes('week')) return 'next week';
    if (firstStep.timeline?.includes('day')) return 'in a few days';
    if (firstStep.timeline?.includes('month')) return 'next month';

    return 'soon';
  }

  /**
   * Get next deliverable
   */
  getNextDeliverable(nextSteps) {
    if (!nextSteps || !Array.isArray(nextSteps) || nextSteps.length === 0) {
      return 'the information we discussed';
    }

    const firstStep = nextSteps[0];
    return firstStep.action || firstStep || 'the next steps we outlined';
  }

  /**
   * Generate personal note from key quotes
   */
  generatePersonalNote(keyQuotes) {
    if (!keyQuotes || !Array.isArray(keyQuotes) || keyQuotes.length === 0) {
      return 'Looking forward to continuing our conversation!';
    }

    const significantQuote = keyQuotes.find(q => q.socialMediaPotential === 'high');
    if (significantQuote) {
      return `I especially appreciated when you mentioned "${significantQuote.quote}" - it really highlights your commitment to innovation.`;
    }

    return 'Looking forward to continuing our conversation!';
  }

  /**
   * Determine email priority
   */
  determinePriority(salesData) {
    const urgency = salesData.sentiment?.urgency;
    const dealSize = salesData.salesMetrics?.dealSize;
    const salesStage = salesData.salesStage;

    if (urgency === 'high' || salesStage === 'closing') return 'high';
    if (urgency === 'low') return 'low';

    return 'normal';
  }

  /**
   * Calculate optimal send time
   */
  calculateOptimalSendTime() {
    const now = new Date();
    const hour = now.getHours();

    // If it's late evening or early morning, schedule for next business day at 9 AM
    if (hour < 8 || hour > 18) {
      const tomorrow = new Date(now);
      tomorrow.setDate(tomorrow.getDate() + 1);
      tomorrow.setHours(9, 0, 0, 0);
      return tomorrow.toISOString();
    }

    // Send within 30 minutes
    const sendTime = new Date(now.getTime() + 30 * 60 * 1000);
    return sendTime.toISOString();
  }

  /**
   * Calculate follow-up date
   */
  calculateFollowUpDate(nextSteps) {
    if (!nextSteps || !Array.isArray(nextSteps) || nextSteps.length === 0) {
      // Default to 3 business days
      const followUp = new Date();
      followUp.setDate(followUp.getDate() + 3);
      return followUp.toISOString().split('T')[0];
    }

    const firstStep = nextSteps[0];
    if (firstStep.timeline?.includes('week')) {
      const followUp = new Date();
      followUp.setDate(followUp.getDate() + 7);
      return followUp.toISOString().split('T')[0];
    }

    if (firstStep.timeline?.includes('day')) {
      const followUp = new Date();
      followUp.setDate(followUp.getDate() + 2);
      return followUp.toISOString().split('T')[0];
    }

    // Default to 5 business days
    const followUp = new Date();
    followUp.setDate(followUp.getDate() + 5);
    return followUp.toISOString().split('T')[0];
  }
}

// Export for use in n8n Function nodes
if (typeof module !== 'undefined' && module.exports) {
  module.exports = EmailRecapGenerator;
}

// For testing in n8n context
if (typeof items !== 'undefined') {
  const generator = new EmailRecapGenerator();
  const result = generator.generateRecap(items[0].json);
  return [{ json: result }];
}