SHARED_DIR=$1

apt update
apt-get install -y java-common
JAVA_ARCHIVE=$(find $SHARED_DIR -name "jdk*.tar.gz" -print -quit)

if [ ! -f $JAVA_ARCHIVE ]; then
     >&2 echo Could not find JDK
     exit 1
fi

if [ ! -d "/usr/lib/jvm" ]; then
     mkdir /usr/lib/jvm
fi

if [ ! -d "/usr/lib/jvm/java-8-oracle" ]; then
     cd /usr/lib/jvm
     tar -xf $JAVA_ARCHIVE
     mv `tar -tf $JAVA_ARCHIVE | head -1` java-8-oracle

     update-alternatives --install /usr/bin/servertool servertool  /usr/lib/jvm/java-8-oracle/jre/bin/servertool 1820
     update-alternatives --install /usr/bin/keytool keytool  /usr/lib/jvm/java-8-oracle/jre/bin/keytool 1820
     update-alternatives --install /usr/bin/java java  /usr/lib/jvm/java-8-oracle/jre/bin/java 1820
     update-alternatives --install /usr/bin/jcontrol jcontrol  /usr/lib/jvm/java-8-oracle/jre/bin/jcontrol 1820
     update-alternatives --install /usr/bin/rmid rmid  /usr/lib/jvm/java-8-oracle/jre/bin/rmid 1820
     update-alternatives --install /usr/bin/ControlPanel ControlPanel  /usr/lib/jvm/java-8-oracle/jre/bin/ControlPanel 1820
     update-alternatives --install /usr/bin/rmiregistry rmiregistry  /usr/lib/jvm/java-8-oracle/jre/bin/rmiregistry 1820
     update-alternatives --install /usr/bin/orbd orbd  /usr/lib/jvm/java-8-oracle/jre/bin/orbd 1820
     update-alternatives --install /usr/bin/jjs jjs  /usr/lib/jvm/java-8-oracle/jre/bin/jjs 1820
     update-alternatives --install /usr/bin/pack200 pack200  /usr/lib/jvm/java-8-oracle/jre/bin/pack200 1820
     update-alternatives --install /usr/bin/tnameserv tnameserv  /usr/lib/jvm/java-8-oracle/jre/bin/tnameserv 1820
     update-alternatives --install /usr/bin/unpack200 unpack200  /usr/lib/jvm/java-8-oracle/jre/bin/unpack200 1820
     update-alternatives --install /usr/bin/policytool policytool  /usr/lib/jvm/java-8-oracle/jre/bin/policytool 1820
     update-alternatives --install /usr/bin/javaws javaws  /usr/lib/jvm/java-8-oracle/jre/bin/javaws 1820
     update-alternatives --install /usr/bin/rmic rmic  /usr/lib/jvm/java-8-oracle/bin/rmic 1820
     update-alternatives --install /usr/bin/jvisualvm jvisualvm  /usr/lib/jvm/java-8-oracle/bin/jvisualvm 1820
     update-alternatives --install /usr/bin/xjc xjc  /usr/lib/jvm/java-8-oracle/bin/xjc 1820
     update-alternatives --install /usr/bin/jinfo jinfo  /usr/lib/jvm/java-8-oracle/bin/jinfo 1820
     update-alternatives --install /usr/bin/schemagen schemagen  /usr/lib/jvm/java-8-oracle/bin/schemagen 1820
     update-alternatives --install /usr/bin/jdb jdb  /usr/lib/jvm/java-8-oracle/bin/jdb 1820
     update-alternatives --install /usr/bin/java-rmi.cgi java-rmi.cgi  /usr/lib/jvm/java-8-oracle/bin/java-rmi.cgi 1820
     update-alternatives --install /usr/bin/wsimport wsimport  /usr/lib/jvm/java-8-oracle/bin/wsimport 1820
     update-alternatives --install /usr/bin/jarsigner jarsigner  /usr/lib/jvm/java-8-oracle/bin/jarsigner 1820
     update-alternatives --install /usr/bin/jmap jmap  /usr/lib/jvm/java-8-oracle/bin/jmap 1820
     update-alternatives --install /usr/bin/serialver serialver  /usr/lib/jvm/java-8-oracle/bin/serialver 1820
     update-alternatives --install /usr/bin/jcmd jcmd  /usr/lib/jvm/java-8-oracle/bin/jcmd 1820
     update-alternatives --install /usr/bin/native2ascii native2ascii  /usr/lib/jvm/java-8-oracle/bin/native2ascii 1820
     update-alternatives --install /usr/bin/jstatd jstatd  /usr/lib/jvm/java-8-oracle/bin/jstatd 1820
     update-alternatives --install /usr/bin/javac javac  /usr/lib/jvm/java-8-oracle/bin/javac 1820
     update-alternatives --install /usr/bin/jstack jstack  /usr/lib/jvm/java-8-oracle/bin/jstack 1820
     update-alternatives --install /usr/bin/wsgen wsgen  /usr/lib/jvm/java-8-oracle/bin/wsgen 1820
     update-alternatives --install /usr/bin/idlj idlj  /usr/lib/jvm/java-8-oracle/bin/idlj 1820
     update-alternatives --install /usr/bin/javah javah  /usr/lib/jvm/java-8-oracle/bin/javah 1820
     update-alternatives --install /usr/bin/javafxpackager javafxpackager  /usr/lib/jvm/java-8-oracle/bin/javafxpackager 1820
     update-alternatives --install /usr/bin/javapackager javapackager  /usr/lib/jvm/java-8-oracle/bin/javapackager 1820
     update-alternatives --install /usr/bin/jsadebugd jsadebugd  /usr/lib/jvm/java-8-oracle/bin/jsadebugd 1820
     update-alternatives --install /usr/bin/jps jps  /usr/lib/jvm/java-8-oracle/bin/jps 1820
     update-alternatives --install /usr/bin/jrunscript jrunscript  /usr/lib/jvm/java-8-oracle/bin/jrunscript 1820
     update-alternatives --install /usr/bin/jhat jhat  /usr/lib/jvm/java-8-oracle/bin/jhat 1820
     update-alternatives --install /usr/bin/javap javap  /usr/lib/jvm/java-8-oracle/bin/javap 1820
     update-alternatives --install /usr/bin/jdeps jdeps  /usr/lib/jvm/java-8-oracle/bin/jdeps 1820
     update-alternatives --install /usr/bin/jstat jstat  /usr/lib/jvm/java-8-oracle/bin/jstat 1820
     update-alternatives --install /usr/bin/appletviewer appletviewer  /usr/lib/jvm/java-8-oracle/bin/appletviewer 1820
     update-alternatives --install /usr/bin/extcheck extcheck  /usr/lib/jvm/java-8-oracle/bin/extcheck 1820
     update-alternatives --install /usr/bin/javadoc javadoc  /usr/lib/jvm/java-8-oracle/bin/javadoc 1820
     update-alternatives --install /usr/bin/jar jar  /usr/lib/jvm/java-8-oracle/bin/jar 1820
     update-alternatives --install /usr/bin/jconsole jconsole  /usr/lib/jvm/java-8-oracle/bin/jconsole 1820

     cp "$SHARED_DIR/configs/.java-8-oracle.jinfo" .

    update-java-alternatives --set java-8-oracle
fi


# Set JAVA_HOME variable both now and for when the system restarts
export JAVA_HOME
JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")
echo "JAVA_HOME=$JAVA_HOME" >> /etc/environment