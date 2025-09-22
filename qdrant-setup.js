#!/usr/bin/env node
/**
 * QDRANT VECTOR DATABASE SETUP
 * Creates collections and configures vector storage for estate planning transcripts
 */

const axios = require('axios');

class QdrantSetup {
    constructor() {
        this.qdrantUrl = 'http://localhost:6333';
        this.collections = {
            estate_planning_transcripts: {
                vectors: {
                    size: 1024, // Mistral embedding size
                    distance: 'Cosine'
                }
            },
            estate_knowledge_base: {
                vectors: {
                    size: 1024,
                    distance: 'Cosine'
                }
            }
        };
    }

    async createCollection(name, config) {
        try {
            console.log(`🔧 Creating collection: ${name}`);

            const response = await axios.put(`${this.qdrantUrl}/collections/${name}`, config);

            if (response.status === 200) {
                console.log(`✅ Collection '${name}' created successfully`);
                return true;
            }
        } catch (error) {
            if (error.response?.status === 400 && error.response.data.message?.includes('already exists')) {
                console.log(`ℹ️  Collection '${name}' already exists`);
                return true;
            } else {
                console.error(`❌ Failed to create collection '${name}':`, error.message);
                return false;
            }
        }
    }

    async createIndex(collectionName, fieldName, fieldType) {
        try {
            console.log(`🔍 Creating index on ${collectionName}.${fieldName}`);

            const response = await axios.put(
                `${this.qdrantUrl}/collections/${collectionName}/index`,
                {
                    field_name: fieldName,
                    field_schema: fieldType
                }
            );

            if (response.status === 200) {
                console.log(`✅ Index created on ${fieldName}`);
                return true;
            }
        } catch (error) {
            console.error(`❌ Failed to create index on ${fieldName}:`, error.message);
            return false;
        }
    }

    async seedKnowledgeBase() {
        console.log('🌱 Seeding knowledge base with estate planning concepts...');

        const knowledgeEntries = [
            {
                id: 'family-blended',
                vector: Array(1024).fill(0).map(() => Math.random() - 0.5), // Placeholder vector
                payload: {
                    concept: 'blended_family',
                    category: 'family_structure',
                    indicators: ['stepchildren', 'previous marriage', 'ex-wife', 'ex-husband', 'half-siblings'],
                    complexity_score: 8,
                    planning_considerations: ['Separate trusts', 'Step-child provisions', 'Spouse protection']
                }
            },
            {
                id: 'family-special-needs',
                vector: Array(1024).fill(0).map(() => Math.random() - 0.5),
                payload: {
                    concept: 'special_needs',
                    category: 'family_structure',
                    indicators: ['special needs', 'disabled child', 'disability benefits', 'SSI', 'medicaid'],
                    complexity_score: 9,
                    planning_considerations: ['Special needs trust', 'Medicaid planning', 'ABLE accounts']
                }
            },
            {
                id: 'business-llc',
                vector: Array(1024).fill(0).map(() => Math.random() - 0.5),
                payload: {
                    concept: 'LLC_interest',
                    category: 'business_structure',
                    indicators: ['LLC', 'limited liability', 'operating agreement', 'member interests'],
                    complexity_score: 6,
                    planning_considerations: ['Succession planning', 'Buy-sell agreements', 'Valuation discounts']
                }
            },
            {
                id: 'business-s-corp',
                vector: Array(1024).fill(0).map(() => Math.random() - 0.5),
                payload: {
                    concept: 'S_Corp_interest',
                    category: 'business_structure',
                    indicators: ['S corp', 'S corporation', 'shareholder agreement', 'pass-through'],
                    complexity_score: 7,
                    planning_considerations: ['Shareholder agreements', 'Stock redemption', 'ESOP considerations']
                }
            },
            {
                id: 'urgency-health',
                vector: Array(1024).fill(0).map(() => Math.random() - 0.5),
                payload: {
                    concept: 'health_urgency',
                    category: 'urgency_factors',
                    indicators: ['health issues', 'terminal illness', 'recent diagnosis', 'surgery'],
                    urgency_score: 9,
                    planning_considerations: ['Immediate execution', 'Power of attorney', 'Healthcare directives']
                }
            },
            {
                id: 'urgency-business-sale',
                vector: Array(1024).fill(0).map(() => Math.random() - 0.5),
                payload: {
                    concept: 'business_sale_urgency',
                    category: 'urgency_factors',
                    indicators: ['business sale', 'exit strategy', 'liquidity event', 'significant assets'],
                    urgency_score: 8,
                    planning_considerations: ['Installment sales', 'Tax deferral', 'Charitable strategies']
                }
            }
        ];

        try {
            const response = await axios.put(
                `${this.qdrantUrl}/collections/estate_knowledge_base/points`,
                {
                    points: knowledgeEntries
                }
            );

            if (response.status === 200) {
                console.log(`✅ Knowledge base seeded with ${knowledgeEntries.length} concepts`);
                return true;
            }
        } catch (error) {
            console.error('❌ Failed to seed knowledge base:', error.message);
            return false;
        }
    }

    async setupCollections() {
        console.log('🚀 Setting up Qdrant collections for estate planning...');
        console.log('=' * 60);

        let success = true;

        // Create collections
        for (const [name, config] of Object.entries(this.collections)) {
            const created = await this.createCollection(name, config);
            if (!created) success = false;
        }

        // Create indexes for better filtering
        const indexes = [
            { collection: 'estate_planning_transcripts', field: 'client_name', type: 'keyword' },
            { collection: 'estate_planning_transcripts', field: 'family_context', type: 'keyword' },
            { collection: 'estate_planning_transcripts', field: 'business_context', type: 'keyword' },
            { collection: 'estate_planning_transcripts', field: 'urgency_context', type: 'keyword' },
            { collection: 'estate_planning_transcripts', field: 'meeting_outcome', type: 'keyword' },
            { collection: 'estate_knowledge_base', field: 'concept', type: 'keyword' },
            { collection: 'estate_knowledge_base', field: 'category', type: 'keyword' }
        ];

        for (const index of indexes) {
            const created = await this.createIndex(index.collection, index.field, index.type);
            if (!created) success = false;
        }

        // Seed knowledge base
        const seeded = await this.seedKnowledgeBase();
        if (!seeded) success = false;

        return success;
    }

    async testConnection() {
        try {
            console.log('🔍 Testing Qdrant connection...');
            const response = await axios.get(`${this.qdrantUrl}/collections`);

            if (response.status === 200) {
                console.log('✅ Qdrant connection successful');
                console.log('📊 Available collections:', response.data.result.collections.map(c => c.name));
                return true;
            }
        } catch (error) {
            console.error('❌ Qdrant connection failed:', error.message);
            console.error('💡 Make sure Qdrant is running: docker run -p 6333:6333 qdrant/qdrant');
            return false;
        }
    }

    async run() {
        console.log('🎯 QDRANT VECTOR DATABASE SETUP');
        console.log('=' * 50);

        // Test connection first
        const connected = await this.testConnection();
        if (!connected) {
            process.exit(1);
        }

        // Setup collections
        const setupSuccess = await this.setupCollections();

        if (setupSuccess) {
            console.log('\n🎉 QDRANT SETUP COMPLETED SUCCESSFULLY!');
            console.log('✅ Collections created and indexed');
            console.log('✅ Knowledge base seeded');
            console.log('✅ Ready for vector-enhanced processing');

            console.log('\n📋 NEXT STEPS:');
            console.log('1. Import the enhanced-vector-estate-workflow.json into n8n');
            console.log('2. Configure Mistral API credentials in n8n');
            console.log('3. Update file paths for your transcript directory');
            console.log('4. Test with a single transcript file');

        } else {
            console.log('\n❌ QDRANT SETUP HAD ERRORS');
            console.log('⚠️  Check the error messages above and retry');
            process.exit(1);
        }
    }
}

// Run setup if called directly
if (require.main === module) {
    const setup = new QdrantSetup();
    setup.run().catch(console.error);
}

module.exports = QdrantSetup;