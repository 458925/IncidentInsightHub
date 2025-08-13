# Azure DevOps Setup Guide
## Fix Pipeline Configuration Errors

This guide helps you resolve the service connection error and properly configure your Azure DevOps pipeline.

## 🚨 **Current Error:**
```
The pipeline is not valid. Job Deploy: Step AzureCLI input connectedServiceNameARM references service connection AzureSubscrip
```

## 🔧 **Solution Steps**

### Step 1: Create or Find Azure Service Connection

#### Option A: Create New Service Connection

1. **Navigate to Project Settings:**
   - Go to your Azure DevOps project
   - Click **Project Settings** (gear icon, bottom left)

2. **Create Service Connection:**
   - Under **Pipelines**, click **Service connections**
   - Click **New service connection**
   - Select **Azure Resource Manager**
   - Choose **Service principal (automatic)**

3. **Configure Connection:**
   - **Subscription**: Select your Azure subscription
   - **Resource group**: Leave empty for full access
   - **Service connection name**: Use one of these:
     - `AzureServiceConnection`
     - `Azure-Subscription-Connection`
     - `MyAzureConnection`
   - **Description**: "Connection for Incident Insight Hub deployment"
   - ✅ **Grant access permission to all pipelines**
   - Click **Save**

#### Option B: Find Existing Service Connection

1. Go to **Project Settings** → **Service connections**
2. Look for existing Azure connections
3. Note the exact name (case-sensitive)

### Step 2: Update Pipeline Configuration

You need to update `azure-pipelines.yml` with your actual values:

```yaml
variables:
  pythonVersion: '3.11'
  # Update these with YOUR actual values:
  azureServiceConnection: 'YOUR_ACTUAL_CONNECTION_NAME'
  resourceGroup: 'YOUR_ACTUAL_RESOURCE_GROUP'
  appName: 'YOUR_ACTUAL_APP_NAME'
  websitePort: '8000'
```

### Step 3: Create Azure Resources (if not done already)

#### Using Azure CLI:

```bash
# Login to Azure
az login

# Create resource group
az group create --name "your-rg-name" --location "East US"

# Create App Service Plan
az appservice plan create \
  --name "your-plan-name" \
  --resource-group "your-rg-name" \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --resource-group "your-rg-name" \
  --plan "your-plan-name" \
  --name "your-unique-app-name" \
  --runtime "PYTHON|3.11"
```

#### Using Azure Portal:

1. Go to [Azure Portal](https://portal.azure.com)
2. Create **Resource Group**
3. Create **App Service** (Linux, Python 3.11)
4. Note the exact names for pipeline configuration

### Step 4: Example Valid Configuration

Here's an example of properly configured variables:

```yaml
variables:
  pythonVersion: '3.11'
  azureServiceConnection: 'Azure-Subscription-1'  # Your actual connection name
  resourceGroup: 'incident-hub-rg'                # Your actual resource group
  appName: 'incident-insight-hub-dev'             # Your actual app name
  websitePort: '8000'
```

### Step 5: Common Service Connection Names

If you're unsure of the name, these are common patterns:
- `Azure-Subscription-1`
- `AzureServiceConnection`
- `Visual Studio Enterprise`
- `Azure Service Connection`
- Your subscription name

### Step 6: Verify Permissions

Ensure your service connection has:
- **Contributor** role on the resource group
- **Website Contributor** role on the App Service
- Access to the subscription

## 🛠️ **Quick Fix Commands**

### Find Your Subscription ID:
```bash
az account list --output table
```

### Find Your Resource Groups:
```bash
az group list --output table
```

### Find Your App Services:
```bash
az webapp list --output table
```

## 📝 **Configuration Checklist**

Before running the pipeline, verify:

- [ ] Service connection exists in Azure DevOps
- [ ] Service connection name is correct in `azure-pipelines.yml`
- [ ] Resource group exists in Azure
- [ ] Resource group name is correct in pipeline
- [ ] App Service exists in Azure
- [ ] App Service name is correct in pipeline
- [ ] Service connection has proper permissions

## 🔄 **Testing the Fix**

1. **Update `azure-pipelines.yml`** with correct values
2. **Commit and push** the changes:
   ```bash
   git add azure-pipelines.yml
   git commit -m "Fix service connection configuration"
   git push origin main
   ```
3. **Run the pipeline** in Azure DevOps
4. **Monitor** the Build stage - it should now pass validation

## 🚨 **Troubleshooting Additional Issues**

### If service connection creation fails:
- Check Azure subscription permissions
- Ensure you're a subscription administrator
- Try creating manually via Azure CLI

### If resource group doesn't exist:
```bash
az group create --name "your-rg-name" --location "East US"
```

### If app service doesn't exist:
```bash
az webapp create \
  --resource-group "your-rg-name" \
  --plan "your-plan-name" \
  --name "your-app-name" \
  --runtime "PYTHON|3.11"
```

## ✅ **Success Indicators**

Pipeline validation passes when:
- No red errors in pipeline validation
- Build stage starts successfully
- Service connection is recognized
- Azure resources are found

---

**Need Help?** 
1. Check Azure DevOps project settings for exact service connection names
2. Verify Azure resources exist in the portal
3. Ensure service connection has required permissions
4. Test with a simple pipeline first if issues persist 