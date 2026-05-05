import requests
import sys

def scan_s3_buckets(company_name):
    print(f"\n[*] Bhai, starting The Cloud Plunderer: AWS S3 Bucket Scanner...")
    print(f"[*] Generating bucket permutations for target: '{company_name}'\n")
    print("==================================================")

    # The Hacker's Dictionary of common bucket naming patterns
    suffixes = [
        "", "-dev", "-prod", "-test", "-staging", "-assets", "-media", 
        "-public", "-backup", "-static", "-api", "app", "-data"
    ]

    found_buckets = 0

    print("[*] Launching payloads against AWS servers...\n")

    for suffix in suffixes:
        bucket_name = f"{company_name}{suffix}"
        target_url = f"http://{bucket_name}.s3.amazonaws.com"
        
        try:
            # We use a short timeout to speed up the scan
            response = requests.get(target_url, timeout=5)
            status = response.status_code
            text = response.text

            if status == 200 and "<ListBucketResult>" in text:
                print(f"   [!!!] JACKPOT 🎯 PUBLIC BUCKET FOUND!")
                print(f"   [!!!] URL: {target_url}")
                print(f"   [!!!] The bucket is exposing its files! Open the URL to see the XML directory listing.\n")
                found_buckets += 1
                
            elif status == 403:
                # 403 Access Denied means the bucket EXISTS, but it is secure (Private)
                print(f"   [-] Secure: {bucket_name} exists but access is denied (HTTP 403).")
                
            elif status == 404:
                # 404 NoSuchBucket means this bucket name is available/doesn't exist
                # Silently ignore to keep the terminal output clean
                pass
                
        except requests.exceptions.RequestException:
            pass # Ignore connection errors

    print("\n==================================================")
    if found_buckets > 0:
        print(f"[+] Scan Complete! Found {found_buckets} publicly readable S3 Buckets. Time to claim the bounty! 💸")
    else:
        print("[-] Scan Complete. No exposed S3 buckets found for this target pattern.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 s3_plunderer.py <Company_Base_Name>")
        print("Example: python3 s3_plunderer.py uber")
        sys.exit(1)
        
    company = sys.argv[1].lower()
    scan_s3_buckets(company)
