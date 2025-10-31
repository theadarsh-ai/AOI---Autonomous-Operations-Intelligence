# AWS Credentials Diagnosis Report

## 🔍 Issue Identified

Your AWS credentials are **temporary security tokens** that have **expired or are invalid**.

---

## 📊 Test Results

```json
{
  "region": "us-east-2",
  "services": {
    "bedrock_runtime": {
      "status": "configured",
      "ready": true
    },
    "dynamodb": {
      "status": "error",
      "error": "UnrecognizedClientException: The security token included in the request is invalid"
    },
    "s3": {
      "status": "error",
      "error": "InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records"
    }
  }
}
```

---

## ⚠️ Root Cause

Your Access Key ID starts with **"ASIA..."** which indicates:

| Type | Prefix | Lifespan | Source |
|------|--------|----------|--------|
| **Your credentials** | ASIA | Temporary (1-12 hours) | AWS SSO / Assumed Role |
| **Needed credentials** | AKIA | Permanent | IAM User Access Key |

**The Problem:** Temporary credentials expire and cannot be used for long-running applications like this autonomous AI system.

**Error Details:**
1. ❌ "Security token invalid" - Your temporary credentials have expired
2. ❌ "Access Key Id does not exist" - The temporary session is no longer valid

---

## ✅ Solution: Create Permanent IAM Credentials

You have **3 options** to fix this:

### Option 1: Create IAM User with Permanent Keys (RECOMMENDED)

This is the best solution for this application because it will work 24/7 without expiring.

#### Step 1: Create IAM User
1. Log into **AWS Console**: https://console.aws.amazon.com
2. Go to **IAM** → **Users** → **Create user**
3. User name: `msp-ai-orchestrator`
4. Click **Next**

#### Step 2: Attach Permissions
Attach these managed policies:
- ✅ `AmazonBedrockFullAccess`
- ✅ `AmazonDynamoDBFullAccess`
- ✅ `AmazonS3FullAccess`

Or create a custom policy with these permissions:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock-runtime:*",
        "bedrock-agent:*",
        "bedrock-agent-runtime:*"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:*"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": "*"
    }
  ]
}
```

#### Step 3: Create Access Key
1. After creating user, click on the user name
2. Go to **Security credentials** tab
3. Scroll to **Access keys** section
4. Click **Create access key**
5. Choose **"Application running outside AWS"**
6. Click **Next** → **Create access key**
7. **IMPORTANT:** Download the CSV file or copy the credentials NOW
   - You won't be able to see the Secret Access Key again!

#### Step 4: Update Replit Secrets
1. In Replit, click the **🔒 Lock icon** (Secrets) in left sidebar
2. Update these values:
   ```
   AWS_ACCESS_KEY_ID=AKIA... (starts with AKIA, not ASIA)
   AWS_SECRET_ACCESS_KEY=your-secret-key-here
   AWS_DEFAULT_REGION=us-east-1
   ```
3. Click **Save**

#### Step 5: Test Connection
```bash
python run_backend.py
```

You should see:
```
✅ AWS Connection Status: All services connected
✅ Bedrock Runtime: configured
✅ DynamoDB: connected
✅ S3: connected
```

---

### Option 2: Use AWS SSO with Auto-Refresh (Advanced)

If you must use AWS SSO or temporary credentials:

1. **Install AWS CLI** in this Repl
2. **Configure AWS SSO** session
3. **Add refresh script** that renews tokens before they expire
4. **Run refresh script** in background process

**Downsides:**
- More complex setup
- Requires maintenance
- Can fail if SSO session expires
- Not recommended for autonomous 24/7 systems

---

### Option 3: Switch to Supported Region

Your current region is **us-east-2** (Ohio). While this is a valid region, Bedrock availability varies by region.

**Recommended Bedrock regions:**
- ✅ `us-east-1` (N. Virginia) - **BEST CHOICE**
- ✅ `us-west-2` (Oregon)
- ✅ `eu-central-1` (Frankfurt)
- ✅ `ap-southeast-1` (Singapore)

**After creating permanent credentials, update:**
```
AWS_DEFAULT_REGION=us-east-1
```

---

## 🎯 Step-by-Step Fix (Quick Guide)

### 5-Minute Fix:

1. **AWS Console** → **IAM** → **Users** → **Create user**: `msp-ai-orchestrator`

2. **Attach policies**:
   - AmazonBedrockFullAccess
   - AmazonDynamoDBFullAccess
   - AmazonS3FullAccess

3. **Create access key** → Download CSV

4. **Replit Secrets** → Update:
   ```
   AWS_ACCESS_KEY_ID=AKIA... (from CSV)
   AWS_SECRET_ACCESS_KEY=... (from CSV)
   AWS_DEFAULT_REGION=us-east-1
   ```

5. **Enable Bedrock**:
   - AWS Console → Search "Bedrock"
   - Click "Model access"
   - Enable "Claude 3.5 Sonnet"

6. **Test**:
   ```bash
   python run_backend.py
   ```

---

## 🔐 Security Best Practices

### ✅ DO:
- Create a dedicated IAM user for this application
- Use least-privilege permissions (only what's needed)
- Store credentials in Replit Secrets (never in code)
- Rotate access keys every 90 days
- Enable MFA on your AWS root account

### ❌ DON'T:
- Use root account credentials
- Share access keys with others
- Commit credentials to git
- Use the same credentials across multiple applications
- Leave unused access keys active

---

## 📋 Verification Checklist

After updating credentials, verify:

- [ ] Access Key ID starts with **AKIA** (not ASIA)
- [ ] Secret Access Key is the full string from CSV
- [ ] Region is set to **us-east-1** or other Bedrock-supported region
- [ ] Bedrock model access is **enabled** in AWS Console
- [ ] IAM user has **AmazonBedrockFullAccess** policy
- [ ] All secrets are saved in **Replit Secrets** (not code)

---

## 🆘 Still Having Issues?

### Error: "Access Denied"
**Solution:** Your IAM user needs the AmazonBedrockFullAccess policy

### Error: "Model not found"
**Solution:** Enable Claude 3.5 Sonnet in Bedrock console → Model access

### Error: "Region not supported"
**Solution:** Change AWS_DEFAULT_REGION to us-east-1

### Error: "Credentials expired"
**Solution:** You're still using temporary credentials (ASIA). Need permanent (AKIA)

---

## 📞 Next Steps

1. **Create permanent IAM credentials** (see Option 1 above)
2. **Enable Bedrock model access** in AWS Console
3. **Update Replit Secrets** with new credentials
4. **Run backend**: `python run_backend.py`
5. **Verify connection** - should see all ✅ checkmarks
6. **Watch autonomous AI in action!** 🤖

---

## Summary

**Current Status:** ❌ Temporary credentials (ASIA...) - EXPIRED  
**Required:** ✅ Permanent credentials (AKIA...)  
**Fix Time:** ~5 minutes  
**Difficulty:** Easy  

Once you create permanent IAM credentials, your autonomous MSP AI system will work perfectly 24/7!

---

**Last tested:** October 31, 2025  
**Region:** us-east-2 (recommend switching to us-east-1)  
**Issue:** Temporary AWS SSO credentials expired  
**Solution:** Create permanent IAM user with access key
