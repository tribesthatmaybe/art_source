# Would it be worth it to harvest the targets from the sidecars and use the
# destinations as the make targets? probably not, but I bet it would be fun.
# This is why real game editors use databases :D
files := $(shell scripts/get_changed_sources.py --ext .xcf)
.PHONY: changed build_container clean $(files)

DOCKER_IMAGE = tribesthatmaybe/art_build:later
WHEEL = build_tools/tribes_art_build_tools-13-py2-none-any.whl

ifdef EXPORT_ROOT
	OUT_DIR = --export_root $(EXPORT_ROOT)
endif

$(WHEEL): clean
	cd build_tools && python2 setup.py bdist_wheel -d .

build_container: $(WHEEL)
	docker build --tag $(DOCKER_IMAGE) build_tools

changed: $(files)

$(files): build_container
	docker run -v "$(shell pwd):/source" $(DOCKER_IMAGE) $(OUT_DIR) $@

all: build_container
	docker run -v "$(shell pwd):/source" $(DOCKER_IMAGE) $(OUT_DIR) .

clean:
	rm -f $(WHEEL)
