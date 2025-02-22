test_cases = {
    # Level 0: Basic Correctness & Edge Cases (5 test cases)
    "test_case_1": {
        "inputs": {
            "grid": [
                ["1", "1", "1", "1", "0"],
                ["1", "1", "0", "1", "0"],
                ["1", "1", "0", "0", "0"],
                ["0", "0", "0", "0", "0"]
            ]
        },
        "output": 1  # One big island
    },
    "test_case_2": {
        "inputs": {
            "grid": [
                ["1", "1", "0", "0", "0"],
                ["1", "1", "0", "0", "0"],
                ["0", "0", "1", "0", "0"],
                ["0", "0", "0", "1", "1"]
            ]
        },
        "output": 3  # Three distinct islands
    },
    "test_case_3": {
        "inputs": {
            "grid": [["0"]]
        },
        "output": 0  # No land
    },
    "test_case_4": {
        "inputs": {
            "grid": [["1"]]
        },
        "output": 1  # Single cell island
    },
    "test_case_5": {
        "inputs": {
            "grid": [
                ["1", "0", "1", "0"],
                ["0", "1", "0", "1"],
                ["1", "0", "1", "0"]
            ]
        },
        "output": 6  # Diagonal islands don't connect, 6 separate islands
    },

    # Level 1: Moderate Cases (5 test cases)
    "test_case_6": {
        "inputs": {
            "grid": [
                ["1", "1", "0", "1", "1"],
                ["0", "0", "0", "0", "1"],
                ["1", "1", "1", "0", "1"],
                ["0", "0", "1", "1", "0"]
            ]
        },
        "output": 3  # Three separate land masses
    },
    "test_case_7": {
        "inputs": {
            "grid": [
                ["1"] * 10 for _ in range(10)
            ]
        },
        "output": 1  # Entire grid is one big island
    },
    "test_case_8": {
        "inputs": {
            "grid": [
                ["1"] * 5 + ["0"] * 5,
                ["1"] * 5 + ["0"] * 5,
                ["1"] * 5 + ["0"] * 5,
                ["1"] * 5 + ["0"] * 5,
                ["1"] * 5 + ["0"] * 5,
                ["0"] * 10,
                ["0"] * 10
            ]
        },
        "output": 2  # One large island on left, one large on right
    },
    "test_case_9": {
        "inputs": {
            "grid": [
                ["1", "0", "1", "0", "1"],
                ["0", "1", "0", "1", "0"],
                ["1", "0", "1", "0", "1"],
                ["0", "1", "0", "1", "0"]
            ]
        },
        "output": 9  # Each "1" is isolated
    },
    "test_case_10": {
        "inputs": {
            "grid": [
                ["0", "0", "0", "1"],
                ["0", "0", "1", "1"],
                ["0", "1", "1", "0"],
                ["1", "1", "0", "0"]
            ]
        },
        "output": 1  # All lands are connected
    },

    # Level 2: Larger Inputs (5 test cases)
    "test_case_11": {
        "inputs": {
            "grid": [
                ["1"] * 50 for _ in range(50)
            ]
        },
        "output": 1  # Single large island
    },
    "test_case_12": {
        "inputs": {
            "grid": [
                ["1" if (i+j) % 2 == 0 else "0" for j in range(50)]
                for i in range(50)
            ]
        },
        "output": 1250  # Each land cell is isolated
    },
    "test_case_13": {
        "inputs": {
            "grid": [
                ["1" if i % 10 != 0 else "0" for j in range(100)]
                for i in range(100)
            ]
        },
        "output": 10  # Vertical strips of islands
    },
    "test_case_14": {
        "inputs": {
            "grid": [
                ["0"] * 75 + ["1"] * 25 for _ in range(100)
            ]
        },
        "output": 1  # One connected island at the right
    },
    "test_case_15": {
        "inputs": {
            "grid": [
                ["1"] * 25 + ["0"] * 25 + ["1"] * 25 + ["0"] * 25
                for _ in range(100)
            ]
        },
        "output": 2  # Two major islands (left and right)
    },

    # Level 3: Stress Tests (5 test cases)
    "test_case_16": {
        "inputs": {
            "grid": [
                ["1"] * 300 for _ in range(300)
            ]
        },
        "output": 1  # One massive island
    },
    "test_case_17": {
        "inputs": {
            "grid": [
                ["1" if (i + j) % 3 == 0 else "0" for j in range(300)]
                for i in range(300)
            ]
        },
        "output": "Computed Separately"  # Randomized islands
    },
    "test_case_18": {
        "inputs": {
            "grid": [
                ["1" if i % 20 != 0 else "0" for j in range(300)]
                for i in range(300)
            ]
        },
        "output": 15  # Vertical stripes
    },
    "test_case_19": {
        "inputs": {
            "grid": [
                ["0"] * 150 + ["1"] * 150 for _ in range(300)
            ]
        },
        "output": 1  # One island on the right
    },
    "test_case_20": {
        "inputs": {
            "grid": [
                ["1" if random.random() > 0.7 else "0" for j in range(300)]
                for i in range(300)
            ]
        },
        "output": "Computed Separately"  # Large randomized test
    }
}