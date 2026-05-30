import time
from parse_xml import parse_xml

XML_FILE = "modified_sms_v2.xml"


def linear_search(transactions, target_id):
    for transaction in transactions:
        if transaction["id"] == target_id:
            return transaction
    return None


def dictionary_lookup(transaction_dict, target_id):
    return transaction_dict.get(target_id)


def measure_time(function, *args):
    start = time.perf_counter()
    result = function(*args)
    end = time.perf_counter()

    return result, end - start


def main():
    transactions = parse_xml(XML_FILE)

    # Use at least 20 records as required by the assignment
    test_transactions = transactions[:20]

    # Create dictionary: id → transaction
    transaction_dict = {
        transaction["id"]: transaction
        for transaction in test_transactions
    }

    # Pick the last ID so linear search has to work harder
    target_id = test_transactions[-1]["id"]

    linear_result, linear_time = measure_time(
        linear_search,
        test_transactions,
        target_id
    )

    dict_result, dict_time = measure_time(
        dictionary_lookup,
        transaction_dict,
        target_id
    )

    print("DSA Search Comparison")
    print("----------------------")
    print(f"Number of records tested: {len(test_transactions)}")
    print(f"Target transaction ID: {target_id}")
    print()
    print(f"Linear search result found: {linear_result is not None}")
    print(f"Linear search time: {linear_time:.10f} seconds")
    print()
    print(f"Dictionary lookup result found: {dict_result is not None}")
    print(f"Dictionary lookup time: {dict_time:.10f} seconds")
    print()
    print("Conclusion:")
    print("Linear search checks transactions one by one, so its time complexity is O(n).")
    print("Dictionary lookup finds a transaction directly by ID, so its average time complexity is O(1).")
    print("Therefore, dictionary lookup is faster and more efficient for searching by transaction ID.")


if __name__ == "__main__":
    main()