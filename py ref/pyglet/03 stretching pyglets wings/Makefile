# this Makefile works from Cygwin

project=stretching_pyglets_wings
version=1.3
zipname=${project}-${version}

all: presentation.html

presentation.html: presentation\presentation.rst
	( \
    cd presentation; \
	python ${SYSTEMDRIVE}\\Python25\\Scripts\\rst2s5.py --theme-url ui/custom presentation.rst index.html; \
    )

clean:
	-rm presentation/index.html
	-find . \( \
		-name 'tags' -o \
		-name '*.pyc' -o \
		-name '*.pyo' \
		\) -exec rm {} \;

zip: clean all
	-rm -rf ../${zipname} ../${zipname}.zip ../presentation
	cp -r . ../${zipname}
	-find ../${zipname} -name '.svn' -exec rm -rf {} \;
	mv ../${zipname}/presentation ..
	( \
		cd ..; \
		zip -r ${zipname}.zip ${zipname}; \
	)
	-rm -rf ../${zipname}

.PHONY: all, clean

