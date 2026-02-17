from django.conf import settings


def github_repo(request):
    """Make GITHUB_REPO setting available in all templates."""
    return {
        'GITHUB_REPO': getattr(settings, 'GITHUB_REPO', ''),
    }
