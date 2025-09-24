# 🌿 Branch Strategy & Testing Isolation

## Overview

This document outlines the branching strategy for safe testing and development of pipeline workflows.

## 🌳 Branch Structure

```
main (production)
├── develop (development integration)
├── feature/* (feature development)
├── hotfix/* (emergency fixes)
└── test/* (isolated testing branches)
```

## 🧪 Testing Branch Strategy

### 1. Create Isolated Testing Branch

```bash
# Create testing branch from main
git checkout main
git pull origin main
git checkout -b test/pipeline-validation

# Or create from current branch for specific feature testing
git checkout -b test/feature-xyz-validation
```

### 2. Safe Testing Environment

```bash
# Test workflows in isolation
npm run test:all

# Test Docker services without affecting production
docker-compose -f docker-compose.test.yml up -d

# Test specific pipeline components
npm run test:pipeline
npm run test:workflows
npm run test:integration
```

### 3. Validation Checklist

Before merging any pipeline changes:

- [ ] All unit tests pass (`npm test`)
- [ ] Pipeline resilience tests pass (`npm run test:pipeline`)
- [ ] Workflow validation passes (`npm run test:workflows`)
- [ ] Docker services start correctly
- [ ] n8n workflows can be imported
- [ ] Baserow integration works
- [ ] Security scans pass
- [ ] Performance benchmarks meet criteria

## 🔄 Workflow Testing Process

### Step 1: Validate Workflow Structure

```bash
# Run workflow validation
npm run test:workflows

# Expected output:
# ✅ Workflows Loaded
# ✅ Estate Planning Valid
# ✅ Batch Processor Valid
# ✅ Sales Processor Valid (if applicable)
```

### Step 2: Test Pipeline Resilience

```bash
# Run resilience tests
npm run test:pipeline

# Expected output:
# ✅ Error Handling
# ✅ Retry Mechanisms
# ✅ Fallback Strategies
# ✅ Circuit Breaker
# ✅ Graceful Degradation
# ✅ Recovery Procedures
```

### Step 3: Integration Testing

```bash
# Start services for integration testing
docker-compose up -d

# Wait for services to be ready
sleep 60

# Run integration tests
npm run test:integration

# Expected output:
# ✅ Docker Compose Up
# ✅ n8n Accessible
# ✅ Baserow Accessible
# ✅ Services Communicating
```

### Step 4: End-to-End Validation

```bash
# Test complete workflow execution
npm run test:all

# Manual validation steps:
# 1. Open n8n at http://localhost:5679
# 2. Import workflow JSON files
# 3. Test manual trigger execution
# 4. Verify Baserow data creation
# 5. Check log outputs for errors
```

## 🚀 CI/CD Pipeline Testing

### GitHub Actions Workflow Validation

The CI/CD pipeline automatically tests:

1. **Code Quality** (`lint` job)
   - ESLint checks
   - Prettier formatting
   - Markdown linting

2. **Unit Tests** (`test` job)
   - Function node scripts
   - Pipeline resilience
   - Workflow validation

3. **Integration Tests** (`integration-test` job)
   - Docker service health
   - Service communication
   - API accessibility

4. **Security Scans** (`security` job)
   - Dependency vulnerabilities
   - Secret detection
   - Code analysis

### Testing Different Scenarios

```yaml
# Matrix testing for different configurations
strategy:
  matrix:
    node-version: [18, 20]
    test-scenario: [basic, full-stack, minimal]
    include:
      - test-scenario: basic
        services: []
      - test-scenario: full-stack
        services: [ollama, qdrant]
      - test-scenario: minimal
        services: []
```

## 🔧 Local Development Testing

### Development Environment Setup

```bash
# Clone repository
git clone <repository-url>
cd n8n-cursor-integration

# Install dependencies
npm install

# Create local testing branch
git checkout -b test/local-development

# Start minimal services for testing
docker-compose up -d n8n baserow

# Run tests
npm run test:all
```

### Testing Workflow Modifications

```bash
# 1. Modify workflow JSON files in /workflows
# 2. Validate structure
npm run test:workflows

# 3. Test in n8n interface
# - Import modified workflow
# - Test manual execution
# - Check for errors

# 4. Validate with test data
# - Use sample-transcript.txt
# - Verify processing pipeline
# - Check output format

# 5. Run full test suite
npm run test:all
```

## 🛡️ Risk Mitigation Strategies

### 1. Blue-Green Testing

```bash
# Test new workflows alongside existing ones
cp workflows/estate-planning.json workflows/estate-planning-v2.json

# Modify v2 for testing
# Import both versions in n8n
# Compare results before switching
```

### 2. Rollback Procedures

```bash
# Always maintain working version
git tag stable-version-$(date +%Y%m%d)

# Test new version in isolation
git checkout -b test/new-version-validation

# If issues found, rollback
git checkout main
git reset --hard stable-version-latest
```

### 3. Canary Testing

```bash
# Process small batch with new workflow
# Monitor error rates and performance
# Gradually increase traffic to new version
```

## 📊 Testing Success Criteria

### Unit Tests
- ✅ 100% of function scripts execute without errors
- ✅ All resilience patterns work correctly
- ✅ Error handling covers edge cases

### Integration Tests
- ✅ All Docker services start and respond
- ✅ APIs are accessible and functional
- ✅ Services can communicate effectively

### End-to-End Tests
- ✅ Workflows can be imported and executed
- ✅ Data flows correctly through pipeline
- ✅ Output format matches expectations

### Performance Tests
- ✅ Processing time < 30 seconds per document
- ✅ Memory usage < 1GB per service
- ✅ Error rate < 1% under normal load

## 🔄 Continuous Testing

### Automated Testing Schedule

- **On every commit**: Unit tests + linting
- **On PR creation**: Full test suite
- **Daily**: Integration tests with Docker
- **Weekly**: Performance and load tests
- **Before release**: Complete validation suite

### Monitoring and Alerting

```bash
# Set up monitoring for:
# - Test execution failures
# - Performance degradation
# - Service availability
# - Error rates

# Alert channels:
# - GitHub Issues for test failures
# - Slack for critical issues
# - Email for weekly reports
```

## 📚 Testing Documentation

### Test Reports

Each test run generates comprehensive reports:

- **Unit Test Results**: Pass/fail status for each component
- **Integration Test Results**: Service health and connectivity
- **Performance Metrics**: Execution times and resource usage
- **Error Analysis**: Failed test details and recommendations

### Historical Testing Data

- Maintain test result history in `test-results/` directory
- Track performance trends over time
- Identify recurring issues and patterns
- Generate monthly testing summary reports

---

## 🎯 Quick Reference

### Essential Commands

```bash
# Full test suite
npm run test:all

# Individual test categories
npm run test:pipeline      # Resilience tests
npm run test:workflows     # Workflow validation
npm run test:integration   # Docker integration

# Development workflow
git checkout -b test/my-feature
npm run test:all
# Make changes
npm run test:all
git commit -m "test: validate my-feature"
```

### Testing Checklist

Before any deployment:

- [ ] Branch created for isolated testing
- [ ] All automated tests pass
- [ ] Manual workflow validation completed
- [ ] Performance benchmarks met
- [ ] Security scans clean
- [ ] Documentation updated
- [ ] Rollback plan prepared

---

**Last Updated:** December 2024  
**Version:** 1.0  
**Maintainer:** Development Team