rm -rf /tmp/scalex-doc-old
mv -f doc /tmp/scalex-doc-old
mkdir doc
epydoc --html -v -o doc/ scalex --no-private --no-sourcecode
#epydoc --html -v -o doc/ scalex --no-private
