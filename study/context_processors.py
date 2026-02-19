from django.conf import settings


def github_repo(request):
    """Make GITHUB_REPO setting available in all templates."""
    return {
        'GITHUB_REPO': getattr(settings, 'GITHUB_REPO', ''),
    }


def oauth_providers(request):
    """Make configured OAuth provider names available in all templates."""
    providers = getattr(settings, 'SOCIALACCOUNT_PROVIDERS', {})
    return {
        'oauth_github_enabled': 'github' in providers,
        'oauth_google_enabled': 'google' in providers,
    }
