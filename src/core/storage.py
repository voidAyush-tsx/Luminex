"""
Data Storage & CSV Export Module
Handles in-memory storage and CSV generation
"""

import os
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime


class TransactionStorage:
    """In-memory storage for verified transactions"""

    def __init__(self):
        """Initialize empty transaction list"""
        self.transactions = []

    def add_transaction(self, transaction: Dict[str, Any]) -> None:
        """
        Add a new transaction to storage

        Args:
            transaction: Transaction data dictionary
        """
        self.transactions.append(transaction)
        print(f"💾 Transaction #{len(self.transactions)} stored")

    def get_all_transactions(self) -> List[Dict[str, Any]]:
        """
        Get all stored transactions

        Returns:
            List of all transactions
        """
        return self.transactions

    def get_recent_transactions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get most recent transactions

        Args:
            limit: Number of transactions to return

        Returns:
            List of recent transactions
        """
        return self.transactions[-limit:] if limit > 0 else self.transactions

    def clear(self) -> None:
        """Clear all stored transactions"""
        self.transactions = []
        print("🗑️  All transactions cleared")

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about stored transactions

        Returns:
            Statistics dictionary
        """
        total = len(self.transactions)
        matched = sum(1 for t in self.transactions if "MATCHED" in t.get("status", ""))
        mismatched = total - matched

        return {
            "total_processed": total,
            "matched": matched,
            "mismatched": mismatched,
            "match_rate": f"{(matched/total*100):.2f}%" if total > 0 else "0%"
        }


def export_to_csv(transactions: List[Dict[str, Any]], output_dir: str = "data/exports") -> str:
    """
    Export transactions to CSV file

    Args:
        transactions: List of transaction dictionaries
        output_dir: Directory to save CSV file

    Returns:
        Path to generated CSV file
    """
    try:
        # Create exports directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Prepare data for DataFrame
        csv_data = []

        for transaction in transactions:
            # Extract mismatch details if present
            details = transaction.get("details", {})
            mismatch_fields = []

            if isinstance(details, dict):
                for field, info in details.items():
                    if isinstance(info, dict) and "reason" in info:
                        mismatch_fields.append(field)

            mismatch_summary = ", ".join(mismatch_fields) if mismatch_fields else "None"

            csv_data.append({
                "Invoice Vendor": transaction.get("invoice_vendor", "N/A"),
                "PO Vendor": transaction.get("po_vendor", "N/A"),
                "Invoice Total": transaction.get("invoice_total", 0),
                "PO Total": transaction.get("po_total", 0),
                "Invoice Date": transaction.get("invoice_date", "N/A"),
                "PO Date": transaction.get("po_date", "N/A"),
                "Invoice Number": transaction.get("invoice_number", "N/A"),
                "PO Number": transaction.get("po_number", "N/A"),
                "Status": transaction.get("status", "Unknown"),
                "Mismatched Fields": mismatch_summary,
                "Timestamp": transaction.get("timestamp", "N/A")
            })

        # Create DataFrame
        df = pd.DataFrame(csv_data)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"futurix_transactions_{timestamp}.csv"
        filepath = os.path.join(output_dir, filename)

        # Export to CSV
        df.to_csv(filepath, index=False, encoding='utf-8')

        print(f"📊 CSV exported: {filepath}")
        print(f"   Total records: {len(csv_data)}")

        return filepath

    except Exception as e:
        print(f"❌ CSV export error: {str(e)}")
        raise

