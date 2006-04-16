#!/bin/sh

[ $# -gt 1 ] || exit 1

TYPE="$1"
shift

find_dir() {
	while read DIR; do
		for D in $(find -type d -name $DIR); do
			echo "$TYPE,install,url,jar:resource:/chrome/$JAR!${D#.}/"
			echo "$TYPE,install,url,jar:resource:/chrome/$JAR!$(dirname ${D#.})/" | sed 's@///*@/@g'
		done
	done
}

while [ -n "$1" ]; do
	DIR=$(mktemp -d unzip.XXXXXX)
	cd $DIR
	unzip ../$1 >/dev/null
	JAR=$(basename $1)
	
	find -name contents.rdf \
		| xargs cat \
		| perl -pi -e '
			$txt .= $_;
			$_ = undef; 
			END { 
				while( $txt =~ s/<chrome:packages>(.*?)<\/chrome:packages>//s ) {
					$t = $1;
					while ( $t =~ s/<RDF:li\s+resource=".*:(\S+?)"// ) {
						print $1 ."\n";
					}
				}
			}' | find_dir | sort -u
	cd ..
	rm -rf $DIR
	shift
done

# vim: ts=4:sw=4
