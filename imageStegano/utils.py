import secrets
import uuid


def genereate_unique_enc_key(length=40):
    return secrets.token_urlsafe(length)


def upload_path(instance, filename):
    # get app name from instance
    app_name = instance._meta.app_label

    # get model name from instance
    model_name = instance.__class__.__name__.lower()

    # slugify file name
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    # return path
    return f"{app_name}/{model_name}/{filename}"
