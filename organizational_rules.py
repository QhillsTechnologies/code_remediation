def rules_text():
    text1 = """
    # Organizational Vulnerability Priority List

This document outlines our organization's customized prioritization of common security vulnerabilities, which may differ from standard severity ratings based on our specific business context, technical environment, and risk tolerance.

## Priority Levels

| Priority Level | Description | Response Timeframe |
|----------------|-------------|-------------------|
| **Critical** | Vulnerabilities that pose an immediate and severe risk to core business operations or sensitive data | Immediate remediation (24-48 hours) |
| **High** | Significant security issues that could lead to substantial business impact | Remediation within 1 week |
| **Medium** | Important security issues that should be addressed in the normal development cycle | Remediation within 1 month |
| **Low** | Minor security issues that present minimal risk to the organization | Address during regular maintenance cycles |

## JavaScript Vulnerabilities

| Vulnerability | Standard Rating | Our Priority | Rationale |
|--------------|-----------------|--------------|-----------|
| Cross-Site Scripting (XSS) | High | **Medium** | Our application uses Content-Security-Policy headers and serves mostly authenticated users, reducing the impact of XSS vulnerabilities |
| Prototype Pollution | High | **High** | Given our extensive use of JavaScript frameworks, prototype pollution could affect multiple systems and should be treated as a high priority |
| Insecure Direct Object References (IDOR) | High | **Critical** | Direct access to our customer and financial data makes this a critical issue for our organization |
| NoSQL Injection | High | **Medium** | Our NoSQL databases contain non-critical data and have additional access controls in place |
| DOM-based Vulnerabilities | Medium | **Low** | Our client-side architecture limits the impact of most DOM-based vulnerabilities |
| Client-side Authorization Checks | Medium | **High** | All security controls must be enforced server-side; any client-side only checks create significant exposure |

## Python Vulnerabilities

| Vulnerability | Standard Rating | Our Priority | Rationale |
|--------------|-----------------|--------------|-----------|
| SQL Injection | Critical | **Critical** | Maintains critical status due to our extensive relational database usage for core operations |
| Command Injection | Critical | **Critical** | Our backend systems run with elevated privileges, making command injection a severe threat |
| Path Traversal | High | **Medium** | Our file system permissions and containerization reduce the impact of path traversal issues |
| Insecure Deserialization | High | **High** | Given our microservice architecture, deserialization attacks could affect multiple services |
| Cross-Site Request Forgery (CSRF) | Medium | **Low** | Our implementation of proper CSRF tokens and same-site cookies significantly mitigates this risk |
| Weak Password Storage | High | **Critical** | Customer account protection is a top business priority, making password security critical |

## PHP Vulnerabilities

| Vulnerability | Standard Rating | Our Priority | Rationale |
|--------------|-----------------|--------------|-----------|
| SQL Injection | Critical | **High** | Our PHP applications use ORM layers that reduce but don't eliminate this risk |
| Remote File Inclusion | Critical | **Medium** | Our deployment architecture restricts access to external resources, limiting the impact |
| XSS | High | **Medium** | Our PHP applications implement output encoding and have limited user-facing components |
| CSRF | Medium | **Low** | Our PHP applications implement proper CSRF protection |
| Insecure Deserialization | High | **High** | Several critical flows use PHP serialization/deserialization |

## Java Vulnerabilities

| Vulnerability | Standard Rating | Our Priority | Rationale |
|--------------|-----------------|--------------|-----------|
| XML External Entity (XXE) Injection | High | **Critical** | Our extensive use of XML processing for B2B integrations makes this a critical concern |
| SQL Injection | Critical | **Medium** | Our Java applications primarily use parameterized queries and ORM frameworks, reducing this risk |
| Insecure Deserialization | High | **Critical** | Our Java applications heavily use serialization for data transfer between services |
| Path Traversal | High | **Low** | Our Java applications implement strict access controls limiting the impact |
| Improper Authentication | Critical | **High** | Authentication flaws could impact security but our multi-layer authentication reduces some risk |

## C/C++ Vulnerabilities

| Vulnerability | Standard Rating | Our Priority | Rationale |
|--------------|-----------------|--------------|-----------|
| Buffer Overflow | Critical | **Medium** | Most of our C/C++ code is used in non-internet-facing applications |
| Memory Leaks | Medium | **High** | System stability is crucial for our continuous operations, making memory leaks higher priority |
| Use After Free | High | **Medium** | Limited deployment of C/C++ code reduces organization-wide impact |
| Integer Overflow | Medium | **Low** | Our numeric processing has built-in bounds checking |
| Format String Vulnerabilities | High | **Medium** | Our logging and formatting operations have standardized implementations |

## Go Vulnerabilities

| Vulnerability | Standard Rating | Our Priority | Rationale |
|--------------|-----------------|--------------|-----------|
| Template Injection | High | **Medium** | Our Go applications use templates with limited data input |
| SQL Injection | Critical | **High** | Our Go microservices handle important data but have multiple protection layers |
| Improper Error Handling | Medium | **High** | Proper error handling is critical for our observability and monitoring strategy |
| CSRF | Medium | **Low** | Our API architecture makes CSRF attacks difficult |
| Insecure Randomness | Medium | **Critical** | Our Go services handle authentication token generation, making secure randomness essential |

## Implementation Guidelines

### Vulnerability Management Process

1. **Scanning**: All code should be scanned for vulnerabilities before deployment
2. **Prioritization**: Vulnerabilities should be prioritized according to this document
3. **Assignment**: Issues should be assigned based on the priority level
4. **Remediation**: Fixes should be implemented within the specified timeframes
5. **Verification**: All fixes should be verified with appropriate testing
6. **Reporting**: Regular vulnerability reports should highlight changes in the security posture

### Exceptions

Exceptions to these priority levels may be granted in the following cases:

1. Business-critical deployments with compensating controls
2. Third-party code where patches are not yet available
3. Legacy systems with planned replacement within 6 months

All exceptions must be documented and approved by the security team and relevant business owner.

### Review Cycle

This priority list should be reviewed quarterly to ensure it remains aligned with:

1. Current business objectives
2. Technology stack changes
3. Threat landscape developments
4. Actual incidents and near-misses


    """
    return text1