import pandas as pd
import random
from datetime import timedelta

# ============================================
# LOAD BASE DATASET
# ============================================
print("🚀 Creating Clean ITSM Dataset...")
print("=" * 50)

df = pd.read_csv("C:\\Users\\vidhi\\OneDrive\\Desktop\\Important stuff\\Projects\\pcghack\\ITSM_Dataset.csv")
print(f"📊 Original Shape: {df.shape}")

# ============================================
# TICKET DESCRIPTION TEMPLATES
# ============================================
text_templates = {
    "Security": [
        "Suspicious login attempts detected from unknown IP address.",
        "User reported phishing email with malicious attachment.",
        "Unusual outbound traffic detected from internal server.",
        "Firewall rule update required due to security vulnerability.",
        "Multiple failed authentication attempts on admin account.",
        "User reporting suspicious email with attachment from unknown sender claiming to be from CEO.",
        "Failed login attempts detected for admin account - 15 attempts in 2 minutes from IP 185.142.53.x.",
        "Employee's laptop showing ransomware warning popup - all files encrypted with .locky extension",
        "Unauthorized USB device detected on engineering workstation in Lab 3.",
        "SIEM alert: Unusual outbound traffic from database server to unknown external IP"
    ],
    
    "Network Ops": [
        "Users experiencing network latency in office location.",
        "VPN connection failing with authentication error.",
        "Switch outage affecting multiple departments.",
        "Packet loss detected between data centers.",
        "DNS resolution not working for internal domain.",
        "Internet connectivity slow in Bangalore office - users experiencing 500ms+ latency",
        "Cannot connect to VPN from hotel network - error code 812: connection blocked",
        "Network switch in wiring closet C03 is down - all users in west wing offline",
        "WiFi authentication failing for guests in Conference Room B",
        "Load balancer showing unhealthy backend servers for payment application"
    ],
    
    "Development": [
        "Application returning 500 error after recent deployment.",
        "Database query performance degraded significantly.",
        "Feature request submitted for dashboard enhancement.",
        "Bug identified in production affecting login flow.",
        "API integration failing with external service.",
        "API endpoint /api/v1/users returning 500 error when special characters in name",
        "Database query timing out after recent schema change - index missing on orders table",
        "Mobile app crashes on startup for Android 13 users - stack trace attached",
        "Production deployment failed - build pipeline error at step 4: Docker image not found",
        "Memory leak in payment processing service - consuming 90% heap after 24hrs"
    ],
    
    "IT Support": [
        "Laptop not booting after system update.",
        "Password reset requested for locked account.",
        "Printer not responding in office.",
        "Microsoft Office activation failed.",
        "Email not syncing on mobile device.",
        "New hire onboarding: need laptop, monitors, and software access for John Smith starting Monday",
        "Laptop won't boot - black screen with blinking cursor after Windows update",
        "Password reset request for Salesforce - user locked out after 5 attempts",
        "Printer not working on floor 7 - error message 'PC Load Letter'",
        "Can't access shared drive after recent domain password change"
    ],
    
    "Customer Service": [
        "Customer reporting billing discrepancy.",
        "Subscription cancellation request received.",
        "User unable to access account after email update.",
        "Refund requested for duplicate charge.",
        "Complaint about delayed support response.",
        "Billing question: charged twice for January subscription - need refund",
        "Can't access my account after changing email address - verification email not received",
        "How do I upgrade my plan to enterprise? Need pricing for 500 users",
        "Where's my order? Order #ORD-45678 placed 2 weeks ago, no tracking",
        "Download link expired - need new link for software installer"
    ]
}

# ============================================
# GENERATE TICKET DESCRIPTIONS
# ============================================
def generate_text(row):
    domain = row["Agent Group"]
    
    if domain in text_templates:
        base = random.choice(text_templates[domain])
    else:
        base = "General system issue reported."
    
    # Add urgency for high priority tickets
    priority = str(row["Priority"]).lower() if pd.notna(row["Priority"]) else "medium"
    
    if "high" in priority or "critical" in priority:
        urgency = " This requires immediate attention."
        return base + urgency
    
    return base

df["description"] = df.apply(generate_text, axis=1)

# ============================================
# GENERATE TIMESTAMPS
# ============================================
# Use existing time columns or create new ones
if "Created time" in df.columns:
    df["created_date"] = pd.to_datetime(df["Created time"])
else:
    # Generate random dates within last 30 days
    base_date = pd.Timestamp.now()
    df["created_date"] = [base_date - timedelta(days=random.randint(0, 30), 
                                                 hours=random.randint(0, 23),
                                                 minutes=random.randint(0, 59)) 
                          for _ in range(len(df))]

if "Resolution time" in df.columns:
    df["resolved_date"] = pd.to_datetime(df["Resolution time"])
else:
    # Resolution time = created_date + random hours
    df["resolved_date"] = df["created_date"] + pd.to_timedelta(
        [random.randint(1, 72) for _ in range(len(df))], unit="h"
    )

# Calculate resolution time in hours
df["resolution_hours"] = (df["resolved_date"] - df["created_date"]).dt.total_seconds() / 3600

# ============================================
# ADD BUSINESS FIELDS
# ============================================
# Source channel
sources = ["Email", "Phone", "Portal", "Chat", "Monitoring System"]
df["source"] = [random.choice(sources) for _ in range(len(df))]

# Current status
statuses = ["Open", "In Progress", "Pending", "Resolved", "Closed"]
df["status"] = [random.choice(statuses) for _ in range(len(df))]

# Number of affected users
df["affected_users"] = [random.randint(1, 200) for _ in range(len(df))]

# ============================================
# CALCULATE SLA BREACH
# ============================================
def check_sla_breach(row):
    priority = row["Priority"]
    resolution = row["resolution_hours"]
    
    sla_limits = {
        "Critical": 4,
        "High": 8,
        "Medium": 24,
        "Low": 48
    }
    
    limit = sla_limits.get(priority, 24)
    return 1 if resolution > limit else 0

df["sla_breach"] = df.apply(check_sla_breach, axis=1)

# ============================================
# ADD ESCALATION FLAG
# ============================================
df["escalated"] = df["resolution_hours"].apply(lambda x: 1 if x > 24 else 0)

# ============================================
# SELECT FINAL COLUMNS
# ============================================
final_columns = [
    "Ticket ID",
    "description",
    "Agent Group",
    "Priority",
    "Support Level",
    "status",
    "source",
    "affected_users",
    "created_date",
    "resolved_date",
    "resolution_hours",
    "sla_breach",
    "escalated"
]

# Keep only columns that exist
available_cols = [col for col in final_columns if col in df.columns]
df_clean = df[available_cols].copy()

# Rename columns for clarity
df_clean = df_clean.rename(columns={
    "Agent Group": "assigned_group",
    "Support Level": "support_level"
})

# ============================================
# DISPLAY STATISTICS
# ============================================
print("\n" + "="*50)
print("📊 DATASET STATISTICS")
print("="*50)
print(f"Total Tickets: {len(df_clean)}")
print(f"Date Range: {df_clean['created_date'].min()} to {df_clean['created_date'].max()}")
print(f"\nTickets by Group:")
print(df_clean['assigned_group'].value_counts())
print(f"\nPriority Distribution:")
print(df_clean['Priority'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%')
print(f"\nSLA Breach Rate: {df_clean['sla_breach'].mean():.1%}")
print(f"Escalation Rate: {df_clean['escalated'].mean():.1%}")

# ============================================
# SAVE CLEAN DATASET
# ============================================
output_file = "ITSM_Clean_Dataset.csv"
df_clean.to_csv(output_file, index=False)
print(f"\n✅ Clean dataset saved as: {output_file}")

# Show sample records
print("\n" + "="*50)
print("🔍 SAMPLE RECORDS (First 3)")
print("="*50)
print(df_clean[['Ticket ID', 'description', 'assigned_group', 'Priority', 'sla_breach']].head(3).to_string())