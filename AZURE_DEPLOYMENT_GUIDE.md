# Azure App Service Deployment Guide
## Incident Insight Hub

This guide will help you deploy the Incident Insight Hub Streamlit application to Azure App Service.

## Prerequisites

1. **Azure Account**: Active Azure subscription
2. **Azure CLI**: Installed and configured
3. **Git**: For code deployment
4. **Python 3.8+**: Application requirement

## Deployment Files Created

The following files have been created for Azure deployment:

- `startup.py` - Python startup script for Azure App Service
- `startup.sh` - Bash startup script (alternative)
- `web.config` - IIS configuration for Azure App Service
- `.deployment` - Deployment configuration
- `deploy.cmd` - Custom deployment script
- `requirements.txt` - Python dependencies (already existed)

## Deployment Methods

### Method 1: Azure CLI Deployment (Recommended)

1. **Login to Azure**:
   ```bash
   az login
   ```

2. **Create Resource Group**:
   ```bash
   az group create --name incident-insight-rg --location "East US"
   ```

3. **Create App Service Plan**:
   ```bash
   az appservice plan create --name incident-insight-plan --resource-group incident-insight-rg --sku B1 --is-linux
   ```

4. **Create Web App**:
   ```bash
   az webapp create --resource-group incident-insight-rg --plan incident-insight-plan --name incident-insight-hub --runtime "PYTHON|3.11"
   ```

5. **Configure Deployment Source**:
   ```bash
   # If using local Git
   az webapp deployment source config-local-git --name incident-insight-hub --resource-group incident-insight-rg
   
   # Or if using GitHub
   az webapp deployment source config --name incident-insight-hub --resource-group incident-insight-rg --repo-url <your-github-repo-url> --branch main --manual-integration
   ```

6. **Set Application Settings**:
   ```bash
   az webapp config appsettings set --resource-group incident-insight-rg --name incident-insight-hub --settings WEBSITES_PORT=8000 SCM_DO_BUILD_DURING_DEPLOYMENT=true
   ```

7. **Deploy Code**:
   ```bash
   # If using local Git
   git add .
   git commit -m "Initial deployment"
   git remote add azure <azure-git-url>
   git push azure main
   ```

### Method 2: Azure Portal Deployment

1. **Create App Service**:
   - Go to [Azure Portal](https://portal.azure.com)
   - Create new App Service
   - Choose Python 3.11 runtime
   - Select appropriate pricing tier (B1 or higher recommended)

2. **Configure Deployment**:
   - Go to Deployment Center
   - Choose GitHub, Azure DevOps, or Local Git
   - Configure source control settings

3. **Set Application Settings**:
   - Go to Configuration → Application Settings
   - Add: `WEBSITES_PORT = 8000`
   - Add: `SCM_DO_BUILD_DURING_DEPLOYMENT = true`

4. **Deploy Code**:
   - Push code to configured repository
   - Azure will automatically build and deploy

### Method 3: ZIP Deployment

1. **Create ZIP file**:
   ```bash
   # Exclude unnecessary files
   zip -r incident-insight-hub.zip . -x "*.git*" "*__pycache__*" "*.pyc" "logs/*" ".vscode/*"
   ```

2. **Deploy via Azure CLI**:
   ```bash
   az webapp deployment source config-zip --resource-group incident-insight-rg --name incident-insight-hub --src incident-insight-hub.zip
   ```

## Configuration Settings

### Required App Settings

Set these in Azure Portal → App Service → Configuration:

- `WEBSITES_PORT`: `8000`
- `SCM_DO_BUILD_DURING_DEPLOYMENT`: `true`
- `PYTHONPATH`: `/home/site/wwwroot`

### Optional Settings

- `STREAMLIT_SERVER_HEADLESS`: `true`
- `STREAMLIT_BROWSER_GATHER_USAGE_STATS`: `false`

## Troubleshooting

### Common Issues

1. **Port Configuration**:
   - Ensure `WEBSITES_PORT` is set to `8000`
   - Streamlit will bind to the port specified by Azure

2. **Build Failures**:
   - Check deployment logs in Azure Portal → App Service → Deployment Center
   - Verify `requirements.txt` is in root directory
   - Ensure Python version compatibility

3. **Application Not Starting**:
   - Check application logs: Azure Portal → App Service → Log stream
   - Verify `startup.py` is executable
   - Check `web.config` configuration

4. **Memory Issues**:
   - Consider upgrading to a higher App Service Plan (S1 or higher)
   - Monitor memory usage in Azure Portal

### Viewing Logs

```bash
# Stream logs via Azure CLI
az webapp log tail --name incident-insight-hub --resource-group incident-insight-rg

# Download logs
az webapp log download --name incident-insight-hub --resource-group incident-insight-rg
```

## Post-Deployment

1. **Test Application**:
   - Navigate to `https://incident-insight-hub.azurewebsites.net`
   - Upload sample data to test functionality

2. **Monitor Performance**:
   - Use Azure Application Insights for monitoring
   - Set up alerts for availability and performance

3. **Scale as Needed**:
   - Monitor resource usage
   - Scale up/out based on demand

## Security Considerations

1. **HTTPS**: Enabled by default on Azure App Service
2. **Authentication**: Consider adding Azure AD authentication if needed
3. **Network Security**: Configure access restrictions if required
4. **Data Privacy**: Ensure uploaded data is handled according to compliance requirements

## Cost Optimization

1. **Pricing Tier**: Start with B1, upgrade as needed
2. **Auto-scaling**: Configure based on usage patterns
3. **Resource Monitoring**: Use Azure Cost Management

## Support

For issues with Azure deployment:
- Check Azure documentation
- Use Azure support channels
- Review application logs for specific errors

---

**Note**: This application processes incident data and provides analytics. Ensure you have appropriate permissions and follow your organization's data handling policies when deploying to cloud services. 