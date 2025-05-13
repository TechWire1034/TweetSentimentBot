# Security Policy for TweetSentimentBot

## Supported Versions
The TweetSentimentBot project currently supports the latest version as of May 13, 2025. Security updates are applied to the `master` branch.

| Version | Supported          |
|---------|--------------------|
| Latest  | ✅                 |

## Reporting a Vulnerability
If you discover a security vulnerability, please report it responsibly:

1. **Contact**: Email the project maintainer at a private channel (not specified publicly).
2. **Details**: Provide a detailed description of the vulnerability, including steps to reproduce and potential impact.
3. **Response**: Expect an acknowledgment within 48 hours. We aim to address vulnerabilities within 14 days.
4. **Disclosure**: We follow responsible disclosure, coordinating public disclosure after mitigation.

Do not open public issues for security vulnerabilities.

## Security Practices
- **Dependencies**: Regularly update dependencies (`tweepy`, `transformers`, `matplotlib`, `python-dotenv`) to patched versions.
- **API Credentials**: Store sensitive data (e.g., Bearer Token, HF_TOKEN) in `.env`, excluded from the repository via `.gitignore`.
- **Data Handling**: Tweets are processed locally; no user data is stored or shared beyond analysis results.
- **Code Review**: All changes are reviewed before merging to ensure secure coding practices.

## Known Limitations
- The project uses the X API in Basic Access mode, limiting streaming capabilities until Production mode is approved.

