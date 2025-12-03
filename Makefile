# Quick ops
.PHONY: env ctl peer bridge sanity

SHELL := /bin/bash

env:
	@echo "HOST=$${HOST:-10.7.0.1} PORT=$${PORT:-7420} PROM=$${PROMETHEUS_BIND:-127.0.0.1:9108}"

ctl:
	python3 gl_controller_metrics_env.py

peer:
	python3 gl_peer.py

bridge:
	OPENAI_API_KEY=$$OPENAI_API_KEY python3 gl_openai_bridge.py

sanity:
	bash gl_sanity_check.sh

# Quick ops (local)
.PHONY: logs status up down

logs:
	bash run_venv.sh logs

status:
	bash run_venv.sh status

up:
	bash run_venv.sh up

down:
	bash run_venv.sh down

# Docker helpers
.PHONY: docker-build docker-up docker-down dlogs doctor mesh responder dpeer ci-up ci-down

docker-build:
	docker build -t ghostlink:latest .

docker-up:
	docker compose up -d

docker-down:
	docker compose down

dlogs:
	docker logs -f ghostlink

doctor:
	ss -ltnp | egrep ':7420|:7422|:9108' || true
	curl -fsS http://127.0.0.1:9108/metrics | head -n 10 || true

mesh:
	sed -i 's/RUN_MESH=0/RUN_MESH=1/' docker-compose.yml
	docker compose up -d --build

responder:
	sed -i 's/RUN_RESPONDER=0/RUN_RESPONDER=1/' docker-compose.yml
	docker compose up -d --build

dpeer:
	sed -i 's/RUN_PEER=0/RUN_PEER=1/' docker-compose.yml
	docker compose up -d --build

# CI compose with port mappings
ci-up:
	docker compose -f docker-compose.ci.yml up -d --build

ci-down:
	docker compose -f docker-compose.ci.yml down

env:
\t@echo "HOST=$${HOST:-10.7.0.1} PORT=$${PORT:-7420} PROM=$${PROMETHEUS_BIND:-127.0.0.1:9108}"

ctl:
\tpython3 gl_controller_metrics_env.py

peer:
\tpython3 gl_peer.py

bridge:
\tOPENAI_API_KEY=$$OPENAI_API_KEY python3 gl_openai_bridge.py

sanity:
\tbash gl_sanity_check.sh
