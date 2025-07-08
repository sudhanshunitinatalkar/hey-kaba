WEBSITE="http://kaba.ai"
DESCRIPTION="KabaCorp, Inc Browser"
NAME=hey-kaba

# super lazy
push:
	git add . && git commit -a -m 'update: WIP' && git pull && git push

build:
	echo "word"

reload:
	@esphome clean hey_kaba.yaml
	@esphome compile hey_kaba.yaml
	@esphome upload hey_kaba.yaml

clean:
	@rm -rf cache/

.PHONY: build
