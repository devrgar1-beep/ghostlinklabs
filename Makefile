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
.PHONY: docker-build docker-up docker-down dlogs doctor mesh responder dpeer ci-up ci-down backbone-deploy backbone-discover neighbors-file

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

# Deploy responders to backbone hosts listed in backbone_hosts.txt
backbone-deploy:
	BACKBONE_USER=${BACKBONE_USER} scripts/deploy_responder.sh backbone_hosts.txt

# Discover responders on the backbone CIDR(s) and write creds/neighbors.txt
# Example: make backbone-discover CIDR="192.168.4.0/22 10.10.0.0/24"
backbone-discover:
	[[ -n "${CIDR}" ]] || (echo "Set CIDR=..." && exit 1)
	OUT_FILE=./creds/neighbors.txt scripts/discover_backbone.py ${CIDR}

# Configure .env to use the neighbors file mounted into the container
neighbors-file:
	grep -q '^NEIGHBORS_FILE=' .env && sed -i 's#^NEIGHBORS_FILE=.*#NEIGHBORS_FILE=/run/ghostlink/neighbors.txt#' .env || echo 'NEIGHBORS_FILE=/run/ghostlink/neighbors.txt' >> .env
	grep -q '^NEIGHBOR_IPS=' .env && sed -i 's/^NEIGHBOR_IPS=.*/NEIGHBOR_IPS=/' .env || true
	@echo 'Updated .env to use NEIGHBORS_FILE=/run/ghostlink/neighbors.txt. Ensure ./creds/neighbors.txt exists.'

# iDRAC operations
.PHONY: idrac-discover idrac-status idrac-health idrac-monitor

# Discover iDRACs on management network and update idrac_inventory.txt
# Example: make idrac-discover MGMT_CIDR="10.10.100.0/24"
idrac-discover:
	[[ -n "${MGMT_CIDR}" ]] || (echo "Set MGMT_CIDR=..." && exit 1)
	scripts/discover_idrac.py ${MGMT_CIDR}

# Show status of an iDRAC host
# Example: make idrac-status HOST=10.10.100.21
idrac-status:
	[[ -n "${HOST}" ]] || (echo "Set HOST=..." && exit 1)
	scripts/idrac_ctl.sh status ${HOST}

# Show health of an iDRAC host
idrac-health:
	[[ -n "${HOST}" ]] || (echo "Set HOST=..." && exit 1)
	scripts/idrac_ctl.sh health ${HOST}

# Start iDRAC health monitor daemon
idrac-monitor:
	python3 gl_idrac_monitor.py

# CI compose with port mappings
ci-up:
	docker compose -f docker-compose.ci.yml up -d --build

ci-down:
	docker compose -f docker-compose.ci.yml down

# New: docker-compose for this project's dev infra
compose-build:
	docker compose -f docker/docker-compose.yml build

compose-up:
	docker compose -f docker/docker-compose.yml up -d --remove-orphans

compose-down:
	docker compose -f docker/docker-compose.yml down

compose-logs:
	docker compose -f docker/docker-compose.yml logs -f


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
