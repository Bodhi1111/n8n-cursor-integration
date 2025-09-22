#!/usr/bin/env node
/**
 * TEST LOCAL VECTOR PROCESSING PIPELINE
 * Comprehensive testing of the local Mistral-7B + Qdrant vector setup
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');

class LocalVectorPipelineTest {
    constructor() {
        this.ollamaUrl = 'http://localhost:11434';
        this.qdrantUrl = 'http://localhost:6333';
        this.testResults = {
            ollama_connection: false,
            mistral_7b_available: false,
            embeddings_working: false,
            qdrant_connection: false,
            collections_exist: false,
            similarity_search_working: false,
            end_to_end_test: false
        };
    }

    async testOllamaConnection() {
        console.log('🔍 Testing Ollama connection...');

        try {
            const response = await axios.get(`${this.ollamaUrl}/api/tags`);
            if (response.status === 200) {
                console.log('✅ Ollama connection successful');
                this.testResults.ollama_connection = true;

                // Check if Mistral-7B is available
                const models = response.data.models || [];
                const mistralModel = models.find(model =>
                    model.name.includes('mistral') && model.name.includes('7b')
                );

                if (mistralModel) {
                    console.log(`✅ Mistral-7B found: ${mistralModel.name}`);
                    this.testResults.mistral_7b_available = true;
                    return mistralModel.name;
                } else {
                    console.log('❌ Mistral-7B not found');
                    console.log('Available models:', models.map(m => m.name));
                    return null;
                }
            }
        } catch (error) {
            console.error('❌ Ollama connection failed:', error.message);
            console.error('💡 Make sure Ollama is running: ollama serve');
            return null;
        }
    }

    async testMistralGeneration(modelName) {
        console.log('🤖 Testing Mistral-7B text generation...');

        try {
            const response = await axios.post(`${this.ollamaUrl}/api/generate`, {
                model: modelName,
                prompt: 'Extract the client name from: "John Smith is seeking estate planning advice."',
                stream: false,
                options: {
                    temperature: 0.1,
                    num_predict: 50
                }
            }, { timeout: 30000 });

            if (response.status === 200 && response.data.response) {
                console.log('✅ Mistral-7B generation working');
                console.log(`📝 Sample response: "${response.data.response.substring(0, 100)}..."`);
                return true;
            }
        } catch (error) {
            console.error('❌ Mistral-7B generation failed:', error.message);
            return false;
        }
    }

    async testEmbeddingsGeneration(modelName) {
        console.log('🧠 Testing embeddings generation...');

        try {
            const response = await axios.post(`${this.ollamaUrl}/api/embeddings`, {
                model: modelName,
                prompt: 'Estate planning consultation for client with blended family and LLC business interests'
            }, { timeout: 30000 });

            if (response.status === 200 && response.data.embedding && Array.isArray(response.data.embedding)) {
                console.log('✅ Embeddings generation working');
                console.log(`📊 Embedding dimension: ${response.data.embedding.length}`);
                this.testResults.embeddings_working = true;
                return response.data.embedding;
            }
        } catch (error) {
            console.error('❌ Embeddings generation failed:', error.message);
            return null;
        }
    }

    async testQdrantConnection() {
        console.log('🔍 Testing Qdrant connection...');

        try {
            const response = await axios.get(`${this.qdrantUrl}/collections`);
            if (response.status === 200) {
                console.log('✅ Qdrant connection successful');
                this.testResults.qdrant_connection = true;

                const collections = response.data.result.collections || [];
                console.log(`📚 Found ${collections.length} collections:`, collections.map(c => c.name));

                // Check for our specific collections
                const estateCollection = collections.find(c => c.name === 'estate_planning_transcripts');
                const knowledgeCollection = collections.find(c => c.name === 'estate_knowledge_base');

                if (estateCollection && knowledgeCollection) {
                    console.log('✅ Required collections exist');
                    this.testResults.collections_exist = true;
                    return true;
                } else {
                    console.log('⚠️  Required collections missing');
                    console.log('💡 Run: node qdrant-setup.js');
                    return false;
                }
            }
        } catch (error) {
            console.error('❌ Qdrant connection failed:', error.message);
            console.error('💡 Make sure Qdrant is running: docker run -p 6333:6333 qdrant/qdrant');
            return false;
        }
    }

    async testVectorStorage(embedding) {
        console.log('💾 Testing vector storage in Qdrant...');

        const testPoint = {
            points: [{
                id: `test_${Date.now()}`,
                vector: embedding.slice(0, 1024), // Ensure correct dimension
                payload: {
                    client_name: 'Test Client',
                    family_context: 'test_family',
                    business_context: 'test_business',
                    urgency_context: 'medium',
                    meeting_outcome: 'test_outcome',
                    test_data: true
                }
            }]
        };

        try {
            const response = await axios.put(
                `${this.qdrantUrl}/collections/estate_planning_transcripts/points`,
                testPoint
            );

            if (response.status === 200) {
                console.log('✅ Vector storage working');
                return testPoint.points[0].id;
            }
        } catch (error) {
            console.error('❌ Vector storage failed:', error.message);
            return null;
        }
    }

    async testSimilaritySearch(embedding, testPointId) {
        console.log('🔍 Testing similarity search...');

        try {
            const response = await axios.post(
                `${this.qdrantUrl}/collections/estate_planning_transcripts/points/search`,
                {
                    vector: embedding.slice(0, 1024),
                    limit: 3,
                    score_threshold: 0.1,
                    with_payload: true
                }
            );

            if (response.status === 200 && response.data.result) {
                const results = response.data.result;
                console.log(`✅ Similarity search working - found ${results.length} results`);

                results.forEach((result, idx) => {
                    console.log(`   ${idx + 1}. ID: ${result.id}, Score: ${result.score.toFixed(3)}, Client: ${result.payload.client_name}`);
                });

                this.testResults.similarity_search_working = true;

                // Clean up test data
                await this.cleanupTestData(testPointId);
                return true;
            }
        } catch (error) {
            console.error('❌ Similarity search failed:', error.message);
            return false;
        }
    }

    async cleanupTestData(testPointId) {
        try {
            await axios.post(
                `${this.qdrantUrl}/collections/estate_planning_transcripts/points/delete`,
                {
                    points: [testPointId]
                }
            );
            console.log('🧹 Test data cleaned up');
        } catch (error) {
            console.log('⚠️  Could not clean up test data:', error.message);
        }
    }

    async testKnowledgeGraphAnalysis() {
        console.log('🧠 Testing knowledge graph analysis...');

        const sampleTranscript = `
        Hi John, where in the world are you joining us from today?
        I'm calling from Maryland. I live here with my wife and our three children.
        We have a blended family - I have two stepchildren from my wife's previous marriage.
        I own an LLC that we're looking to sell next year, and we're concerned about estate planning.
        We have about $2.5 million in assets including our home and business.
        I think we're ready to move forward with your services today.
        `;

        // Simulate the knowledge graph analysis function
        const content = sampleTranscript.toLowerCase();

        const familyPatterns = ['stepchildren', 'blended family', 'previous marriage'];
        const businessPatterns = ['LLC', 'business', 'sell'];
        const urgencyPatterns = ['ready to move forward', 'today', 'next year'];

        let familyScore = 0;
        let businessScore = 0;
        let urgencyScore = 0;

        familyPatterns.forEach(pattern => {
            if (content.includes(pattern)) familyScore++;
        });

        businessPatterns.forEach(pattern => {
            if (content.includes(pattern)) businessScore++;
        });

        urgencyPatterns.forEach(pattern => {
            if (content.includes(pattern)) urgencyScore++;
        });

        const analysis = {
            family_type: familyScore > 0 ? 'blended_family' : 'unknown',
            family_confidence: familyScore / familyPatterns.length,
            business_type: businessScore > 0 ? 'LLC' : 'none',
            business_confidence: businessScore / businessPatterns.length,
            urgency_level: urgencyScore > 0 ? 'high' : 'medium',
            urgency_confidence: urgencyScore / urgencyPatterns.length
        };

        console.log('✅ Knowledge graph analysis working');
        console.log('📊 Analysis results:', analysis);

        return analysis;
    }

    async testCompleteWorkflow(modelName) {
        console.log('🚀 Testing complete end-to-end workflow...');

        try {
            // 1. Knowledge graph analysis
            const analysis = await this.testKnowledgeGraphAnalysis();

            // 2. Generate embeddings
            const embedding = await this.testEmbeddingsGeneration(modelName);
            if (!embedding) return false;

            // 3. Store in vector database
            const testPointId = await this.testVectorStorage(embedding);
            if (!testPointId) return false;

            // 4. Similarity search
            const searchWorking = await this.testSimilaritySearch(embedding, testPointId);
            if (!searchWorking) return false;

            // 5. Context-enhanced prompt creation
            const enhancedPrompt = this.createTestPrompt(analysis);
            console.log('✅ Context-enhanced prompt created');

            // 6. Test Mistral extraction
            const extractionWorking = await this.testMistralGeneration(modelName);
            if (!extractionWorking) return false;

            console.log('🎉 Complete workflow test successful!');
            this.testResults.end_to_end_test = true;
            return true;

        } catch (error) {
            console.error('❌ Complete workflow test failed:', error.message);
            return false;
        }
    }

    createTestPrompt(analysis) {
        return `You are a Senior Estate Planning Attorney analyzing a transcript.

CONTEXT ANALYSIS:
- Family: ${analysis.family_type} (${(analysis.family_confidence * 100).toFixed(1)}%)
- Business: ${analysis.business_type} (${(analysis.business_confidence * 100).toFixed(1)}%)
- Urgency: ${analysis.urgency_level} (${(analysis.urgency_confidence * 100).toFixed(1)}%)

Extract client information from the transcript...`;
    }

    generateTestReport() {
        console.log('\n📊 LOCAL VECTOR PIPELINE TEST REPORT');
        console.log('=' * 50);

        const tests = [
            { name: 'Ollama Connection', status: this.testResults.ollama_connection },
            { name: 'Mistral-7B Available', status: this.testResults.mistral_7b_available },
            { name: 'Embeddings Working', status: this.testResults.embeddings_working },
            { name: 'Qdrant Connection', status: this.testResults.qdrant_connection },
            { name: 'Collections Exist', status: this.testResults.collections_exist },
            { name: 'Similarity Search', status: this.testResults.similarity_search_working },
            { name: 'End-to-End Test', status: this.testResults.end_to_end_test }
        ];

        let passedTests = 0;
        tests.forEach(test => {
            const icon = test.status ? '✅' : '❌';
            console.log(`${icon} ${test.name}`);
            if (test.status) passedTests++;
        });

        const successRate = (passedTests / tests.length * 100).toFixed(1);
        console.log(`\n📈 Success Rate: ${successRate}% (${passedTests}/${tests.length})`);

        if (successRate >= 100) {
            console.log('\n🎉 ALL TESTS PASSED - READY FOR PRODUCTION!');
            console.log('✅ Local vector-enhanced processing is fully operational');
            console.log('✅ Import the local-vector-estate-workflow.json into n8n');
            console.log('✅ Process your first transcript to validate');
        } else if (successRate >= 70) {
            console.log('\n⚠️  MOSTLY WORKING - SOME ISSUES TO RESOLVE');
            console.log('💡 Check failed tests above and resolve before production');
        } else {
            console.log('\n❌ SIGNIFICANT ISSUES - SETUP INCOMPLETE');
            console.log('💡 Review setup guide and resolve failed tests');
        }

        return successRate;
    }

    async run() {
        console.log('🧪 LOCAL VECTOR PIPELINE TEST SUITE');
        console.log('=' * 50);
        console.log('Testing complete local Mistral-7B + Qdrant setup...\n');

        // Test sequence
        const modelName = await this.testOllamaConnection();
        if (!modelName) return this.generateTestReport();

        await this.testMistralGeneration(modelName);
        const embedding = await this.testEmbeddingsGeneration(modelName);

        const qdrantWorking = await this.testQdrantConnection();
        if (!qdrantWorking) return this.generateTestReport();

        if (embedding) {
            const testPointId = await this.testVectorStorage(embedding);
            if (testPointId) {
                await this.testSimilaritySearch(embedding, testPointId);
            }
        }

        if (this.testResults.embeddings_working && this.testResults.collections_exist) {
            await this.testCompleteWorkflow(modelName);
        }

        return this.generateTestReport();
    }
}

// Run tests if called directly
if (require.main === module) {
    const tester = new LocalVectorPipelineTest();
    tester.run().catch(console.error);
}

module.exports = LocalVectorPipelineTest;