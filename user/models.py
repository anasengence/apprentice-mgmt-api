import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# ───────────────────────────────────
# 1. USER MANAGEMENT
# ───────────────────────────────────


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name, last_name, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, first_name, last_name, password, **extra_fields)


# ───────────────────────────────────
# 2. USER MODEL
# ───────────────────────────────────


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_trainer = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)
    is_apprentice = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"] 

    def __str__(self):
        return self.email + " " + str(self.id)


# ───────────────────────────────────
# 3. TRAINER MODEL
# ───────────────────────────────────


class Trainer(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, related_name="trainer_profile"
    )

    def __str__(self):
        return self.user.email + " " + str(self.user.id)


# ───────────────────────────────────
# 4. MENTOR MODEL
# ───────────────────────────────────


class Mentor(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, related_name="mentor_profile"
    )
    trainer = models.ForeignKey(
        Trainer, on_delete=models.CASCADE, related_name="mentors"
    )
    is_external = models.BooleanField(default=False)
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mentors",
    )

    def __str__(self):
        return self.user.email + " " + str(self.user.id)


# ───────────────────────────────────
# 5. APPRENTICE MODEL
# ───────────────────────────────────


class Apprentice(models.Model):
    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="apprentice_profile",
    )
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="apprentices",
    )
    mentor = models.ForeignKey(
        Mentor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="apprentices",
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="apprentices",
    )

    def __str__(self):
        return self.user.email + " " + str(self.user.id)
