import json

def generate_txn(num):
    txns = []

    for i in range(1, num + 1):
        txn = {
            "payer": f"0x12345ExamplePayerAddress{i:05}",
            "receiver": f"dummy@pay{i}",
            "action": [
                {
                    "transaction": {
                        "tx": f"0xabcdef{i:012}",
                        "chain": i % 5 + 1,
                        "type": "OTHER"
                    }
                },
                {
                    "type": "PAYMENT",
                    "data": {
                        "token": f"0x98765ExampleTokenAddress{i:05}",
                        "chain": i % 5 + 1,
                        "receiver": f"0x67890ExampleReceiverAddress{i:05}",
                        "amount": {
                            "amount": str(250 + i),
                            "currency": "CRYPTO"
                        }
                    }
                }
            ],
            "message": f"Hello World{i}",
            "label": f"45{i}",
            "signature": f"0xabcdef{i:06}"
        }
        txns.append(txn)

    return txns

def main():
    num_of_txns = int(input("Enter the number of transactions you want to generate: "))

    txns = generate_txn(num_of_txns)

    with open('payload.json', 'w') as f:
        json.dump(txns, f, indent=4)

    print(f"Generated {num_of_txns} transactions and saved to 'payload.json'")

if __name__ == "__main__":
    main()
