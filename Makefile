PYTHON ?= python3
WORK ?= work
DIST ?= dist
CONFIG ?= configs/default.yaml

.PHONY: test smoke inspect resolve validate package

test:
	$(PYTHON) -m pytest

smoke:
	$(PYTHON) scripts/test_context_detector.py

inspect:
	$(PYTHON) scripts/inspect_source.py $(SOURCE)

resolve:
	$(PYTHON) scripts/resolve_candidates.py $(WORK)/raw_candidate_inventory.json -o $(WORK)/resolved_event_map.json

validate:
	$(PYTHON) scripts/validate_pipeline.py --workdir $(WORK)

package:
	git archive --format=tar.gz --output=goal-aware-gameplay-coaching-agent.tar.gz HEAD
