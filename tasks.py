from invoke import task

GCLOUD_PROJECT = "kupcimat"
GCLOUD_OPTIONS = "--platform managed --region us-central1"


@task(help={"tag": "Docker image name and tag",
            "dockerfile": "Dockerfile name"})
def build_image(ctx, tag, dockerfile):
    """
    Build docker image locally
    """
    ctx.run(f"docker build --file {dockerfile} --tag {tag} .")


@task(help={"tag": "Docker image name and tag"})
def push_image(ctx, tag):
    """
    Push docker image to registry
    """
    ctx.run(f"docker push {tag}")


@task(help={"service": "Service name"})
def deploy_service(ctx, service):
    """
    Deploy service to gcloud
    """
    ctx.run(f"gcloud beta run services replace deployment/{service}.yaml {GCLOUD_OPTIONS}")


@task(help={"service": "Service name",
            "public": "Allow public access (optional)"})
def deploy(ctx, service, public=False):
    """
    Build and deploy service to default gcloud project
    """
    ctx.run("gcloud auth configure-docker gcr.io")
    dockerfile = f"Dockerfile-{service}"
    image_name = f"gcr.io/{GCLOUD_PROJECT}/{service}"
    build_image(ctx, image_name, dockerfile)
    push_image(ctx, image_name)
    deploy_service(ctx, service)
    if public:
        allow_public_service(ctx, service)


@task(help={"service": "Service name"})
def delete_service(ctx, service):
    """
    Delete service in gcloud
    """
    ctx.run(f"gcloud beta run services delete {service}-service {GCLOUD_OPTIONS}")


@task(help={"service": "Service name"})
def allow_public_service(ctx, service):
    """
    Allow public access for service
    """
    ctx.run(f"gcloud beta run services add-iam-policy-binding {service}-service"
            f" --member='allUsers' --role='roles/run.invoker' {GCLOUD_OPTIONS}")


@task(help={"service": "Service name"})
def block_public_service(ctx, service):
    """
    Block public access for service
    """
    ctx.run(f"gcloud beta run services remove-iam-policy-binding {service}-service"
            f" --member='allUsers' --role='roles/run.invoker' {GCLOUD_OPTIONS}")
