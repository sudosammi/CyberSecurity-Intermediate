import requests
import sys
import json

def scan_graphql(target_url):
    print(f"\n[*] Bhai, targeting GraphQL API at: {target_url}")
    print("[*] Firing the Introspection Query to steal the API's blueprint (Kundli)...\n")
    print("--------------------------------------------------")

    # The Universal Introspection Query Payload
    # Yeh standard query har GraphQL server ko samajh aati hai
    introspection_query = {
        "query": """
        query IntrospectionQuery {
          __schema {
            types {
              name
              kind
              fields {
                name
              }
            }
          }
        }
        """
    }

    # API ko batana zaroori hai ki hum JSON bhej rahe hain
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
    }

    try:
        # POST request bhej rahe hain target par
        response = requests.post(target_url, json=introspection_query, headers=headers, timeout=10)
        
        # Hacker Logic: Agar response mein '__schema' likha hai, matlab humne blueprint chura liya!
        if response.status_code == 200 and "__schema" in response.text:
            print("   [!!!] JACKPOT 🎯 INTROSPECTION IS ENABLED!")
            print("   [!!!] We successfully downloaded the complete backend schema.\n")
            
            schema_data = response.json().get('data', {}).get('__schema', {})
            types = schema_data.get('types', [])
            
            print("--- DISCOVERED API OBJECTS (Look for hidden features!) ---")
            for t in types:
                # GraphQL ke built-in types '__' se shuru hote hain, hum unko ignore karenge
                if not t['name'].startswith('__') and t['kind'] == 'OBJECT':
                    print(f"[*] Object Name: {t['name']}")
                    if t.get('fields'):
                        # Sirf pehle 5 fields print kar rahe hain terminal clean rakhne ke liye
                        fields = [f['name'] for f in t['fields']]
                        print(f"    -> Accessible Fields: {', '.join(fields[:5])} ...")
            
            print("\n[*] Hacker Pro-Tip: Upar diye gaye Objects mein 'Admin', 'User', ya 'Token' jaise words dhoondho!")
            
        else:
            print("[-] No luck. Introspection is securely disabled, or this isn't a GraphQL endpoint.")

    except Exception as e:
        print(f"[-] Arre yaar, connection failed/timeout: {e}")

    print("--------------------------------------------------")
    print("[+] GraphQL Scan Complete, Bhai!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 graphql_hacker.py <graphql_endpoint>")
        print("Example: python3 graphql_hacker.py http://testphp.vulnweb.com/graphql")
        sys.exit(1)
        
    target = sys.argv[1]
    scan_graphql(target)
