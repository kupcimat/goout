from kupcimat.config_util import get_int, get_str

PORT = get_int("PORT", default=8080)
BUCKET_NAME = get_str("BUCKET_NAME")
