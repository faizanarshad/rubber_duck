#!/usr/bin/env python3
"""
Test script for CSV processing functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.csv_processor import CSVProcessor

def test_csv_processing():
    """Test CSV processing with sample medical data"""
    csv_processor = CSVProcessor()
    
    # Test files
    test_files = [
        "sample_documents/medical_conditions.csv",
        "sample_documents/lab_results.csv"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n=== Testing {test_file} ===")
            
            # Test validation
            is_valid = csv_processor.validate_csv_file(test_file)
            print(f"File validation: {'PASSED' if is_valid else 'FAILED'}")
            
            if is_valid:
                # Get file info
                csv_info = csv_processor.get_csv_info(test_file)
                print(f"Rows: {csv_info.get('rows', 'N/A')}")
                print(f"Columns: {csv_info.get('columns', 'N/A')}")
                print(f"Medical content: {csv_info.get('medical_info', {}).get('is_medical', False)}")
                print(f"Content type: {csv_info.get('medical_info', {}).get('content_type', 'unknown')}")
                print(f"Estimated documents: {csv_info.get('estimated_documents', 'N/A')}")
                
                # Test document creation
                try:
                    documents = csv_processor.process_csv_to_documents(test_file, f"test_{os.path.basename(test_file)}")
                    print(f"Generated documents: {len(documents)}")
                    
                    # Show first document sample
                    if documents:
                        first_doc = documents[0]
                        print(f"First document ID: {first_doc['id']}")
                        print(f"First document text (first 200 chars): {first_doc['text'][:200]}...")
                        print(f"Metadata: {first_doc['metadata']}")
                    
                except Exception as e:
                    print(f"Document processing failed: {str(e)}")
        else:
            print(f"Test file not found: {test_file}")

if __name__ == "__main__":
    print("Testing CSV Processing Functionality")
    print("=" * 50)
    test_csv_processing()
    print("\nTesting completed!")

