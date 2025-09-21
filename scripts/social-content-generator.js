/**
 * Social Media Content Generator
 * Creates viral, attention-getting social media content from sales meeting insights
 */

class SocialContentGenerator {
  constructor() {
    this.platformSpecs = {
      linkedin: { maxLength: 3000, professionalTone: true, hashtagLimit: 5 },
      twitter: { maxLength: 280, casualTone: true, hashtagLimit: 3 },
      instagram: { maxLength: 2200, visualFocus: true, hashtagLimit: 10 },
      facebook: { maxLength: 2000, storytelling: true, hashtagLimit: 5 },
      tiktok: { maxLength: 150, trendy: true, hashtagLimit: 5 }
    };

    this.viralElements = {
      hooks: [
        'Just had the most incredible conversation...',
        '🤯 Mind-blown by what I learned today...',
        'Plot twist:',
        'This changed everything I thought I knew about...',
        'Real talk:',
        'Hot take:',
        'Unpopular opinion:',
        'Here\'s what nobody talks about...',
        'The truth about...',
        'This will change how you think about...'
      ],
      emotions: [
        'excited', 'inspired', 'amazed', 'grateful', 'motivated',
        'surprised', 'curious', 'passionate', 'determined'
      ],
      powerWords: [
        'revolutionary', 'game-changing', 'breakthrough', 'innovative',
        'disruptive', 'transformative', 'cutting-edge', 'next-level'
      ]
    };
  }

  /**
   * Generate social media content for all platforms
   * @param {Object} salesData - Extracted sales data
   * @returns {Object} Platform-specific content
   */
  generateAllContent(salesData) {
    try {
      const insights = this.extractContentInsights(salesData);
      const contentStrategy = this.developContentStrategy(insights);

      const socialContent = {
        linkedin: this.generateLinkedInContent(insights, contentStrategy),
        twitter: this.generateTwitterContent(insights, contentStrategy),
        instagram: this.generateInstagramContent(insights, contentStrategy),
        facebook: this.generateFacebookContent(insights, contentStrategy),
        tiktok: this.generateTikTokContent(insights, contentStrategy)
      };

      return {
        ...salesData,
        socialContent,
        contentInsights: insights,
        contentStrategy,
        generatedAt: new Date().toISOString(),
        platforms: Object.keys(socialContent),
        totalPosts: Object.keys(socialContent).length
      };
    } catch (error) {
      console.error('Error generating social content:', error);
      return {
        ...salesData,
        socialContentError: error.message,
        contentStatus: 'failed'
      };
    }
  }

  /**
   * Extract content-worthy insights from sales data
   */
  extractContentInsights(salesData) {
    const insights = {
      companyHighlight: this.extractCompanyHighlight(salesData),
      industryInsight: this.extractIndustryInsight(salesData),
      problemStatement: this.extractProblemStatement(salesData),
      inspiringQuotes: this.extractInspiringQuotes(salesData.keyQuotes),
      lessonLearned: this.extractLessonLearned(salesData),
      marketTrend: this.extractMarketTrend(salesData),
      humanStory: this.extractHumanStory(salesData),
      contrarian: this.extractContrarianTake(salesData),
      behindScenes: this.extractBehindScenes(salesData),
      gratitude: this.extractGratitudeMoment(salesData)
    };

    return insights;
  }

  /**
   * Develop content strategy based on insights
   */
  developContentStrategy(insights) {
    const strategies = [];

    if (insights.inspiringQuotes.length > 0) {
      strategies.push({
        type: 'quote_highlight',
        hook: 'Quote that stopped me in my tracks:',
        cta: 'What do you think about this perspective?'
      });
    }

    if (insights.industryInsight) {
      strategies.push({
        type: 'industry_insight',
        hook: 'Here\'s what I\'m seeing in the industry:',
        cta: 'Anyone else noticing this trend?'
      });
    }

    if (insights.problemStatement) {
      strategies.push({
        type: 'problem_solution',
        hook: 'The biggest challenge I\'m hearing about:',
        cta: 'How are you solving this in your organization?'
      });
    }

    if (insights.humanStory) {
      strategies.push({
        type: 'human_story',
        hook: 'Sometimes the best meetings remind you why you love what you do:',
        cta: 'What energizes you most about your work?'
      });
    }

    return strategies;
  }

  /**
   * Generate LinkedIn content (professional, thought leadership)
   */
  generateLinkedInContent(insights, strategies) {
    const posts = [];

    // Quote-driven post
    if (insights.inspiringQuotes.length > 0) {
      const quote = insights.inspiringQuotes[0];
      posts.push({
        type: 'quote_post',
        content: `💡 Quote from today's meeting that really resonated:

"${quote.text}"

${insights.companyHighlight ? `This came up during my conversation with the incredible team at ${insights.companyHighlight.name}.` : ''}

${insights.lessonLearned ? `Key takeaway: ${insights.lessonLearned}` : ''}

${insights.industryInsight ? `\nWhat I'm seeing across ${insights.industryInsight.industry}: ${insights.industryInsight.trend}` : ''}

What's your take on this? 👇

#Leadership #${insights.industryInsight?.industry || 'Business'} #Sales #Innovation #Growth`,
        engagement: 'high',
        tone: 'professional_insight'
      });
    }

    // Industry insight post
    if (insights.industryInsight) {
      posts.push({
        type: 'industry_trend',
        content: `🔍 Trend I'm seeing in ${insights.industryInsight.industry}:

${insights.problemStatement ? `The challenge: ${insights.problemStatement}` : ''}

${insights.industryInsight.trend}

${insights.lessonLearned ? `Why this matters: ${insights.lessonLearned}` : ''}

${insights.companyHighlight ? `Shoutout to companies like ${insights.companyHighlight.name} who are thinking differently about this.` : ''}

What trends are you seeing in your space?

#${insights.industryInsight.industry} #MarketTrends #Innovation #BusinessStrategy`,
        engagement: 'medium',
        tone: 'thought_leadership'
      });
    }

    // Gratitude/behind-the-scenes post
    if (insights.gratitude && insights.humanStory) {
      posts.push({
        type: 'gratitude_story',
        content: `🙏 ${insights.gratitude}

${insights.humanStory}

${insights.companyHighlight ? `Working with teams like ${insights.companyHighlight.name} reminds me why I'm passionate about what we do.` : ''}

${insights.lessonLearned ? `Today's lesson: ${insights.lessonLearned}` : ''}

What moments in your work fill you with gratitude?

#Grateful #BusinessRelationships #Purpose #Growth`,
        engagement: 'high',
        tone: 'authentic_personal'
      });
    }

    return posts;
  }

  /**
   * Generate Twitter content (concise, engaging)
   */
  generateTwitterContent(insights, strategies) {
    const tweets = [];

    // Quote tweet
    if (insights.inspiringQuotes.length > 0) {
      const quote = insights.inspiringQuotes[0];
      tweets.push({
        type: 'quote_tweet',
        content: `💭 "${quote.text}"

${insights.companyHighlight ? `- Conversation with ${insights.companyHighlight.name}` : ''}

#SalesLife #${insights.industryInsight?.industry || 'Business'}`,
        engagement: 'high',
        tone: 'inspirational'
      });
    }

    // Hot take / contrarian view
    if (insights.contrarian) {
      tweets.push({
        type: 'hot_take',
        content: `🔥 Hot take: ${insights.contrarian}

${insights.lessonLearned ? `Why: ${insights.lessonLearned}` : ''}

Agree or disagree? 👇`,
        engagement: 'high',
        tone: 'controversial'
      });
    }

    // Quick industry insight
    if (insights.industryInsight && insights.problemStatement) {
      tweets.push({
        type: 'industry_insight',
        content: `📈 ${insights.industryInsight.industry} reality check:

${insights.problemStatement}

${insights.marketTrend ? `The opportunity: ${insights.marketTrend}` : ''}

#${insights.industryInsight.industry} #MarketTrends`,
        engagement: 'medium',
        tone: 'informative'
      });
    }

    return tweets;
  }

  /**
   * Generate Instagram content (visual storytelling)
   */
  generateInstagramContent(insights, strategies) {
    const posts = [];

    // Story-style post
    if (insights.humanStory && insights.behindScenes) {
      posts.push({
        type: 'story_post',
        content: `Behind the scenes: ${insights.behindScenes} 📈

${insights.humanStory}

${insights.companyHighlight ? `Inspired by the vision at ${insights.companyHighlight.name}` : ''}

${insights.lessonLearned ? `Key insight: ${insights.lessonLearned}` : ''}

What drives you in your work? Let me know in the comments! 👇

#entrepreneurlife #businessmeeting #inspiration #growth #sales #meetingday #hustle #businessstory #networking #success`,
        engagement: 'high',
        tone: 'authentic_story',
        visualSuggestion: 'Meeting setup, office view, or quote graphic'
      });
    }

    // Quote graphic post
    if (insights.inspiringQuotes.length > 0) {
      const quote = insights.inspiringQuotes[0];
      posts.push({
        type: 'quote_graphic',
        content: `Words that hit different today 💯

"${quote.text}"

${insights.companyHighlight ? `From an incredible conversation with ${insights.companyHighlight.name}` : ''}

Sometimes the best meetings remind you why you do what you do ✨

${insights.lessonLearned ? `Takeaway: ${insights.lessonLearned}` : ''}

#motivation #businessquotes #entrepreneurship #sales #inspiration #growth #meetinginsights #businesslife #success #mindset`,
        engagement: 'high',
        tone: 'motivational',
        visualSuggestion: 'Quote graphic with professional background'
      });
    }

    return posts;
  }

  /**
   * Generate Facebook content (storytelling, community)
   */
  generateFacebookContent(insights, strategies) {
    const posts = [];

    // Full story post
    if (insights.humanStory && insights.companyHighlight) {
      posts.push({
        type: 'story_post',
        content: `${insights.gratitude || 'Had an amazing meeting today'} 🚀

${insights.humanStory}

${insights.companyHighlight ? `Working with the team at ${insights.companyHighlight.name} has been incredible.` : ''} ${insights.problemStatement ? `They're tackling ${insights.problemStatement}, and their approach is refreshing.` : ''}

${insights.inspiringQuotes.length > 0 ? `One thing that really stuck with me: "${insights.inspiringQuotes[0].text}"` : ''}

${insights.lessonLearned ? `Today's reminder: ${insights.lessonLearned}` : ''}

${insights.industryInsight ? `It's exciting to see how ${insights.industryInsight.industry} is evolving. ${insights.industryInsight.trend}` : ''}

What's energizing you in your work lately? I'd love to hear about it in the comments!

#business #entrepreneurship #sales #growth #inspiration`,
        engagement: 'high',
        tone: 'community_story'
      });
    }

    return posts;
  }

  /**
   * Generate TikTok content (short, trendy, engaging)
   */
  generateTikTokContent(insights, strategies) {
    const videos = [];

    // Quick insight/hot take
    if (insights.contrarian || insights.lessonLearned) {
      videos.push({
        type: 'quick_insight',
        content: `POV: You just learned something that changes everything 🤯

${insights.contrarian || insights.lessonLearned}

#businesstok #entrepreneur #sales #mindset`,
        engagement: 'high',
        tone: 'trendy',
        format: 'talking_head',
        duration: '15-30 seconds'
      });
    }

    // Behind the scenes
    if (insights.behindScenes) {
      videos.push({
        type: 'behind_scenes',
        content: `Day in the life: Sales meeting edition 📈

${insights.behindScenes}

#dayinthelife #sales #business #meetingday`,
        engagement: 'medium',
        tone: 'authentic',
        format: 'day_in_life',
        duration: '30-60 seconds'
      });
    }

    return videos;
  }

  /**
   * Extract company highlight for content
   */
  extractCompanyHighlight(salesData) {
    const companyName = salesData.companyName;
    const companyDetails = salesData.companyDetails;

    if (!companyName || companyName === 'Unknown') return null;

    return {
      name: companyName,
      industry: companyDetails?.industry,
      size: companyDetails?.size,
      highlight: this.generateCompanyHighlight(companyDetails)
    };
  }

  /**
   * Generate company highlight text
   */
  generateCompanyHighlight(companyDetails) {
    if (!companyDetails) return null;

    const highlights = [];

    if (companyDetails.industry) {
      highlights.push(`innovative ${companyDetails.industry} company`);
    }

    if (companyDetails.size === 'startup') {
      highlights.push('fast-growing startup');
    } else if (companyDetails.size === 'enterprise') {
      highlights.push('industry leader');
    }

    return highlights.length > 0 ? highlights[0] : null;
  }

  /**
   * Extract industry insight
   */
  extractIndustryInsight(salesData) {
    const industry = salesData.companyDetails?.industry;
    const painPoints = salesData.painPoints || [];
    const trends = salesData.competitiveIntel?.trends || [];

    if (!industry) return null;

    const commonPainPoint = painPoints.find(p => p.impact === 'high');
    const industryTrend = trends[0];

    return {
      industry,
      trend: industryTrend || this.inferTrend(painPoints),
      impact: commonPainPoint?.impact
    };
  }

  /**
   * Infer trend from pain points
   */
  inferTrend(painPoints) {
    if (!painPoints || painPoints.length === 0) return null;

    const digitalTerms = ['digital', 'automation', 'AI', 'cloud', 'remote'];
    const scalabilityTerms = ['scale', 'growth', 'efficiency', 'productivity'];

    const painText = painPoints.map(p => p.description || p).join(' ').toLowerCase();

    if (digitalTerms.some(term => painText.includes(term))) {
      return 'Companies are accelerating digital transformation initiatives';
    }

    if (scalabilityTerms.some(term => painText.includes(term))) {
      return 'Scalability and efficiency are top priorities';
    }

    return 'Organizations are rethinking their operational strategies';
  }

  /**
   * Extract problem statement
   */
  extractProblemStatement(salesData) {
    const painPoints = salesData.painPoints || [];

    if (painPoints.length === 0) return null;

    const highImpactPain = painPoints.find(p => p.urgency === 'high' || p.impact === 'high');
    const primaryPain = highImpactPain || painPoints[0];

    return primaryPain.description || primaryPain;
  }

  /**
   * Extract inspiring quotes
   */
  extractInspiringQuotes(keyQuotes) {
    if (!keyQuotes || !Array.isArray(keyQuotes)) return [];

    return keyQuotes
      .filter(q => q.socialMediaPotential === 'high' || q.socialMediaPotential === 'medium')
      .map(q => ({
        text: q.quote,
        speaker: q.speaker,
        context: q.context,
        potential: q.socialMediaPotential
      }))
      .slice(0, 3); // Top 3 quotes
  }

  /**
   * Extract lesson learned
   */
  extractLessonLearned(salesData) {
    const sentiment = salesData.sentiment;
    const insights = salesData.competitiveIntel?.insights || [];

    if (sentiment?.overall === 'positive' && sentiment.buyingSignals?.length > 0) {
      return 'Great opportunities come from really understanding customer needs';
    }

    if (insights.length > 0) {
      return insights[0];
    }

    return 'Every conversation teaches you something new about the market';
  }

  /**
   * Extract market trend
   */
  extractMarketTrend(salesData) {
    const competitive = salesData.competitiveIntel;
    const requirements = salesData.requirements || [];

    if (competitive?.trends?.length > 0) {
      return competitive.trends[0];
    }

    const techRequirements = requirements.filter(r =>
      (r.requirement || r).toLowerCase().includes('integration') ||
      (r.requirement || r).toLowerCase().includes('api') ||
      (r.requirement || r).toLowerCase().includes('automation')
    );

    if (techRequirements.length > 0) {
      return 'Integration and automation capabilities are becoming table stakes';
    }

    return null;
  }

  /**
   * Extract human story
   */
  extractHumanStory(salesData) {
    const sentiment = salesData.sentiment;
    const companyName = salesData.companyName;

    if (sentiment?.overall === 'positive' && sentiment.engagement === 'high') {
      return `Just wrapped up an energizing conversation that reminded me why I love what I do.`;
    }

    if (companyName && companyName !== 'Unknown') {
      return `Always inspired when I meet teams who are passionate about solving real problems.`;
    }

    return `Had one of those meetings that fills you with excitement about the future.`;
  }

  /**
   * Extract contrarian take
   */
  extractContrarianTake(salesData) {
    const competitive = salesData.competitiveIntel;
    const painPoints = salesData.painPoints || [];

    // Look for unique perspectives in the competitive intel
    if (competitive?.differentiationOpportunities?.length > 0) {
      return `Most people think ${competitive.differentiationOpportunities[0]}, but here's what I'm seeing...`;
    }

    // Create contrarian view from pain points
    if (painPoints.length > 0) {
      const commonPain = painPoints[0].description || painPoints[0];
      return `Everyone's talking about solutions, but the real problem is ${commonPain}`;
    }

    return null;
  }

  /**
   * Extract behind the scenes content
   */
  extractBehindScenes(salesData) {
    const meetingType = salesData.meetingType;
    const duration = salesData.estimatedDuration;

    const scenarios = [
      `Just finished a ${duration || '60'}-minute ${meetingType || 'strategy'} session`,
      `Between meetings, reflecting on today's conversations`,
      `Coffee's gone cold, but the conversation was fire 🔥`,
      `Sometimes the best insights come from the most unexpected questions`
    ];

    return scenarios[Math.floor(Math.random() * scenarios.length)];
  }

  /**
   * Extract gratitude moment
   */
  extractGratitudeMoment(salesData) {
    const sentiment = salesData.sentiment;

    if (sentiment?.overall === 'positive') {
      return 'Grateful for conversations that challenge my thinking and expand my perspective.';
    }

    return 'Thankful for the opportunity to learn from incredible leaders every day.';
  }
}

// Export for use in n8n Function nodes
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SocialContentGenerator;
}

// For testing in n8n context
if (typeof items !== 'undefined') {
  const generator = new SocialContentGenerator();
  const result = generator.generateAllContent(items[0].json);
  return [{ json: result }];
}