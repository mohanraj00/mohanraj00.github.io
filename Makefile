# Blog operations. Usage: make help
SHELL := /bin/bash

.PHONY: help preview build check publish

help: ## Show this help
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  \033[1m%-9s\033[0m %s\n", $$1, $$2}'

preview: ## Serve the site locally at http://localhost:4000 (Docker; matches GH Pages build)
	docker run --rm -it -p 4000:4000 -v "$$PWD":/srv/jekyll -w /srv/jekyll ruby:3.3 \
		bash -c "bundle install --quiet && bundle exec jekyll serve --host 0.0.0.0 --future"

build: ## One-off build into _site/ (Docker)
	docker run --rm -v "$$PWD":/srv/jekyll -w /srv/jekyll ruby:3.3 \
		bash -c "bundle install --quiet && bundle exec jekyll build --future" && ls _site/synapse/ 2>/dev/null

check: ## What would be published: unpushed commits + working-tree state
	@git status --short; echo "---"; git log --oneline origin/main..HEAD

publish: ## Push to GitHub Pages (THE publish action — asks first)
	@read -p "Push to origin/main and publish the site? [y/N] " a; [[ $$a == y* ]] && git push origin main || echo "aborted"
