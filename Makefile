PYTHON ?= python3
WORK ?= work
DIST ?= dist
CONFIG ?= configs/default.yaml

.PHONY: test smoke smoke-teaching inspect resolve validate validate-teaching package

test:
	$(PYTHON) -m pytest

smoke:
	$(PYTHON) scripts/test_context_detector.py

smoke-teaching:
	$(PYTHON) scripts/validate_teaching.py examples/delta_force_session/teaching_lessons.json
	$(PYTHON) scripts/validate_episode_script.py examples/episode_script.json
	$(PYTHON) scripts/validate_episode_handoff.py examples/scene_recipe.json
	$(PYTHON) scripts/validate_edit_map.py examples/delta_force_session/edit_map.json

inspect:
	$(PYTHON) scripts/inspect_source.py $(SOURCE)

resolve:
	$(PYTHON) scripts/resolve_candidates.py $(WORK)/raw_candidate_inventory.json -o $(WORK)/resolved_event_map.json

validate:
	$(PYTHON) scripts/validate_pipeline.py --workdir $(WORK)

validate-teaching:
	$(MAKE) smoke-teaching

package:
	git archive --format=tar.gz --output=goal-aware-gameplay-coaching-agent.tar.gz HEAD
