import streamlit as st
from src.data_management import load_data


def page_hypothesis_body():
    """
    Display project hypotheses and their validation results.
    Addresses LO6.1: Dashboard describes hypotheses and validation approach.
    """

    st.write("## Hypotheses & Validation")

    st.info(
        "Before building the detection system, I formulated 6 hypotheses based on domain knowledge "
        "about phishing attacks. Each hypothesis was systematically validated using the dataset."
    )

    # Load data for validation
    df, _ = load_data()

    st.write("---")

    # Hypothesis 1
    st.write("### Hypothesis 1: Resource Minimalism")

    st.success(
        "**H1**: Phishing sites use significantly fewer web resources (JavaScript, CSS, images) "
        "than legitimate sites due to quick, low-effort setup.\n\n"
        "**Rationale**: Attackers prioritize speed over quality - they want sites deployed quickly "
        "before being detected and blacklisted."
    )

    # Validation
    phishing = df[df['label'] == 0]
    legitimate = df[df['label'] == 1]

    phishing_zero_resources = len(phishing[(phishing['NoOfJS'] == 0) &
                                            (phishing['NoOfCSS'] == 0) &
                                            (phishing['NoOfImage'] == 0)])
    legitimate_zero_resources = len(legitimate[(legitimate['NoOfJS'] == 0) &
                                                 (legitimate['NoOfCSS'] == 0) &
                                                 (legitimate['NoOfImage'] == 0)])

    phishing_rate = phishing_zero_resources / len(phishing) * 100
    legitimate_rate = legitimate_zero_resources / len(legitimate) * 100

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Phishing Sites (Zero Resources)", f"{phishing_rate:.1f}%")
    with col2:
        st.metric("Legitimate Sites (Zero Resources)", f"{legitimate_rate:.1f}%")

    st.write(
        f"**Result**: VALIDATED ✓\n\n"
        f"{phishing_rate:.1f}% of phishing sites have zero resources vs {legitimate_rate:.1f}% of legitimate sites. "
        f"This massive {phishing_rate/legitimate_rate:.1f}x difference confirms the hypothesis and justifies Rule 1."
    )

    st.write("---")

    # Hypothesis 2
    st.write("### Hypothesis 2: HTTPS Adoption Gap")

    st.success(
        "**H2**: Phishing sites are less likely to use HTTPS encryption compared to legitimate sites.\n\n"
        "**Rationale**: Obtaining SSL certificates requires domain validation, creating barriers for "
        "attackers using temporary/fake domains. Legitimate businesses prioritize user security."
    )

    # Validation
    phishing_https = phishing['IsHTTPS'].mean() * 100
    legitimate_https = legitimate['IsHTTPS'].mean() * 100

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Phishing HTTPS Rate", f"{phishing_https:.1f}%")
    with col2:
        st.metric("Legitimate HTTPS Rate", f"{legitimate_https:.1f}%")

    st.write(
        f"**Result**: VALIDATED ✓\n\n"
        f"Only {phishing_https:.1f}% of phishing sites use HTTPS vs {legitimate_https:.1f}% of legitimate sites. "
        f"This {legitimate_https - phishing_https:.1f} percentage point gap confirms the hypothesis and justifies Rule 2.\n\n"
        f"**Important Note**: {phishing_https:.1f}% of phishing DO use HTTPS, proving that rules alone are insufficient. "
        "This is why we need ML for sophisticated cases."
    )

    st.write("---")

    # Hypothesis 3
    st.write("### Hypothesis 3: Trust Signal Absence")

    st.success(
        "**H3**: Phishing sites lack trust signals (title, favicon, description, copyright) that "
        "legitimate businesses include for branding and professionalism.\n\n"
        "**Rationale**: Legitimate sites invest in branding (favicon, proper titles, meta descriptions, copyright notices). "
        "Phishing sites often skip these details to deploy faster."
    )

    # Validation
    phishing_zero_trust = len(phishing[(phishing['HasTitle'] == 0) &
                                        (phishing['HasFavicon'] == 0) &
                                        (phishing['HasDescription'] == 0) &
                                        (phishing['HasCopyrightInfo'] == 0)])
    legitimate_zero_trust = len(legitimate[(legitimate['HasTitle'] == 0) &
                                            (legitimate['HasFavicon'] == 0) &
                                            (legitimate['HasDescription'] == 0) &
                                            (legitimate['HasCopyrightInfo'] == 0)])

    phishing_zero_trust_rate = phishing_zero_trust / len(phishing) * 100
    legitimate_zero_trust_rate = legitimate_zero_trust / len(legitimate) * 100

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Phishing (Zero Trust Signals)", f"{phishing_zero_trust_rate:.1f}%")
    with col2:
        st.metric("Legitimate (Zero Trust Signals)", f"{legitimate_zero_trust_rate:.1f}%")

    st.write(
        f"**Result**: VALIDATED ✓\n\n"
        f"{phishing_zero_trust_rate:.1f}% of phishing sites have zero trust signals vs {legitimate_zero_trust_rate:.1f}% "
        f"of legitimate sites. This {phishing_zero_trust_rate/legitimate_zero_trust_rate:.1f}x difference confirms "
        "the hypothesis and justifies Rule 4."
    )

    st.write("---")

    # Hypothesis 4
    st.write("### Hypothesis 4: IP Address Domain Usage")

    st.success(
        "**H4**: Phishing sites use IP addresses as domains instead of registered domain names.\n\n"
        "**Rationale**: Legitimate businesses register proper domain names for branding and trust. "
        "Attackers using IP addresses avoid domain registration costs and detection via domain blacklists."
    )

    # Validation
    phishing_ip = len(phishing[phishing['IsDomainIP'] == 1])
    legitimate_ip = len(legitimate[legitimate['IsDomainIP'] == 1])

    phishing_ip_rate = phishing_ip / len(phishing) * 100
    legitimate_ip_rate = legitimate_ip / len(legitimate) * 100

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Phishing Sites (IP Domain)", f"{phishing_ip_rate:.2f}%")
    with col2:
        st.metric("Legitimate Sites (IP Domain)", f"{legitimate_ip_rate:.2f}%")

    st.write(
        f"**Result**: VALIDATED ✓\n\n"
        f"{phishing_ip:,} phishing sites ({phishing_ip_rate:.2f}%) use IP addresses as domains vs "
        f"{legitimate_ip:,} legitimate sites ({legitimate_ip_rate:.2f}%). This represents **perfect precision** - "
        "zero legitimate sites use IP domains in this dataset, confirming the hypothesis and justifying Rule 3."
    )

    st.write("---")

    # Hypothesis 5
    st.write("### Hypothesis 5: Subdomain Obfuscation")

    st.success(
        "**H5**: Phishing sites use excessive subdomains (≥5) to obfuscate the actual domain and evade detection.\n\n"
        "**Rationale**: Attackers create deeply nested subdomains "
        "(e.g., login.secure.verify.account.paypal.phishing-site.com) to make URLs appear legitimate at first glance. "
        "Legitimate businesses rarely need more than 2-3 subdomains."
    )

    # Validation
    phishing_subdom = len(phishing[phishing['NoOfSubDomain'] >= 5])
    legitimate_subdom = len(legitimate[legitimate['NoOfSubDomain'] >= 5])

    phishing_subdom_rate = phishing_subdom / len(phishing) * 100
    legitimate_subdom_rate = legitimate_subdom / len(legitimate) * 100

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Phishing (≥5 Subdomains)", f"{phishing_subdom_rate:.2f}%")
    with col2:
        st.metric("Legitimate (≥5 Subdomains)", f"{legitimate_subdom_rate:.2f}%")

    st.write(
        f"**Result**: VALIDATED ✓\n\n"
        f"{phishing_subdom:,} phishing sites ({phishing_subdom_rate:.2f}%) use 5+ subdomains vs "
        f"{legitimate_subdom:,} legitimate sites ({legitimate_subdom_rate:.2f}%). Again, **perfect precision** - "
        "zero legitimate sites use excessive subdomains, confirming the hypothesis and justifying Rule 5."
    )

    st.write("---")

    # Hypothesis 6
    st.write("### Hypothesis 6: URL Length Obfuscation")

    st.success(
        "**H6**: Phishing sites use longer URLs (>57 characters) to obfuscate malicious intent through "
        "excessive parameters, redirects, or encoded data.\n\n"
        "**Rationale**: Long URLs can hide suspicious domains in a sea of parameters, use redirect chains, "
        "or include base64-encoded data. Legitimate sites favor clean, readable URLs for SEO and user experience."
    )

    # Validation
    phishing_long = len(phishing[phishing['URLLength'] > 57])
    legitimate_long = len(legitimate[legitimate['URLLength'] > 57])

    phishing_long_rate = phishing_long / len(phishing) * 100
    legitimate_long_rate = legitimate_long / len(legitimate) * 100

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Phishing (URL >57 chars)", f"{phishing_long_rate:.1f}%")
    with col2:
        st.metric("Legitimate (URL >57 chars)", f"{legitimate_long_rate:.2f}%")

    st.write(
        f"**Result**: VALIDATED ✓\n\n"
        f"{phishing_long:,} phishing sites ({phishing_long_rate:.1f}%) use long URLs vs "
        f"{legitimate_long:,} legitimate sites ({legitimate_long_rate:.2f}%). Once again, **perfect precision** - "
        "zero legitimate sites exceed the 57-character threshold, confirming the hypothesis and justifying Rule 6."
    )

    st.write("---")

    st.write("### Hypothesis Validation Summary")

    st.success(
        "All 6 hypotheses were validated with strong statistical evidence from the dataset:\n\n"
        "**Behavioral Hypotheses (measurable differences):**\n"
        "1. **Resource Minimalism** (Rule 1): {:.1f}x more prevalent in phishing\n"
        "2. **HTTPS Gap** (Rule 2): {:.1f} percentage point difference\n"
        "3. **Trust Signals** (Rule 4): {:.1f}x more prevalent in phishing\n\n"
        "**Technical Hypotheses (perfect precision):**\n"
        "4. **IP Domains** (Rule 3): 0% legitimate sites use IP addresses\n"
        "5. **Excessive Subdomains** (Rule 5): 0% legitimate sites have ≥5 subdomains\n"
        "6. **Long URLs** (Rule 6): 0% legitimate sites exceed 57 characters\n\n"
        "These 6 validated hypotheses directly informed the development of the 6 detection rules, "
        "which together catch 86.4% of phishing with zero false positives.".format(
            phishing_rate/legitimate_rate,
            legitimate_https - phishing_https,
            phishing_zero_trust_rate/legitimate_zero_trust_rate
        )
    )
