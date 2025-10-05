# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of Hangman Bot seriously. If you discover a security vulnerability, please follow these steps:

### Where to Report

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please report security vulnerabilities by:

1. **Email**: Send details to the project maintainer (contact information in GitHub profile)
2. **GitHub Security Advisory**: Use GitHub's private security reporting feature

### What to Include

When reporting a vulnerability, please include:

* **Description**: Clear description of the vulnerability
* **Impact**: Potential impact and attack scenario
* **Reproduction Steps**: Detailed steps to reproduce the issue
* **Version**: The version of the bot affected
* **Environment**: Python version, OS, dependencies versions
* **Proof of Concept**: If possible, provide a PoC (without exploiting)
* **Suggested Fix**: If you have ideas on how to fix it

### What to Expect

After reporting a vulnerability:

* **Acknowledgment**: You'll receive a response within 48 hours
* **Assessment**: We'll assess the vulnerability within 7 days
* **Updates**: Regular updates on the progress of fixing the issue
* **Credit**: Public acknowledgment (if desired) when the fix is released
* **Timeline**: Security patches are typically released within 14-30 days

## Security Best Practices

When using Hangman Bot:

### Bot Token Security

* **Never commit** your bot token to version control
* **Use `.env` file** for storing sensitive credentials
* **Rotate tokens** periodically
* **Limit bot permissions** to only what's necessary
* **Use `.gitignore`** to exclude `.env` files

### Deployment Security

* **Keep dependencies updated**: Regularly update `aiogram` and other packages
* **Use virtual environments**: Isolate bot dependencies
* **Monitor logs**: Watch for suspicious activity
* **Use HTTPS**: If deploying webhooks, always use HTTPS
* **Validate inputs**: The bot validates user inputs, but be cautious with extensions

### Data Privacy

* **No personal data storage**: This bot doesn't store personal user data
* **Session data**: Game state is kept in memory only during active sessions
* **Message cleanup**: Messages are automatically deleted at game end
* **No logging of user data**: User IDs and messages aren't logged persistently

## Known Security Considerations

### Current Implementation

* **In-memory state**: Game state is stored in memory (lost on restart)
* **No database**: No persistent storage of user data
* **Telegram API dependency**: Security relies on Telegram's infrastructure
* **Rate limiting**: Consider implementing rate limiting for production use

### Recommendations for Production

If deploying this bot for large-scale use:

1. **Implement rate limiting**: Prevent abuse and spam
2. **Add logging**: Monitor for unusual patterns (without storing personal data)
3. **Use webhooks**: More secure and efficient than long polling for production
4. **Deploy with HTTPS**: If using webhooks
5. **Regular updates**: Keep all dependencies up to date
6. **Monitoring**: Set up alerts for unusual activity

## Security Updates

Security updates will be:

* **Announced** in CHANGELOG.md with `[SECURITY]` tag
* **Released** as patch versions (e.g., 1.0.1)
* **Documented** with CVE numbers if applicable
* **Communicated** through GitHub releases and security advisories

## Dependencies Security

### Current Dependencies

* `aiogram>=3.13.1`: Telegram Bot API framework
* `python-dotenv>=1.0.1`: Environment variable management

### Dependency Management

* **Regular audits**: Dependencies are reviewed regularly
* **Update policy**: Security patches are applied promptly
* **Version pinning**: Major versions are pinned in requirements.txt
* **Vulnerability scanning**: Use tools like `pip-audit` or `safety`

### Checking Dependencies

To check for vulnerable dependencies:

```bash
pip install pip-audit
pip-audit
```

Or:

```bash
pip install safety
safety check
```

## Third-Party Integrations

### Telegram Bot API

* **Trusted source**: Uses official Telegram Bot API
* **HTTPS only**: All API calls use HTTPS
* **Token-based auth**: Secure token-based authentication
* **No user passwords**: Bot doesn't handle user passwords

## Responsible Disclosure

We follow responsible disclosure practices:

1. **Private reporting**: Vulnerabilities are reported privately
2. **Fix development**: We develop fixes before public disclosure
3. **Coordinated release**: Patches are released before details
4. **Credit given**: Reporters are credited (if desired)
5. **Public disclosure**: Details published only after fix is available

## Security Hall of Fame

We'd like to thank the following security researchers for responsibly disclosing vulnerabilities:

* *Currently empty - be the first!*

## Contact

For security concerns that don't qualify as vulnerabilities:

* **General questions**: Open a GitHub issue
* **Security discussions**: Use GitHub Discussions
* **Project maintainer**: Check GitHub profile for contact info

## Legal

This security policy is subject to the project's MIT License. Security research must comply with applicable laws and regulations.

---

Last Updated: October 5, 2025  
© 2025 Otabek Sadiridinov