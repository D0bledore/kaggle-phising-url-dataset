def detect_violations(row):
    """
    Check ALL 6 rules and collect ALL violations.

    Args:
        row (Series): A row from the dataset with feature values

    Returns:
        list of (rule_name, explanation) tuples
        Empty list means URL passed all rules (proceed to ML)

    Note: "No References" rule removed after discovering 55 false positives (0.04%)
    """
    violations = []

    # Rule 1: Zero Resources
    if row['NoOfJS'] == 0 and row['NoOfCSS'] == 0 and row['NoOfImage'] == 0:
        violations.append((
            "Zero Resources",
            "Site has no JavaScript, CSS, or images - typical of lazy phishing"
        ))

    # Rule 2: No HTTPS
    if row['IsHTTPS'] == 0:
        violations.append((
            "No HTTPS",
            "Site uses HTTP instead of HTTPS - no encryption"
        ))

    # Rule 3: Domain is IP
    if row['IsDomainIP'] == 1:
        violations.append((
            "Domain is IP Address",
            "Domain is an IP address instead of proper domain name"
        ))

    # Rule 4: Zero Trust Signals
    if (row['HasTitle'] == 0 and row['HasFavicon'] == 0 and
        row['HasDescription'] == 0 and row['HasCopyrightInfo'] == 0):
        violations.append((
            "Zero Trust Signals",
            "No title, favicon, description, or copyright - minimal effort site"
        ))

    # Rule 5: Excessive Subdomains
    if row['NoOfSubDomain'] >= 5:
        violations.append((
            "Excessive Subdomains",
            f"URL has {int(row['NoOfSubDomain'])} subdomains - suspicious structure"
        ))

    # Rule 6: Long URL
    if row['URLLength'] > 57:
        violations.append((
            "Long URL",
            f"URL is {int(row['URLLength'])} characters - obfuscation technique"
        ))

    return violations
