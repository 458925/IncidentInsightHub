# Testing Guide - Incident Insight Hub
## Comprehensive Testing via Azure DevOps

This guide explains how to test and validate your Incident Insight Hub application through Azure DevOps to ensure everything is perfect before and after deployment.

## Testing Architecture

The testing strategy includes multiple stages:

1. **Pre-Deployment Testing** (Build Stage)
   - Unit Tests
   - Import Validation
   - Syntax Validation
   - Dependency Checks

2. **Deployment** (Deploy Stage)
   - Azure App Service Deployment
   - Configuration Validation

3. **Post-Deployment Validation** (Validation Stage)
   - Health Checks
   - Security Validation
   - Performance Testing
   - Integration Testing

## Test Files Structure

```
tests/
├── test_app.py          # Unit tests for application components
├── test_health.py       # Health check and deployment validation
└── __init__.py          # Test package initialization
```

## Local Testing

### 1. Run Unit Tests Locally

```powershell
# Install test dependencies
pip install pytest requests

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_app.py -v

# Run with coverage (optional)
pip install pytest-cov
python -m pytest tests/ --cov=src --cov-report=html
```

### 2. Run Health Check Locally

```powershell
# Start the application first
python -m streamlit run app.py --server.port 8000

# In another terminal, run health check
python tests/test_health.py --url http://localhost:8000
```

### 3. Validate Application Components

```powershell
# Test imports
python -c "
import sys, os
sys.path.append('src')
from src.data_processor import DataProcessor
from src.analyzers import RecurringIssuesAnalyzer
print('✓ All imports successful')
"

# Test Streamlit syntax
python -m streamlit run app.py --help
```

## Azure DevOps Pipeline Testing

### Pipeline Stages Overview

#### Stage 1: Build and Test
- **Unit Tests**: Validates core functionality
- **Import Validation**: Ensures all modules can be imported
- **Syntax Validation**: Verifies Streamlit app syntax
- **Dependency Installation**: Installs and validates all dependencies

#### Stage 2: Deploy
- **Azure App Service Deployment**: Deploys to Linux Web App
- **Configuration Setup**: Sets required app settings and startup commands

#### Stage 3: Post-Deployment Validation
- **Health Check**: Comprehensive application health validation
- **Security Check**: Validates security configurations
- **Performance Test**: Basic performance and response time testing
- **Integration Test**: End-to-end functionality validation

### Pipeline Configuration

The `azure-pipelines.yml` includes:

```yaml
# Pre-deployment testing
- script: python -m pytest tests/ -v --tb=short
  displayName: Run Unit Tests

# Post-deployment validation
- script: python tests/test_health.py --url "https://$(appName).azurewebsites.net"
  displayName: Run Deployment Health Check
```

## Test Scenarios Covered

### 1. Unit Tests (`test_app.py`)

**DataProcessor Tests:**
- ✅ Column validation
- ✅ Data cleaning
- ✅ Error handling

**Analyzer Tests:**
- ✅ Recurring issues analysis
- ✅ SLA metrics calculation
- ✅ Team performance analysis
- ✅ Pattern identification

**Utility Tests:**
- ✅ Date parsing
- ✅ Chart display safety
- ✅ Error handling

### 2. Health Checks (`test_health.py`)

**Dependency Validation:**
- ✅ Streamlit availability
- ✅ Pandas availability
- ✅ Plotly availability

**Application Health:**
- ✅ HTTP connectivity
- ✅ Response time validation
- ✅ Application identification
- ✅ Startup timing

**Deployment Validation:**
- ✅ Azure App Service status
- ✅ Application logs review
- ✅ Endpoint accessibility

### 3. Security Validation

**Configuration Checks:**
- ✅ HTTPS enforcement
- ✅ TLS version validation
- ✅ Application settings verification

### 4. Performance Testing

**Response Time Tests:**
- ✅ Multiple request sampling
- ✅ Average response time calculation
- ✅ Performance threshold validation

### 5. Integration Testing

**End-to-End Validation:**
- ✅ Full application workflow
- ✅ Streamlit detection
- ✅ Content validation

## Monitoring Test Results

### In Azure DevOps Portal

1. **Pipeline Runs**: Navigate to Pipelines → Your Pipeline → Runs
2. **Test Results**: Click on a run → Tests tab
3. **Logs**: Click on a run → Logs → Expand stages/jobs
4. **Artifacts**: Check published test results and coverage reports

### Test Result Interpretation

**✅ GREEN (Success)**: All tests passed, deployment validated
**🟡 YELLOW (Warning)**: Tests passed with warnings (e.g., slow performance)
**❌ RED (Failure)**: Tests failed, deployment should be investigated

## Troubleshooting Common Issues

### 1. Unit Test Failures

```bash
# Check test logs in Azure DevOps
# Common issues:
- Missing dependencies in requirements.txt
- Import path issues
- Data format changes
```

### 2. Health Check Failures

```bash
# Application not responding
- Check App Service logs: az webapp log tail --name <app-name>
- Verify startup command configuration
- Check resource allocation (scale up if needed)
```

### 3. Performance Issues

```bash
# Slow response times
- Check App Service plan (consider scaling up)
- Review application logs for errors
- Monitor resource usage in Azure Portal
```

### 4. Security Validation Failures

```bash
# HTTPS/TLS issues
- Verify App Service SSL settings
- Check custom domain configuration
- Review security policies
```

## Manual Testing Checklist

After successful pipeline deployment, manually verify:

### Functional Testing
- [ ] Application loads successfully
- [ ] File upload functionality works
- [ ] All analysis modules function correctly
- [ ] Charts and visualizations display properly
- [ ] Sample data processing works

### UI/UX Testing
- [ ] Responsive design on different screen sizes
- [ ] Navigation between sections works
- [ ] Error messages are user-friendly
- [ ] Loading states are appropriate

### Data Testing
- [ ] Upload sample_data.xlsx and verify processing
- [ ] Test with malformed data files
- [ ] Verify data validation messages
- [ ] Check analysis accuracy

## Continuous Improvement

### Adding New Tests

1. **Unit Tests**: Add to `tests/test_app.py`
2. **Integration Tests**: Extend `test_health.py`
3. **Performance Tests**: Add to pipeline performance stage

### Test Data Management

- Keep test data files small and focused
- Use anonymized/synthetic data for testing
- Regularly update test scenarios

### Metrics and Monitoring

- Monitor test execution times
- Track test coverage percentage
- Review test failure patterns

## Emergency Procedures

### Rollback Process

If tests fail after deployment:

1. **Immediate**: Check application logs
2. **Quick Fix**: Restart App Service
3. **Rollback**: Deploy previous known-good version
4. **Investigation**: Analyze test failure logs

### Production Validation

For production deployments:

1. Run smoke tests immediately after deployment
2. Monitor application performance for 30 minutes
3. Validate with sample real data
4. Confirm with stakeholders

---

## Summary

This comprehensive testing approach ensures:

- ✅ **Code Quality**: Unit tests validate core functionality
- ✅ **Deployment Success**: Health checks confirm proper deployment
- ✅ **Security**: Security validation ensures safe operation
- ✅ **Performance**: Performance tests verify acceptable response times
- ✅ **Integration**: End-to-end tests confirm complete functionality

The automated pipeline provides confidence that your Incident Insight Hub deployment is robust, secure, and performing optimally.

**Next Steps:**
1. Push your code with the new test files to trigger the pipeline
2. Monitor the pipeline execution in Azure DevOps
3. Review test results and address any failures
4. Manually validate the deployed application
5. Set up monitoring and alerts for production 