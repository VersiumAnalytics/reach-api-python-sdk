GENERIC_RESPONSE = {
    "versium": {
        "version": "2.0",
        "match_counts": {},
        "num_matches": 0,
        "num_results": 0,
        "query_id": "123456",
        "query_time": 0.5680129528045654,
        "results": []
    }
}
MOCK_RESPONSES = {
  "demographic": {
    "versium": {
        "version": "2.0",
        "match_counts": {
            "demographic": 1
        },
        "num_matches": 1,
        "num_results": 1,
        "query_id": "abc-123-def-456",
        "query_time": 0.3501701354980469,
        "results": [
            {
                "Individual Level Match": "Yes",
                "DOB": "199011",
                "Age Range": "25-35",
                "Gender": "Male",
                "Ethnic Group": "Western European",
                "Religion": "Protestant",
                "Occupation": "Other",
                "Language": "English",
                "Working Woman in Household": "No",
                "Senior in Household": "No",
                "Single Parent": "No",
                "Presence of Children": "No",
                "Young Adult in Household": "No",
                "Small Office or Home Office": "No",
                "Online Purchasing Indicator": "No",
                "Online Education": "No"
            }
        ],
        "input_query": {
            "first": "John",
            "last": "Doe",
            "address": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip": "10001"
        }
    }
  },
  "contact": {
    "versium": {
        "version": "2.0",
        "match_counts": {
            "address": 1
        },
        "num_matches": 1,
        "num_results": 1,
        "query_id": "abc-123-def-456",
        "query_time": 0.45166707038879395,
        "results": [
            {
                "Individual Level Match": "Yes",
                "First Name": "John",
                "Last Name": "Doe",
                "Postal Address": "123 Main St Apt 405",
                "City": "New York",
                "State": "NY",
                "Zip": "10001",
                "Country": "US"
            }
        ],
        "input_query": {
            "first": "John",
            "last": "Doe",
            "city": "New York",
            "state": "NY",
            "zip": "10001"
        }
    }
  },

  "b2conlineaudience": {
     "versium": {
        "version": "2.0",
        "match_counts": {
            "b2c_online_audience": 1
        },
        "num_matches": 1,
        "num_results": 1,
        "query_id": "5558dbde012345674f54b5febb01cc15",
        "query_time": 3.8261330127716064,
        "results": [
            {
                "adroll": [],
                "facebook": [
                    {
                        "email": [
                            "123456789a383c114887ca4bb8b8a0d26c6f266e91969017bb5a9cd02c3cc5b1",
                            "1234567893c99514f4dbf7e95d717ac7556853b797692c13c0b086713dd098a7",
                            "1234567899d843b8e40c3325790b5ab4c13158699fbef81e55d660f753c66bd2"
                        ],
                        "phone": [
                            "12345678983d1bce282bd34ff812f1fca969c30fbac4350c0d20346dc6f0aa2d",
                            "1234567894f2981b9351046051a4928d12413517af8fea0470992b85530e4aaa",
                            "12345678934ccd8ccb45850c476c42a4bbc98ecca6ef9af81e93c06d9f1527fb"
                        ],
                        "fn": [
                            "12345678946ecd878947b4eb0ac13d3cca3cf6c4940c94d90163e0a15e947203"
                        ],
                        "ln": [
                            "1234567897569962726f868bd0b003b393b97a1cc147d84703e4bb86df7db00f"
                        ],
                        "fi": [
                            "123456789dd70c3146618063c344e531e6d4b59e379808443ce962b3abd63c5a"
                        ],
                        "ct": [
                            "1234567895be0a4d24ee98a7860a53046a6f5123bc73fd181b0a0f2b9823ddb0"
                        ],
                        "st": [
                            "123456789b7c739690268360ea392429368787010a558a1837643058d2437dce"
                        ],
                        "country": [
                            "123456789ce5c6ba215fe5f27f532d4e7edbac4b6a5e09e1ef3a08084a904621"
                        ],
                        "zip": [
                            "1234567898d18c5668b644358d52a1e37013dccaa69ca002f85cfcc8ec6d2426"
                        ]
                    }
                ],
                "generic": [
                    {
                        "email": [
                            "d1234567890b7d0d930b6e89e3c719a1517073aded2b2bcb6fbb4165d1586742"
                        ]
                    },
                    {
                        "email": [
                            "ba123456789107053e688a6d19e14033b2f0a022273a6c958336e9c19b541c9b"
                        ]
                    }
                ],
                "google": [
                    {
                        "Email": [
                            "ea123456789b350f89fc074da4a788af3ed956429037d802ac5d6ce9ec9453e6",
                            "3c123456789cb615e32b5e5025846f57e5102c3df72a9914a119ddda27643b2a",
                            "23123456789e2a7638218fccf94abbf3f33bd50f140a0420633f8192d8f91537",
                            "881234567895594eee113ca224e2ae6173ddc5d8fc3353ab7820482cb7ceace2",
                            "e91234567896e9c202f5d4a980cccb85edf4facb09c8c29c20192ce65e46a726",
                            "e612345678917040c991ec08dd34fa2ef0ea742821f4eae1b1ba4dd0f7476b50",
                            "ae1234567891f49534c46b7fd94005aa8b1ea28cd63abe8bb0df3a3f7274f6c2"
                        ],
                        "Phone": [
                            "e2123456789ba33453a097328cb402ad612dc54d3a125d923ada86f6685398dd",
                            "91123456789d1bce282bd34ff812f1fca969c30fbac4350c0d20346dc6f0aa2d",
                            "fc1234567892981b9351046051a4928d12413517af8fea0470992b85530e4aaa",
                            "7a123456789d658ba8b9c651157cb5041ddd6e87cb29c09109d2a989842cffb1",
                            "2312345678984fa42670526167cc3775b01cc8c99a712b7f6fbd2d75c3b2838e",
                            "6d123456789e30dcd326ddbe17f97714f0a587abe871f40ffea323226a3a283c",
                            "de1234567899c0ebb790f85b66752b0f52c60776891fcff0df941341bf600c43"
                        ],
                        "First Name": [
                            "68123456789ecd878947b4eb0ac13d3cca3cf6c4940c94d90163e0a15e947203"
                        ],
                        "Last Name": [
                            "a612345678969962726f868bd0b003b393b97a1cc147d84703e4bb86df7db00f"
                        ],
                        "Zip": [
                            "10001"
                        ],
                        "Country": [
                            "us"
                        ]
                    }
                ],
                "linkedin": [],
                "original": [
                    {
                        "email": [
                            ""
                        ]
                    }
                ]
            }
        ],
        "input_query": {
            "first": "John",
            "last": "Doe",
            "city": "New York",
            "state": "NY",
            "zip": "10001"
        }
    }
  },

  "b2bonlineaudience": {
    "versium": {
        "version": "2.0",
        "match_counts": [],
        "num_matches": 0,
        "num_results": 1,
        "query_id": "5558dbde012345674f54b5febb01cc15",
        "query_time": 1.5494139194488525,
        "results": [
            {
                "adroll": [],
                "facebook": [
                    {
                        "email": [
                            "55545362714c69baf4fce267a1234567897962877dc77c03faa93a6b69bcb9e0a2",
                            "5557ef2e49da6176f0354d909123456789476394eb8d6ed24487b868804cfa3242",
                            "555ba015fad0ff361d000150d1234567892c6bb8d89645c6d3ad4a46cf6b8fbe13"
                        ],
                        "phone": [
                            "555c5a98e6b07f3368f3236d8f123456789c6331106574c2de838f18cc6f76cbd5",
                            "555d3ad20e224dc262280c84d812345678936ba83d07b87e7e2dacb8e8be4c54df",
                            "555a581afd2ad8a909868f32961234567892617a25ccb06143c9df5b3535b36321"
                        ],
                        "fn": [
                            "555e7550846ecd878947b4eb0a123456789a3cf6c4940c94d90163e0a15e947203"
                        ],
                        "ln": [
                            "555ded4217569962726f868bd01234567893b97a1cc147d84703e4bb86df7db00f"
                        ],
                        "fi": [
                            "55566a7a5dd70c3146618063c31234567896d4b59e379808443ce962b3abd63c5a"
                        ],
                        "ct": [
                            "5554b29c05be0a4d24ee98a786123456789a6f5123bc73fd181b0a0f2b9823ddb0"
                        ],
                        "st": [
                            "555810070b7c739690268360ea12345678968787010a558a1837643058d2437dce"
                        ],
                        "country": [
                            "555db2a2fce5c6ba215fe5f27f123456789edbac4b6a5e09e1ef3a08084a904621"
                        ],
                        "zip": [
                            "55553c0278d18c5668b644358d123456789013dccaa69ca002f85cfcc8ec6d2426"
                        ]
                    }
                ],
                "generic": [],
                "google": [
                    {
                        "Email": [
                            "5553ca84d8f8a77d49e74f766012345678999cea263e923e607c06a496e91b7030",
                            "555bee37e4b42446c1212bfabc1234567896697ea8517124ca356592254e0ce385",
                            "555cf640b8aa579c87e40aa890123456789f5f8b4393fc3e6df3ff4d0010b0815f",
                            "555d71efe7681d844242dba491123456789e49b2a21a9a01c083a99ab3befc6d26",
                            "5550f8dce2a97ec44e68ff889b123456789609496a7c542bc05e39a6fbaf106fff",
                            "555d915f5ca5729255669324191234567899205b516c9d7a67b79b763dde10c8cc",
                            "555205034c04fafa7069e7d8ed123456789bd1b313c90ef738e6c8a5d37cc7fc38",
                            "555ea4bc86f1a8eaa975f7afec1234567895cd1510285b5dba7391ab1d110bc034"
                        ],
                        "Phone": [
                            "5555194804b3265220ae5c5e0f885a7c9e1e42eeac65e9d731d53698a45ab724",
                            "55574e73146428b55425a2175854b1a08a17408d27542b3d92b84bc5599f24c2",
                            "555042fca06d54f875590e4c695a981eef459481f6c0548f5532e75d91435b29",
                            "55549cce792429688a4b8e5a0c6b650abf5b656c30d7fc505b0983394a9f703d",
                            "555fc928e75b04a5625c097bcfc3e57a3ceb17533214f983a0d953205383a63b",
                            "5559eedc83f51c6d0787e8c7b806a7cfcfe2252be711ef3599eb84dc8e3df6fb",
                            "5556ca8c62fc5f2c104cb1c0f123456789b5a208b99f8e54782eeda2437ee5814a"
                        ],
                        "First Name": [
                            "555e7550846ecd899893243240ac13d3cca3cf6c4940c94d90163e0a15e947203"
                        ],
                        "Last Name": [
                            "555ded42175695785426f868bd0b003b393b97a1cc147d84703e4bb86df7db00f"
                        ],
                        "Zip": [
                            "10001"
                        ],
                        "Country": [
                            "us"
                        ]
                    }
                ],
                "linkedin": [],
                "original": [
                    {
                        "email": [
                            ""
                        ]
                    }
                ]
            }
        ],
        "input_query": {
            "first": "John",
            "last": "Doe",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
            "business": "Versium"
        }
    }
  },
  "firmographic": {
    "versium": {
        "version": "2.0",
        "match_counts": {
            "firmographic": 1
        },
        "num_matches": 1,
        "num_results": 1,
        "query_id": "555b4c658123456789a18dbf2b2dccfb",
        "query_time": 0.17173981666564941,
        "results": [
            {
                "Business": "Versium Analytics, Inc.",
                "Postal Address": "7530 164th Avenue Ne",
                "City": "Redmond",
                "State": "WA",
                "Zip": "98052",
                "Country": "US",
                "Domain": "versium.com",
                "Number of Employees": "123",
                "Sales Volume": "123456",
                "Year Founded": "2012",
                "SIC": "7374",
                "Public or Private": "Private"
            }
        ],
        "input_query": {
            "domain": "versium.com"
        }
    }
},
  "c2b": {
    "versium": {
        "version": "2.0",
        "match_counts": {
            "c2b": 1
        },
        "num_matches": 1,
        "num_results": 1,
        "query_id": "5558dbde012345674f54b5febb01cc15",
        "query_time": 0.5680129528045654,
        "results": [
            {
                "Title": "Software Engineer",
                "First Name": "John",
                "Last Name": "Doe",
                "Email Address": "jdoe@versium.com",
                "Business": "Versium",
                "Postal Address": "7530 164th Avenue Ne",
                "City": "Redmond",
                "State": "WA",
                "Zip": "98052",
                "Domain": "versium.com",
                "Number of Employees": "123",
                "Sales Volume": "123456",
                "Year Founded": "2012",
                "SIC": "7374",
                "SIC Description": "Data Processing And Preparation",
                "Public or Private": "Private"
            }
        ],
        "input_query": {
            "first": "John",
            "last": "Doe",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
            "email": "jdoe@gmail.com"
        }
    }
  },
  "iptodomain": {"versium": {
        "version": "2.0",
        "match_counts": {
            "ip_to_domain": 1
        },
        "num_matches": 1,
        "num_results": 1,
        "query_id": "5558dbde012345674f54b5febb01cc15",
        "query_time": 0.23208904266357422,
        "results": [
            {
                "IP Usage Type": "Commercial",
                "Is ISP?": "No",
                "Domain 1": "versium.com",
                "Company Name 1": "Versium Analytics, Inc.",
                "Company Address 1": "7530 164th Avenue Ne",
                "Company City 1": "Redmond",
                "Company State 1": "WA",
                "Company Zip 1": "98052",
                "Company Country 1": "US",
                "Employee Range 1": "123",
                "Sales Revenue Range 1": "123456",
                "Year Founded 1": "2012",
                "SIC 1": "7374",
                "Public/Private 1": "Private",
                "Domain 2": "versium2.com",
                "Company Name 2": "Versium2 Analytics, Inc.",
                "Company Address 2": "7530 164th Avenue Ne",
                "Company City 2": "Redmond",
                "Company State 2": "WA",
                "Company Zip 2": "98052",
                "Company Country 2": "US",
                "Employee Range 2": "123",
                "Sales Revenue Range 2": "123456",
                "Year Founded 2": "2012",
                "SIC 2": "7374",
                "Public/Private 2": "Private",
                "Domain 3": "versium2.com",
                "Company Name 3": "Versium2 Analytics, Inc.",
                "Company Address 3": "7530 164th Avenue Ne",
                "Company City 3": "Redmond",
                "Company State 3": "WA",
                "Company Zip 3": "98052",
                "Company Country 3": "US",
                "Employee Range 3": "123",
                "Sales Revenue Range 3": "123456",
                "Year Founded 3": "2012",
                "SIC 3": "7374",
                "Public/Private 3": "Private"
            }
        ],
        "input_query": {
            "ip": "73.157.111.58"
        }
    }
  },
  "hemtobusinessdomain": {
    "versium": {
        "version": "2.0",
        "match_counts": {
            "hem_to_business_domain": 1
        },
        "num_matches": 1,
        "num_results": 1,
        "query_id": "55561a5a01234580de7bc7007870352a",
        "query_time": 0.09659481048583984,
        "results": [
            {
                "Domain": "versium.com"
            }
        ],
        "input_query": {
            "email": "555520f123456789dcfca57fa0ff032d"
        }
    }
  }
}
