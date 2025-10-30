"""
API Testing Script for Futurix AI
Test all endpoints and functionality
"""

import requests
import os
import json
from datetime import datetime


BASE_URL = "http://127.0.0.1:8000"


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_health_check():
    """Test the root endpoint"""
    print_section("TEST 1: Health Check")

    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            print("✅ Health check PASSED")
            return True
        else:
            print("❌ Health check FAILED")
            return False

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_upload(invoice_path, po_path):
    """Test file upload endpoint"""
    print_section("TEST 2: File Upload & Processing")

    if not os.path.exists(invoice_path):
        print(f"❌ Invoice file not found: {invoice_path}")
        return False

    if not os.path.exists(po_path):
        print(f"❌ PO file not found: {po_path}")
        return False

    try:
        files = {
            'invoice': open(invoice_path, 'rb'),
            'po': open(po_path, 'rb')
        }

        print(f"Uploading:")
        print(f"  Invoice: {invoice_path}")
        print(f"  PO: {po_path}")

        response = requests.post(f"{BASE_URL}/upload", files=files)

        print(f"\nStatus Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"\n📊 Results:")
            print(f"  Status: {result.get('status')}")
            print(f"\n  Invoice Data:")
            print(f"    Vendor: {result.get('invoice', {}).get('vendor')}")
            print(f"    Total: {result.get('invoice', {}).get('total')}")
            print(f"    Date: {result.get('invoice', {}).get('date')}")
            print(f"    Confidence: {result.get('invoice', {}).get('confidence')}")

            print(f"\n  PO Data:")
            print(f"    Vendor: {result.get('po', {}).get('vendor')}")
            print(f"    Total: {result.get('po', {}).get('total')}")
            print(f"    Date: {result.get('po', {}).get('date')}")
            print(f"    Confidence: {result.get('po', {}).get('confidence')}")

            print(f"\n  Comparison:")
            print(f"    Status: {result.get('result', {}).get('status')}")
            print(f"    Matched: {result.get('result', {}).get('matched')}")

            details = result.get('result', {}).get('details', {})
            if details:
                print(f"    Discrepancies: {list(details.keys())}")

            print("\n✅ Upload & processing PASSED")
            return True
        else:
            print(f"❌ Upload FAILED: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_history():
    """Test history endpoint"""
    print_section("TEST 3: Transaction History")

    try:
        response = requests.get(f"{BASE_URL}/history?limit=5")

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"\nTotal Transactions: {result.get('total_transactions')}")
            print(f"Showing: {result.get('showing')}")

            transactions = result.get('transactions', [])
            if transactions:
                print(f"\nRecent Transactions:")
                for i, trans in enumerate(transactions[:3], 1):
                    print(f"\n  Transaction {i}:")
                    print(f"    Vendor: {trans.get('invoice_vendor')} → {trans.get('po_vendor')}")
                    print(f"    Amount: {trans.get('invoice_total')} → {trans.get('po_total')}")
                    print(f"    Status: {trans.get('status')}")
                    print(f"    Time: {trans.get('timestamp')}")

            print("\n✅ History PASSED")
            return True
        else:
            print(f"❌ History FAILED: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_statistics():
    """Test statistics endpoint"""
    print_section("TEST 4: Statistics")

    try:
        response = requests.get(f"{BASE_URL}/stats")

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            stats = response.json()
            print(f"\n📊 Statistics:")
            print(f"  Total Processed: {stats.get('total_processed')}")
            print(f"  Matched: {stats.get('matched')}")
            print(f"  Mismatched: {stats.get('mismatched')}")
            print(f"  Match Rate: {stats.get('match_rate')}")

            print("\n✅ Statistics PASSED")
            return True
        else:
            print(f"❌ Statistics FAILED: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_export():
    """Test CSV export endpoint"""
    print_section("TEST 5: CSV Export")

    try:
        response = requests.get(f"{BASE_URL}/export")

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            # Save CSV
            filename = f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'wb') as f:
                f.write(response.content)

            print(f"✅ CSV downloaded: {filename}")

            # Show file size
            file_size = os.path.getsize(filename)
            print(f"   File size: {file_size} bytes")

            # Show first few lines
            with open(filename, 'r') as f:
                lines = f.readlines()[:5]
                print(f"\n   Preview (first 5 lines):")
                for line in lines:
                    print(f"   {line.strip()}")

            print("\n✅ Export PASSED")
            return True
        elif response.status_code == 404:
            print("⚠️  No transactions to export (upload files first)")
            return True
        else:
            print(f"❌ Export FAILED: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def run_all_tests(invoice_path=None, po_path=None):
    """Run all API tests"""
    print("\n" + "🧪" * 30)
    print("  FUTURIX AI - API TEST SUITE")
    print("🧪" * 30)

    results = {
        "Health Check": test_health_check(),
    }

    # Only test upload if files provided
    if invoice_path and po_path:
        results["File Upload"] = test_upload(invoice_path, po_path)
        results["History"] = test_history()
        results["Statistics"] = test_statistics()
        results["Export"] = test_export()
    else:
        print("\n⚠️  Skipping upload tests (no files provided)")
        print("   Usage: python test_api.py <invoice_file> <po_file>")

    # Summary
    print_section("TEST SUMMARY")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, passed_status in results.items():
        status = "✅ PASSED" if passed_status else "❌ FAILED"
        print(f"  {test_name}: {status}")

    print(f"\n  Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n  🎉 ALL TESTS PASSED!")
    else:
        print("\n  ⚠️  SOME TESTS FAILED")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    import sys

    # Check if server is running
    try:
        response = requests.get(BASE_URL, timeout=2)
    except:
        print("\n❌ ERROR: Server is not running!")
        print("   Please start the server first:")
        print("   uvicorn main:app --reload\n")
        sys.exit(1)

    # Get file paths from command line
    invoice_file = sys.argv[1] if len(sys.argv) > 1 else None
    po_file = sys.argv[2] if len(sys.argv) > 2 else None

    # Run tests
    run_all_tests(invoice_file, po_file)

