#/bin/bash
docker compose exec -it tester poetry run python -u -m scripts."$@"
