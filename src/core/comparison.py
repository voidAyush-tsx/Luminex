"""
Discrepancy Detection Engine
Compares invoice and PO data to identify mismatches
"""

from typing import Dict, Any
from fuzzywuzzy import fuzz
from datetime import datetime
from src.core.config import settings


def fuzzy_match_vendor(vendor1: str, vendor2: str, threshold: int = None) -> bool:
    """
    Check if two vendor names match using fuzzy logic

    Args:
        vendor1: First vendor name
        vendor2: Second vendor name
        threshold: Minimum similarity score (0-100)

    Returns:
        True if vendors match, False otherwise
    """
    if threshold is None:
        threshold = settings.VENDOR_FUZZY_THRESHOLD

    if not vendor1 or not vendor2:
        return False

    # Calculate similarity ratio
    ratio = fuzz.ratio(vendor1.lower(), vendor2.lower())

    print(f"  Vendor similarity: {ratio}% (threshold: {threshold}%)")

    return ratio >= threshold


def compare_amounts(amount1: float, amount2: float, tolerance_percent: float = None) -> tuple:
    """
    Compare two amounts with tolerance

    Args:
        amount1: First amount
        amount2: Second amount
        tolerance_percent: Acceptable difference percentage

    Returns:
        Tuple of (matches, difference, difference_percent)
    """
    if tolerance_percent is None:
        tolerance_percent = settings.AMOUNT_TOLERANCE_PERCENT

    if amount1 is None or amount2 is None:
        return False, None, None

    difference = abs(amount1 - amount2)
    avg_amount = (amount1 + amount2) / 2
    difference_percent = (difference / avg_amount * 100) if avg_amount > 0 else 0

    matches = difference_percent <= tolerance_percent

    print(f"  Amount difference: {difference:.2f} ({difference_percent:.2f}%, tolerance: {tolerance_percent}%)")

    return matches, difference, difference_percent


def compare_dates(date1_str: str, date2_str: str, tolerance_days: int = None) -> tuple:
    """
    Compare two dates with tolerance

    Args:
        date1_str: First date string
        date2_str: Second date string
        tolerance_days: Acceptable difference in days

    Returns:
        Tuple of (matches, difference_days)
    """
    if tolerance_days is None:
        tolerance_days = settings.DATE_TOLERANCE_DAYS

    if not date1_str or not date2_str:
        return False, None

    try:
        # Parse dates
        date_formats = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y']

        date1 = None
        date2 = None

        for fmt in date_formats:
            try:
                date1 = datetime.strptime(date1_str, fmt)
                break
            except ValueError:
                continue

        for fmt in date_formats:
            try:
                date2 = datetime.strptime(date2_str, fmt)
                break
            except ValueError:
                continue

        if not date1 or not date2:
            # If parsing fails, do exact string match
            return date1_str == date2_str, None

        # Calculate difference
        difference = abs((date1 - date2).days)
        matches = difference <= tolerance_days

        print(f"  Date difference: {difference} days (tolerance: {tolerance_days} days)")

        return matches, difference

    except Exception as e:
        print(f"  Date comparison error: {str(e)}")
        return date1_str == date2_str, None


def compare_invoice_po(invoice_data: Dict[str, Any], po_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare invoice and PO data to detect discrepancies

    Args:
        invoice_data: Extracted invoice data
        po_data: Extracted PO data

    Returns:
        Dictionary with comparison results
    """
    print("\n⚖️  Starting comparison...")

    mismatches = {}

    # Compare vendor
    print("\n🏢 Comparing vendors...")
    vendor_match = fuzzy_match_vendor(
        invoice_data.get("vendor"),
        po_data.get("vendor")
    )

    if not vendor_match:
        mismatches["vendor"] = {
            "invoice": invoice_data.get("vendor", "N/A"),
            "po": po_data.get("vendor", "N/A"),
            "reason": "Vendor names do not match (fuzzy match < 85%)"
        }

    # Compare total amounts
    print("\n💰 Comparing amounts...")
    amount_match, amount_diff, amount_diff_percent = compare_amounts(
        invoice_data.get("total"),
        po_data.get("total")
    )

    if not amount_match:
        mismatches["total"] = {
            "invoice": invoice_data.get("total", 0),
            "po": po_data.get("total", 0),
            "difference": amount_diff,
            "difference_percent": f"{amount_diff_percent:.2f}%" if amount_diff_percent else "N/A",
            "reason": f"Amount difference exceeds tolerance (diff: {amount_diff_percent:.2f}%)"
        }

    # Compare dates
    print("\n📅 Comparing dates...")
    date_match, date_diff = compare_dates(
        invoice_data.get("date"),
        po_data.get("date")
    )

    if not date_match:
        mismatches["date"] = {
            "invoice": invoice_data.get("date", "N/A"),
            "po": po_data.get("date", "N/A"),
            "difference_days": date_diff,
            "reason": f"Dates do not match (diff: {date_diff} days)" if date_diff else "Dates do not match"
        }

    # Determine overall status
    if mismatches:
        status = "MISMATCH ⚠️"
        print(f"\n❌ Discrepancies found: {len(mismatches)}")
    else:
        status = "MATCHED ✅"
        print(f"\n✅ All fields matched!")

    # Build result
    result = {
        "status": status,
        "matched": not bool(mismatches),
        "total_checks": 3,
        "passed_checks": 3 - len(mismatches),
        "details": mismatches if mismatches else {
            "message": "All fields matched successfully",
            "vendor_match": True,
            "amount_match": True,
            "date_match": True
        },
        "summary": {
            "vendor": "✅ Matched" if vendor_match else "❌ Mismatch",
            "amount": "✅ Matched" if amount_match else "❌ Mismatch",
            "date": "✅ Matched" if date_match else "❌ Mismatch"
        }
    }

    return result

