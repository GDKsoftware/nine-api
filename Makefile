default: client

SETUPPYTHON:=$(shell env PATH=/bin:/usr/bin:/usr/local/bin bash -c "command -v python3 || echo .python3-not-found")
VIRTUALENV?=.env
VIRTUALENV_DONE:=$(VIRTUALENV)/.done
export PYTHONPATH=$(CURDIR)/bin
PYTHON=$(VIRTUALENV)/bin/python3

NINE_DEV=$(shell pwd)
PROTOC_ROOT=${NINE_DEV}/protoc
PROTOC=${PROTOC_ROOT}/bin/protoc
PROTOBUF_INC=${PROTOC_ROOT}/include

NINE_DEFINITIONS=${NINE_DEV}/definitions

$(SETUPPYTHON):
	@echo "Python 3 not found on path. Please install (sudo apt install python3.8 python3.8-venv or similar)"
	@exit 1

$(VIRTUALENV_DONE): requirements.txt
	$(SETUPPYTHON) -m venv $(VIRTUALENV)
	$(VIRTUALENV)/bin/pip install --upgrade pip
	$(VIRTUALENV)/bin/pip install -r requirements.txt
	touch $(VIRTUALENV_DONE)

$(PROTOC):
	curl -L https://github.com/protocolbuffers/protobuf/releases/download/v3.20.1/protoc-3.20.1-linux-x86_64.zip --output protoc.zip
	unzip protoc.zip -d protoc
	rm protoc.zip

lib: definitions/nine.proto $(PROTOC)
	mkdir -p ${NINE_DEV}/libnine
	mkdir -p ${NINE_DEV}/libcpp
	${PROTOC} --proto_path=${PROTOC_ROOT} -I${PROTOBUF_INC} -I${NINE_DEFINITIONS} --python_out=${NINE_DEV}/libnine --cpp_out=${NINE_DEV}/libcpp nine.proto

client: $(VIRTUALENV_DONE)
	$(PYTHON) test_client.py

server: $(VIRTUALENV_DONE)
	$(PYTHON) test_server.py

clean:
	rm -rf $(VIRTUALENV)
	rm -rf __pycache__
	rm -rf libnine/__pycache__
	rm -rf protoc
