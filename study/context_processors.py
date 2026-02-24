from django.conf import settings


def github_repo(request):
    """Expose GITHUB_REPO and OAuth provider flags to all templates."""
    return {
        'GITHUB_REPO': getattr(settings, 'GITHUB_REPO', ''),
        'GITHUB_OAUTH_ENABLED': getattr(settings, 'GITHUB_OAUTH_ENABLED', False),
        'GOOGLE_OAUTH_ENABLED': getattr(settings, 'GOOGLE_OAUTH_ENABLED', False),
    }
