"""
Migration 0029 — Restructure Mathematics

Splits the single "Engineering Mathematics" course into five courses that mirror
the actual CDU units a student takes:

  Foundation Mathematics (FOUND101)  — pre-university / bridging
  Mathematics 1A         (SMA101)    — CDU SMA101
  Mathematics 1B         (SMA102)    — CDU SMA102
  Mathematics 2          (SMA209)    — CDU SMA209
  Data Analytics         (SMA212)    — CDU SMA212 (new content)

Steps
-----
1. Create the five new courses under the system user.
2. Move existing topics from Engineering Mathematics to their new home,
   updating each topic's `code` to its new position in the new course.
3. Create new topics that were absent from the old Engineering Mathematics course.
4. Delete Engineering Mathematics (now empty).
5. Back-fill CourseEnrollment for all non-system users for the five new courses.

Idempotent: get_or_create / filter().update() with guards throughout.
Reverse: intentional no-op (see reverse_func).
"""

from django.db import migrations

# ---------------------------------------------------------------------------
# Topic assignments
# ---------------------------------------------------------------------------

# Topics to MOVE from Engineering Mathematics to a new course.
# Structure: (old_topic_name, new_course_code, new_topic_code)
MOVES = [
    # → Foundation Mathematics
    ("Basic Arithmetic & Number Sense",      "FOUND101", "001A"),
    ("Algebra Fundamentals",                 "FOUND101", "001B"),
    ("Geometry",                             "FOUND101", "002A"),
    ("Trigonometry Fundamentals",            "FOUND101", "002B"),
    ("Pre-Calculus",                         "FOUND101", "003A"),
    # → Mathematics 1A
    ("Differential Calculus",                "SMA101",   "002A"),
    ("Integral Calculus",                    "SMA101",   "003A"),
    ("Linear Algebra",                       "SMA101",   "005A"),
    # → Mathematics 1B
    ("Multivariable Calculus",               "SMA102",   "004A"),
    # → Mathematics 2
    ("Ordinary Differential Equations (ODEs)", "SMA209", "001A"),
    ("Fourier Analysis",                     "SMA209",   "003A"),
    ("Laplace Transforms",                   "SMA209",   "004A"),
    ("Partial Differential Equations (PDEs)", "SMA209",  "009A"),
]

# Brand-new topics to CREATE in new courses.
# Structure: (course_code, topic_code, topic_name)
NEW_TOPICS = [
    # Mathematics 1A — SMA101
    ("SMA101", "001A", "Functions & Limits"),
    ("SMA101", "001B", "Continuity & Exponential Functions"),
    ("SMA101", "002B", "Curve Sketching & Optimisation"),
    ("SMA101", "003B", "Applications of Integration"),
    ("SMA101", "004A", "Complex Numbers"),
    ("SMA101", "004B", "Vectors in 2D & 3D"),
    ("SMA101", "005B", "Systems of Linear Equations"),
    # Mathematics 1B — SMA102
    ("SMA102", "001A", "Advanced Integration Techniques"),
    ("SMA102", "001B", "Volumes, Surface Areas & Applications"),
    ("SMA102", "002A", "Numerical Methods"),
    ("SMA102", "003A", "Vector Spaces & Linear Transformations"),
    ("SMA102", "003B", "Eigenvalues & Eigenvectors"),
    ("SMA102", "004B", "Vector Functions & Line Integrals"),
    ("SMA102", "005A", "Surface Integrals & Green's Theorem"),
    ("SMA102", "005B", "Gauss's Divergence Theorem"),
    # Mathematics 2 — SMA209
    ("SMA209", "001B", "Second-Order ODEs (Homogeneous)"),
    ("SMA209", "002A", "Second-Order ODEs (Non-Homogeneous)"),
    ("SMA209", "002B", "Systems of ODEs"),
    ("SMA209", "003B", "Fourier Transforms"),
    ("SMA209", "004B", "Laplace Transforms — Applications"),
    # Data Analytics — SMA212
    ("SMA212", "001A", "Descriptive Statistics & Visualisation"),
    ("SMA212", "002A", "Inferential Statistics"),
    ("SMA212", "003A", "Data Preprocessing"),
    ("SMA212", "004A", "Clustering Methods"),
    ("SMA212", "005A", "Frequent Pattern Mining"),
    ("SMA212", "006A", "Regression Analysis"),
    ("SMA212", "007A", "Classification Algorithms"),
    ("SMA212", "008A", "Big Data Concepts"),
    ("SMA212", "009A", "Data Ethics, Privacy & Ownership"),
    ("SMA212", "010A", "Python & Pandas for Data Analytics"),
]

# Course definitions: (code, name, description)
NEW_COURSES = [
    (
        "FOUND101",
        "Foundation Mathematics",
        (
            "Pre-university bridging course covering arithmetic, algebra, geometry, "
            "trigonometry, and pre-calculus. Recommended before SMA101."
        ),
    ),
    (
        "SMA101",
        "Mathematics 1A",
        (
            "CDU SMA101 — functions, limits, continuity, differential and integral calculus, "
            "complex numbers, vectors, and an introduction to linear algebra."
        ),
    ),
    (
        "SMA102",
        "Mathematics 1B",
        (
            "CDU SMA102 — multivariable calculus, advanced integration, numerical methods, "
            "vector calculus, linear algebra, and surface/line integrals."
        ),
    ),
    (
        "SMA209",
        "Mathematics 2",
        (
            "CDU SMA209 — ordinary and partial differential equations, systems of ODEs, "
            "Fourier analysis, Fourier transforms, and Laplace transform applications."
        ),
    ),
    (
        "SMA212",
        "Data Analytics",
        (
            "CDU SMA212 — statistics, data preprocessing, clustering, pattern mining, "
            "regression, classification, big data, data ethics, and Python/Pandas."
        ),
    ),
]


def restructure_mathematics(apps, schema_editor):
    Course = apps.get_model("study", "Course")
    Topic = apps.get_model("study", "Topic")
    CourseEnrollment = apps.get_model("study", "CourseEnrollment")
    User = apps.get_model("auth", "User")

    # Fetch system user
    try:
        system_user = User.objects.get(username="system")
    except User.DoesNotExist:
        # Nothing to do on a blank install — courses come from 0013 which
        # already uses the same system user.
        return

    # ------------------------------------------------------------------
    # 1. Create (or retrieve) the five new courses
    # ------------------------------------------------------------------
    course_map = {}  # code → Course instance
    for code, name, description in NEW_COURSES:
        course, _ = Course.objects.get_or_create(
            code=code,
            defaults={
                "name": name,
                "description": description,
                "created_by": system_user,
            },
        )
        course_map[code] = course

    # ------------------------------------------------------------------
    # 2. Move existing topics from Engineering Mathematics
    # ------------------------------------------------------------------
    try:
        eng_math = Course.objects.get(
            name="Engineering Mathematics",
            created_by=system_user,
        )
    except Course.DoesNotExist:
        eng_math = None  # already restructured on a previous run

    if eng_math is not None:
        for old_name, new_course_code, new_code in MOVES:
            Topic.objects.filter(
                course=eng_math,
                name=old_name,
            ).update(
                course=course_map[new_course_code],
                code=new_code,
            )

    # ------------------------------------------------------------------
    # 3. Create new topics that didn't exist in Engineering Mathematics
    # ------------------------------------------------------------------
    for course_code, topic_code, topic_name in NEW_TOPICS:
        Topic.objects.get_or_create(
            course=course_map[course_code],
            name=topic_name,
            defaults={"code": topic_code, "order": 0},
        )
        # In case it already exists but code wasn't set (idempotent guard)
        Topic.objects.filter(
            course=course_map[course_code],
            name=topic_name,
            code="",
        ).update(code=topic_code)

    # ------------------------------------------------------------------
    # 4. Delete Engineering Mathematics (should now be empty)
    # ------------------------------------------------------------------
    if eng_math is not None:
        remaining = Topic.objects.filter(course=eng_math).count()
        if remaining == 0:
            eng_math.delete()

    # ------------------------------------------------------------------
    # 5. Back-fill CourseEnrollment for all non-system users
    # ------------------------------------------------------------------
    non_system_users = User.objects.exclude(username="system")
    for user in non_system_users:
        for course in course_map.values():
            CourseEnrollment.objects.get_or_create(
                user=user,
                course=course,
                defaults={"status": "studying"},
            )


def reverse_func(apps, schema_editor):
    # Intentional no-op: reversing a destructive restructure is not safe
    # without a full data backup.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("study", "0028_alter_topic_options_and_more"),
    ]

    operations = [
        migrations.RunPython(restructure_mathematics, reverse_func),
    ]
